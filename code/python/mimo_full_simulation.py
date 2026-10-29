import os
import numpy as np
import scipy.linalg as la
import matplotlib.pyplot as plt

baseDirectory = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
figuresDirectory = os.path.join(baseDirectory, "figures")
os.makedirs(figuresDirectory, exist_ok=True)

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.size"] = 10
plt.rcParams["axes.linewidth"] = 1.0
plt.rcParams["grid.alpha"] = 0.4
plt.rcParams["grid.linestyle"] = "--"

channelMatrixH = np.array([[0.7, 0.3], [0.4, 0.6]], dtype=complex)
symbolVectorX = np.array([1.0 + 1.0j, 1.0 - 1.0j], dtype=complex)

h11 = channelMatrixH[0, 0]
h12 = channelMatrixH[0, 1]
h21 = channelMatrixH[1, 0]
h22 = channelMatrixH[1, 1]

s0 = symbolVectorX[0]
s1 = symbolVectorX[1]

receivedSignalR0 = h11 * s0 + h12 * s1
receivedSignalR1 = -h11 * np.conj(s1) + h12 * np.conj(s0)
receivedSignalR2 = h21 * s0 + h22 * s1
receivedSignalR3 = -h21 * np.conj(s1) + h22 * np.conj(s0)

frobeniusNormSquaredH = np.abs(h11)**2 + np.abs(h12)**2 + np.abs(h21)**2 + np.abs(h22)**2

combinerOutputZ0 = np.conj(h11) * receivedSignalR0 + h12 * np.conj(receivedSignalR1) + \
                   np.conj(h21) * receivedSignalR2 + h22 * np.conj(receivedSignalR3)

combinerOutputZ1 = np.conj(h12) * receivedSignalR0 - h11 * np.conj(receivedSignalR1) + \
                   np.conj(h22) * receivedSignalR2 - h21 * np.conj(receivedSignalR3)

recoveredSymbolHatS0 = combinerOutputZ0 / frobeniusNormSquaredH
recoveredSymbolHatS1 = combinerOutputZ1 / frobeniusNormSquaredH

errorStbcS0 = np.abs(recoveredSymbolHatS0 - s0)
errorStbcS1 = np.abs(recoveredSymbolHatS1 - s1)

receivedVectorSdmY = channelMatrixH @ symbolVectorX

weightMatrixZf = la.pinv(channelMatrixH)
recoveredVectorZf = weightMatrixZf @ receivedVectorSdmY
errorNormZf = la.norm(recoveredVectorZf - symbolVectorX)

noiseVarianceSdm = 0.0
weightMatrixMmse = la.inv(channelMatrixH.conj().T @ channelMatrixH + noiseVarianceSdm * np.eye(2)) @ channelMatrixH.conj().T
recoveredVectorMmse = weightMatrixMmse @ receivedVectorSdmY
errorNormMmse = la.norm(recoveredVectorMmse - symbolVectorX)

leftSingularMatrixU, singularValuesS, rightSingularMatrixVh = la.svd(channelMatrixH)
unitaryMatrixV = rightSingularMatrixVh.conj().T
precodedVectorX = unitaryMatrixV @ symbolVectorX
receivedVectorSvd = channelMatrixH @ precodedVectorX
combinedVectorSvd = leftSingularMatrixU.conj().T @ receivedVectorSvd
recoveredVectorSvd = combinedVectorSvd / singularValuesS
errorNormSvd = la.norm(recoveredVectorSvd - symbolVectorX)

figureStbc, axesStbc = plt.subplots(1, 2, figsize=(14, 6), dpi=300)

axesStbc[0].axhline(0, color="gray", linestyle="--", linewidth=0.8)
axesStbc[0].axvline(0, color="gray", linestyle="--", linewidth=0.8)

axesStbc[0].scatter([s0.real, s1.real], [s0.imag, s1.imag],
                    color="blue", s=130, marker="o", label="Tx Symbols (s0, s1)", zorder=5)

axesStbc[0].scatter([receivedSignalR0.real, receivedSignalR1.real, receivedSignalR2.real, receivedSignalR3.real],
                    [receivedSignalR0.imag, receivedSignalR1.imag, receivedSignalR2.imag, receivedSignalR3.imag],
                    color="crimson", s=90, marker="^", label="Received (r0, r1, r2, r3)", zorder=4)

axesStbc[0].scatter([combinerOutputZ0.real, combinerOutputZ1.real],
                    [combinerOutputZ0.imag, combinerOutputZ1.imag],
                    color="orange", s=110, marker="s", label="Combiner Output (z0, z1)", zorder=4)

axesStbc[0].scatter([recoveredSymbolHatS0.real, recoveredSymbolHatS1.real],
                    [recoveredSymbolHatS0.imag, recoveredSymbolHatS1.imag],
                    color="forestgreen", s=160, marker="x", linewidths=2.5, label="Recovered (s_hat0, s_hat1)", zorder=6)

for labelText, pointCoord in [("s0", s0), ("s1", s1),
                              ("r0", receivedSignalR0), ("r1", receivedSignalR1),
                              ("r2", receivedSignalR2), ("r3", receivedSignalR3),
                              ("z0", combinerOutputZ0), ("z1", combinerOutputZ1),
                              ("s_hat0", recoveredSymbolHatS0), ("s_hat1", recoveredSymbolHatS1)]:
    axesStbc[0].annotate(f"{labelText} ({pointCoord.real:+.2f}{pointCoord.imag:+.2f}i)",
                         (pointCoord.real, pointCoord.imag),
                         textcoords="offset points", xytext=(8, 5), fontsize=8.5)

axesStbc[0].set_title("Constellation & Signal Vectors in Complex Plane", fontsize=12, fontweight="bold")
axesStbc[0].set_xlabel("In-Phase (I)", fontsize=11)
axesStbc[0].set_ylabel("Quadrature (Q)", fontsize=11)
axesStbc[0].set_xlim(-1.8, 1.8)
axesStbc[0].set_ylim(-1.8, 1.8)
axesStbc[0].grid(True)
axesStbc[0].legend(loc="upper left", fontsize=9)

axesStbc[1].axis("off")
tableSignalData = [
    ["Tx s0", f"{s0.real:+.4f} {s0.imag:+.4f}i", "Tx s1", f"{s1.real:+.4f} {s1.imag:+.4f}i"],
    ["Rx r0 (t1, ant1)", f"{receivedSignalR0.real:+.4f} {receivedSignalR0.imag:+.4f}i", "Rx r1 (t2, ant1)", f"{receivedSignalR1.real:+.4f} {receivedSignalR1.imag:+.4f}i"],
    ["Rx r2 (t1, ant2)", f"{receivedSignalR2.real:+.4f} {receivedSignalR2.imag:+.4f}i", "Rx r3 (t2, ant2)", f"{receivedSignalR3.real:+.4f} {receivedSignalR3.imag:+.4f}i"],
    ["Combiner z0", f"{combinerOutputZ0.real:+.4f} {combinerOutputZ0.imag:+.4f}i", "Combiner z1", f"{combinerOutputZ1.real:+.4f} {combinerOutputZ1.imag:+.4f}i"],
    ["Recovered s_hat0", f"{recoveredSymbolHatS0.real:+.4f} {recoveredSymbolHatS0.imag:+.4f}i", "Recovered s_hat1", f"{recoveredSymbolHatS1.real:+.4f} {recoveredSymbolHatS1.imag:+.4f}i"],
    ["Error |s_hat0 - s0|", f"{errorStbcS0:.2e}", "Error |s_hat1 - s1|", f"{errorStbcS1:.2e}"],
    ["Channel Norm ||H||_F^2", f"{frobeniusNormSquaredH:.4f}", "Status", "Orthogonal Perfect Recovery"]
]

tableStbc = axesStbc[1].table(cellText=tableSignalData,
                              colLabels=["Signal 0", "Value", "Signal 1", "Value"],
                              loc="center", cellLoc="center")
tableStbc.auto_set_font_size(False)
tableStbc.set_fontsize(9.5)
tableStbc.scale(1.0, 2.0)
for (rowIndex, colIndex), cellObj in tableStbc.get_celld().items():
    if rowIndex == 0:
        cellObj.set_facecolor("#2b5c8f")
        cellObj.set_text_props(color="white", fontweight="bold")
    elif rowIndex % 2 == 1:
        cellObj.set_facecolor("#f0f4f8")

axesStbc[1].set_title("Step-by-Step Numerical Verification Table", fontsize=12, fontweight="bold", pad=20)

figureStbc.suptitle("MIMO 2x2 Alamouti STBC Signal Processing & Symbol Recovery", fontsize=14, fontweight="bold")
figureStbc.tight_layout()
figureStbcPath = os.path.join(figuresDirectory, "fig1_stbc_signal_recovery.png")
figureStbc.savefig(figureStbcPath, dpi=300)
plt.close(figureStbc)

figureSdm, axesSdm = plt.subplots(1, 3, figsize=(16, 5), dpi=300)

axesSdm[0].axhline(0, color="gray", linestyle="--", linewidth=0.8)
axesSdm[0].axvline(0, color="gray", linestyle="--", linewidth=0.8)
axesSdm[0].scatter([symbolVectorX[0].real, symbolVectorX[1].real],
                   [symbolVectorX[0].imag, symbolVectorX[1].imag],
                   color="blue", s=130, marker="o", label="Tx Symbols (x0, x1)", zorder=5)
axesSdm[0].scatter([receivedVectorSdmY[0].real, receivedVectorSdmY[1].real],
                   [receivedVectorSdmY[0].imag, receivedVectorSdmY[1].imag],
                   color="crimson", s=90, marker="^", label="Coupled Rx y = Hx", zorder=4)
axesSdm[0].scatter([recoveredVectorZf[0].real, recoveredVectorZf[1].real],
                   [recoveredVectorZf[0].imag, recoveredVectorZf[1].imag],
                   color="forestgreen", s=150, marker="x", linewidths=2.5, label="ZF Recovered x_hat", zorder=6)
axesSdm[0].set_title("Zero-Forcing Equalization", fontsize=11, fontweight="bold")
axesSdm[0].set_xlabel("In-Phase (I)", fontsize=10)
axesSdm[0].set_ylabel("Quadrature (Q)", fontsize=10)
axesSdm[0].set_xlim(-1.6, 1.6)
axesSdm[0].set_ylim(-1.6, 1.6)
axesSdm[0].grid(True)
axesSdm[0].legend(loc="upper left", fontsize=8.5)

axesSdm[1].axhline(0, color="gray", linestyle="--", linewidth=0.8)
axesSdm[1].axvline(0, color="gray", linestyle="--", linewidth=0.8)
axesSdm[1].scatter([symbolVectorX[0].real, symbolVectorX[1].real],
                   [symbolVectorX[0].imag, symbolVectorX[1].imag],
                   color="blue", s=130, marker="o", label="Original Symbols x", zorder=5)
axesSdm[1].scatter([precodedVectorX[0].real, precodedVectorX[1].real],
                   [precodedVectorX[0].imag, precodedVectorX[1].imag],
                   color="purple", s=90, marker="d", label="Precoded x_tx = Vx", zorder=4)
axesSdm[1].scatter([combinedVectorSvd[0].real, combinedVectorSvd[1].real],
                   [combinedVectorSvd[0].imag, combinedVectorSvd[1].imag],
                   color="darkorange", s=110, marker="s", label="Decoupled y_tilde = Sx", zorder=4)
axesSdm[1].scatter([recoveredVectorSvd[0].real, recoveredVectorSvd[1].real],
                   [recoveredVectorSvd[0].imag, recoveredVectorSvd[1].imag],
                   color="forestgreen", s=150, marker="x", linewidths=2.5, label="SVD Recovered x_hat", zorder=6)
axesSdm[1].set_title("SVD Precoding & Decoupling", fontsize=11, fontweight="bold")
axesSdm[1].set_xlabel("In-Phase (I)", fontsize=10)
axesSdm[1].set_ylabel("Quadrature (Q)", fontsize=10)
axesSdm[1].set_xlim(-1.8, 1.8)
axesSdm[1].set_ylim(-1.8, 1.8)
axesSdm[1].grid(True)
axesSdm[1].legend(loc="upper left", fontsize=8.5)

detectorNames = ["ZF Detection", "MMSE (Noise=0)", "SVD Precoding"]
detectorErrors = [errorNormZf, errorNormMmse, errorNormSvd]
barColors = ["#2b5c8f", "#d95f02", "#7570b3"]

axesSdm[2].bar(detectorNames, [max(err, 1e-16) for err in detectorErrors], color=barColors, width=0.55)
axesSdm[2].set_yscale("log")
axesSdm[2].set_ylim(1e-17, 1e-13)
axesSdm[2].set_title("Reconstruction Norm Error", fontsize=11, fontweight="bold")
axesSdm[2].set_ylabel("Error Norm ||x_hat - x||", fontsize=10)
axesSdm[2].grid(True, axis="y")
for barIndex, errVal in enumerate(detectorErrors):
    axesSdm[2].text(barIndex, max(errVal, 1e-16) * 2.5, f"{errVal:.2e}", ha="center", fontsize=9, fontweight="bold")

figureSdm.suptitle("MIMO 2x2 Spatial Division Multiplexing (SDM) Detection Comparison", fontsize=13, fontweight="bold")
figureSdm.tight_layout()
figureSdmPath = os.path.join(figuresDirectory, "fig2_sdm_signal_recovery.png")
figureSdm.savefig(figureSdmPath, dpi=300)
plt.close(figureSdm)

ebN0DbArray = np.arange(0, 26, 2, dtype=float)
ebN0LinearArray = 10.0**(ebN0DbArray / 10.0)
numSnrEvaluationPoints = len(ebN0DbArray)

numMonteCarloBits = 200000

berSimSiso = np.zeros(numSnrEvaluationPoints)
berSimSimoSc = np.zeros(numSnrEvaluationPoints)
berSimSimoMrc = np.zeros(numSnrEvaluationPoints)
berSimMisoAlamouti = np.zeros(numSnrEvaluationPoints)
berSimMimoAlamouti = np.zeros(numSnrEvaluationPoints)

berTheorySiso = np.zeros(numSnrEvaluationPoints)
berTheorySimoSc = np.zeros(numSnrEvaluationPoints)
berTheorySimoMrc = np.zeros(numSnrEvaluationPoints)
berTheoryMisoAlamouti = np.zeros(numSnrEvaluationPoints)
berTheoryMimoAlamouti = np.zeros(numSnrEvaluationPoints)

np.random.seed(42)

for pointIndex, (snrDb, snrLinear) in enumerate(zip(ebN0DbArray, ebN0LinearArray)):
    noiseVariance = 1.0 / snrLinear
    noiseStdDev = np.sqrt(noiseVariance / 2.0)

    bitsStream = np.random.randint(0, 2, numMonteCarloBits)
    bpskSignals = 2.0 * bitsStream - 1.0

    hSisoChannel = (np.random.randn(numMonteCarloBits) + 1j * np.random.randn(numMonteCarloBits)) / np.sqrt(2.0)
    noiseSisoChannel = noiseStdDev * (np.random.randn(numMonteCarloBits) + 1j * np.random.randn(numMonteCarloBits))
    rxSisoChannel = hSisoChannel * bpskSignals + noiseSisoChannel
    equalizedSisoChannel = rxSisoChannel * np.conj(hSisoChannel)
    detectedSisoBits = (equalizedSisoChannel.real >= 0).astype(int)
    berSimSiso[pointIndex] = np.mean(detectedSisoBits != bitsStream)

    hSimoChannel1 = (np.random.randn(numMonteCarloBits) + 1j * np.random.randn(numMonteCarloBits)) / np.sqrt(2.0)
    hSimoChannel2 = (np.random.randn(numMonteCarloBits) + 1j * np.random.randn(numMonteCarloBits)) / np.sqrt(2.0)
    noiseSimo1 = noiseStdDev * (np.random.randn(numMonteCarloBits) + 1j * np.random.randn(numMonteCarloBits))
    noiseSimo2 = noiseStdDev * (np.random.randn(numMonteCarloBits) + 1j * np.random.randn(numMonteCarloBits))
    rxSimo1 = hSimoChannel1 * bpskSignals + noiseSimo1
    rxSimo2 = hSimoChannel2 * bpskSignals + noiseSimo2

    selectMaskBranch1 = (np.abs(hSimoChannel1)**2 >= np.abs(hSimoChannel2)**2)
    equalizedSimoSc = np.where(selectMaskBranch1, rxSimo1 * np.conj(hSimoChannel1), rxSimo2 * np.conj(hSimoChannel2))
    detectedSimoScBits = (equalizedSimoSc.real >= 0).astype(int)
    berSimSimoSc[pointIndex] = np.mean(detectedSimoScBits != bitsStream)

    equalizedSimoMrc = rxSimo1 * np.conj(hSimoChannel1) + rxSimo2 * np.conj(hSimoChannel2)
    detectedSimoMrcBits = (equalizedSimoMrc.real >= 0).astype(int)
    berSimSimoMrc[pointIndex] = np.mean(detectedSimoMrcBits != bitsStream)

    numStbcBlocks = numMonteCarloBits // 2
    symbolPairsS0 = bpskSignals[0::2]
    symbolPairsS1 = bpskSignals[1::2]
    scaledTxS0 = symbolPairsS0 / np.sqrt(2.0)
    scaledTxS1 = symbolPairsS1 / np.sqrt(2.0)

    hMisoAntenna1 = (np.random.randn(numStbcBlocks) + 1j * np.random.randn(numStbcBlocks)) / np.sqrt(2.0)
    hMisoAntenna2 = (np.random.randn(numStbcBlocks) + 1j * np.random.randn(numStbcBlocks)) / np.sqrt(2.0)
    noiseMisoTimeSlot1 = noiseStdDev * (np.random.randn(numStbcBlocks) + 1j * np.random.randn(numStbcBlocks))
    noiseMisoTimeSlot2 = noiseStdDev * (np.random.randn(numStbcBlocks) + 1j * np.random.randn(numStbcBlocks))

    rxMisoTimeSlot1 = hMisoAntenna1 * scaledTxS0 + hMisoAntenna2 * scaledTxS1 + noiseMisoTimeSlot1
    rxMisoTimeSlot2 = -hMisoAntenna1 * np.conj(scaledTxS1) + hMisoAntenna2 * np.conj(scaledTxS0) + noiseMisoTimeSlot2

    combinedMisoS0 = np.conj(hMisoAntenna1) * rxMisoTimeSlot1 + hMisoAntenna2 * np.conj(rxMisoTimeSlot2)
    combinedMisoS1 = np.conj(hMisoAntenna2) * rxMisoTimeSlot1 - hMisoAntenna1 * np.conj(rxMisoTimeSlot2)

    detectedMisoBits = np.zeros(numMonteCarloBits, dtype=int)
    detectedMisoBits[0::2] = (combinedMisoS0.real >= 0).astype(int)
    detectedMisoBits[1::2] = (combinedMisoS1.real >= 0).astype(int)
    berSimMisoAlamouti[pointIndex] = np.mean(detectedMisoBits != bitsStream)

    hMimo11 = (np.random.randn(numStbcBlocks) + 1j * np.random.randn(numStbcBlocks)) / np.sqrt(2.0)
    hMimo12 = (np.random.randn(numStbcBlocks) + 1j * np.random.randn(numStbcBlocks)) / np.sqrt(2.0)
    hMimo21 = (np.random.randn(numStbcBlocks) + 1j * np.random.randn(numStbcBlocks)) / np.sqrt(2.0)
    hMimo22 = (np.random.randn(numStbcBlocks) + 1j * np.random.randn(numStbcBlocks)) / np.sqrt(2.0)

    noiseMimoRx1Time1 = noiseStdDev * (np.random.randn(numStbcBlocks) + 1j * np.random.randn(numStbcBlocks))
    noiseMimoRx1Time2 = noiseStdDev * (np.random.randn(numStbcBlocks) + 1j * np.random.randn(numStbcBlocks))
    noiseMimoRx2Time1 = noiseStdDev * (np.random.randn(numStbcBlocks) + 1j * np.random.randn(numStbcBlocks))
    noiseMimoRx2Time2 = noiseStdDev * (np.random.randn(numStbcBlocks) + 1j * np.random.randn(numStbcBlocks))

    rxMimoRx1Time1 = hMimo11 * scaledTxS0 + hMimo12 * scaledTxS1 + noiseMimoRx1Time1
    rxMimoRx1Time2 = -hMimo11 * np.conj(scaledTxS1) + hMimo12 * np.conj(scaledTxS0) + noiseMimoRx1Time2
    rxMimoRx2Time1 = hMimo21 * scaledTxS0 + hMimo22 * scaledTxS1 + noiseMimoRx2Time1
    rxMimoRx2Time2 = -hMimo21 * np.conj(scaledTxS1) + hMimo22 * np.conj(scaledTxS0) + noiseMimoRx2Time2

    combinedMimoS0 = np.conj(hMimo11) * rxMimoRx1Time1 + hMimo12 * np.conj(rxMimoRx1Time2) + \
                     np.conj(hMimo21) * rxMimoRx2Time1 + hMimo22 * np.conj(rxMimoRx2Time2)

    combinedMimoS1 = np.conj(hMimo12) * rxMimoRx1Time1 - hMimo11 * np.conj(rxMimoRx1Time2) + \
                     np.conj(hMimo22) * rxMimoRx2Time1 - hMimo21 * np.conj(rxMimoRx2Time2)

    detectedMimoBits = np.zeros(numMonteCarloBits, dtype=int)
    detectedMimoBits[0::2] = (combinedMimoS0.real >= 0).astype(int)
    detectedMimoBits[1::2] = (combinedMimoS1.real >= 0).astype(int)
    berSimMimoAlamouti[pointIndex] = np.mean(detectedMimoBits != bitsStream)

    gammaSiso = snrLinear
    berTheorySiso[pointIndex] = 0.5 * (1.0 - np.sqrt(gammaSiso / (1.0 + gammaSiso)))

    gammaSimoSc = snrLinear
    berTheorySimoSc[pointIndex] = 0.5 - np.sqrt(gammaSimoSc / (1.0 + gammaSimoSc)) + 0.5 * np.sqrt(gammaSimoSc / (2.0 + gammaSimoSc))

    gammaSimoMrc = snrLinear
    muMrc = np.sqrt(gammaSimoMrc / (1.0 + gammaSimoMrc))
    berTheorySimoMrc[pointIndex] = ((1.0 - muMrc) / 2.0)**2 * (2.0 + muMrc)

    gammaMiso = snrLinear / 2.0
    muMiso = np.sqrt(gammaMiso / (1.0 + gammaMiso))
    berTheoryMisoAlamouti[pointIndex] = ((1.0 - muMiso) / 2.0)**2 * (2.0 + muMiso)

    gammaMimo = snrLinear / 2.0
    muMimo = np.sqrt(gammaMimo / (1.0 + gammaMimo))
    pVal = (1.0 + muMimo) / 2.0
    qVal = (1.0 - muMimo) / 2.0
    berTheoryMimoAlamouti[pointIndex] = (qVal**4) * (1.0 + 4.0 * pVal + 10.0 * (pVal**2) + 20.0 * (pVal**3))

figureBer, axBer = plt.subplots(figsize=(10, 7), dpi=300)

axBer.semilogy(ebN0DbArray, berTheorySiso, color="black", linestyle="-", linewidth=2.0, label="SISO Rayleigh Theoretical (d=1)")
axBer.semilogy(ebN0DbArray, berSimSiso, color="black", linestyle="None", marker="o", markersize=6, label="SISO Monte Carlo")

axBer.semilogy(ebN0DbArray, berTheorySimoSc, color="magenta", linestyle="--", linewidth=1.8, label="SIMO 1x2 SC Theoretical (d=2)")
axBer.semilogy(ebN0DbArray, berSimSimoSc, color="magenta", linestyle="None", marker="s", markersize=5, label="SIMO 1x2 SC Monte Carlo")

axBer.semilogy(ebN0DbArray, berTheorySimoMrc, color="blue", linestyle="--", linewidth=1.8, label="SIMO 1x2 MRC Theoretical (d=2)")
axBer.semilogy(ebN0DbArray, berSimSimoMrc, color="blue", linestyle="None", marker="^", markersize=5, label="SIMO 1x2 MRC Monte Carlo")

axBer.semilogy(ebN0DbArray, berTheoryMisoAlamouti, color="red", linestyle="-.", linewidth=1.8, label="MISO 2x1 Alamouti Theoretical (d=2)")
axBer.semilogy(ebN0DbArray, berSimMisoAlamouti, color="red", linestyle="None", marker="d", markersize=5, label="MISO 2x1 Alamouti Monte Carlo")

axBer.semilogy(ebN0DbArray, berTheoryMimoAlamouti, color="forestgreen", linestyle="-", linewidth=2.2, label="MIMO 2x2 Alamouti Theoretical (d=4)")
axBer.semilogy(ebN0DbArray, berSimMimoAlamouti, color="forestgreen", linestyle="None", marker="x", markersize=7, markeredgewidth=2, label="MIMO 2x2 Alamouti Monte Carlo")

axBer.set_xlim(0, 25)
axBer.set_ylim(1e-6, 1.0)
axBer.set_xlabel("E_b/N_0 (dB)", fontsize=13, fontweight="bold")
axBer.set_ylabel("Bit Error Rate (BER)", fontsize=13, fontweight="bold")
axBer.set_title("BER Performance vs E_b/N_0 for Diversity Techniques in Rayleigh Fading", fontsize=13, fontweight="bold")
axBer.grid(True, which="both", linestyle="--", alpha=0.5)

axBer.annotate("Diversity Order d = 1\n(SISO)", xy=(18, 4e-3), xytext=(19, 2e-2),
               arrowprops=dict(arrowstyle="->", color="black", lw=1.2), fontsize=9, fontweight="bold")
axBer.annotate("Diversity Order d = 2\n(SIMO MRC & MISO Alamouti)", xy=(14, 5e-4), xytext=(15, 3e-3),
               arrowprops=dict(arrowstyle="->", color="blue", lw=1.2), fontsize=9, fontweight="bold")
axBer.annotate("Diversity Order d = 4\n(MIMO 2x2 Alamouti)", xy=(10, 1.5e-4), xytext=(12, 1e-4),
               arrowprops=dict(arrowstyle="->", color="forestgreen", lw=1.2), fontsize=9, fontweight="bold")

axBer.legend(loc="lower left", fontsize=8.5, framealpha=0.95)
figureBer.tight_layout()
figureBerPath = os.path.join(figuresDirectory, "fig3_ber_diversity_comparison.png")
figureBer.savefig(figureBerPath, dpi=300)
plt.close(figureBer)

snrCapacityDbArray = np.arange(-10, 32, 2, dtype=float)
snrCapacityLinearArray = 10.0**(snrCapacityDbArray / 10.0)
numCapacityPoints = len(snrCapacityDbArray)

capacitySisoAwgn = np.log2(1.0 + snrCapacityLinearArray)

eigenvaluesFixedH = (la.svd(channelMatrixH)[1])**2
noiseFloorFixed1 = 1.0 / eigenvaluesFixedH[0]
noiseFloorFixed2 = 1.0 / eigenvaluesFixedH[1]

capacityFixedH_Epa = np.zeros(numCapacityPoints)
capacityFixedH_Wf = np.zeros(numCapacityPoints)
powerRatioFixed1 = np.zeros(numCapacityPoints)
powerRatioFixed2 = np.zeros(numCapacityPoints)

for capIndex, snrLin in enumerate(snrCapacityLinearArray):
    capacityFixedH_Epa[capIndex] = np.sum(np.log2(1.0 + (snrLin / 2.0) * eigenvaluesFixedH))

    if snrLin <= (noiseFloorFixed2 - noiseFloorFixed1):
        allocP1 = snrLin
        allocP2 = 0.0
    else:
        waterLevel = (snrLin + noiseFloorFixed1 + noiseFloorFixed2) / 2.0
        allocP1 = waterLevel - noiseFloorFixed1
        allocP2 = waterLevel - noiseFloorFixed2

    powerRatioFixed1[capIndex] = allocP1 / snrLin
    powerRatioFixed2[capIndex] = allocP2 / snrLin
    capacityFixedH_Wf[capIndex] = np.log2(1.0 + allocP1 * eigenvaluesFixedH[0]) + np.log2(1.0 + allocP2 * eigenvaluesFixedH[1])

numErgodicTrials = 10000
capacityErgodicSiso = np.zeros(numCapacityPoints)
capacityErgodicMimoEpa = np.zeros(numCapacityPoints)
capacityErgodicMimoWf = np.zeros(numCapacityPoints)

np.random.seed(123)

for trialIndex in range(numErgodicTrials):
    hScalarTrial = (np.random.randn() + 1j * np.random.randn()) / np.sqrt(2.0)
    gainScalarTrial = np.abs(hScalarTrial)**2

    hMimoTrial = (np.random.randn(2, 2) + 1j * np.random.randn(2, 2)) / np.sqrt(2.0)
    eigenvaluesTrial = (la.svd(hMimoTrial)[1])**2
    noiseTrialLevels = 1.0 / eigenvaluesTrial

    for capIndex, snrLin in enumerate(snrCapacityLinearArray):
        capacityErgodicSiso[capIndex] += np.log2(1.0 + snrLin * gainScalarTrial)
        capacityErgodicMimoEpa[capIndex] += np.sum(np.log2(1.0 + (snrLin / 2.0) * eigenvaluesTrial))

        if snrLin <= (noiseTrialLevels[1] - noiseTrialLevels[0]):
            pTrial1 = snrLin
            pTrial2 = 0.0
        else:
            waterLevelTrial = (snrLin + noiseTrialLevels[0] + noiseTrialLevels[1]) / 2.0
            pTrial1 = waterLevelTrial - noiseTrialLevels[0]
            pTrial2 = waterLevelTrial - noiseTrialLevels[1]

        capacityErgodicMimoWf[capIndex] += np.log2(1.0 + pTrial1 * eigenvaluesTrial[0]) + np.log2(1.0 + pTrial2 * eigenvaluesTrial[1])

capacityErgodicSiso /= numErgodicTrials
capacityErgodicMimoEpa /= numErgodicTrials
capacityErgodicMimoWf /= numErgodicTrials

figureCap, axCap = plt.subplots(figsize=(10, 6.5), dpi=300)

axCap.plot(snrCapacityDbArray, capacitySisoAwgn, color="black", linestyle="--", linewidth=1.8, label="SISO AWGN Shannon Limit")
axCap.plot(snrCapacityDbArray, capacityErgodicSiso, color="gray", linestyle=":", linewidth=2.0, label="SISO Rayleigh Ergodic Capacity")

axCap.plot(snrCapacityDbArray, capacityFixedH_Epa, color="mediumblue", linestyle="--", linewidth=1.8, label="MIMO 2x2 Fixed H (Equal Power)")
axCap.plot(snrCapacityDbArray, capacityFixedH_Wf, color="mediumblue", linestyle="-", linewidth=2.2, label="MIMO 2x2 Fixed H (Water-filling)")

axCap.plot(snrCapacityDbArray, capacityErgodicMimoEpa, color="crimson", linestyle="--", linewidth=1.8, label="MIMO 2x2 Rayleigh Ergodic (Equal Power)")
axCap.plot(snrCapacityDbArray, capacityErgodicMimoWf, color="crimson", linestyle="-", linewidth=2.2, label="MIMO 2x2 Rayleigh Ergodic (Water-filling)")

axCap.set_xlim(-10, 30)
axCap.set_ylim(0, 20)
axCap.set_xlabel("Signal-to-Noise Ratio SNR (dB)", fontsize=13, fontweight="bold")
axCap.set_ylabel("Spectral Efficiency / Capacity (bps/Hz)", fontsize=13, fontweight="bold")
axCap.set_title("MIMO 2x2 SDM Shannon Capacity vs SNR under Various Power Allocation Strategies", fontsize=13, fontweight="bold")
axCap.grid(True, linestyle="--", alpha=0.5)

axCap.annotate("Multiplexing Gain = 2\n(Slope: 2 bps/Hz per 3 dB)", xy=(22, 13.5), xytext=(12, 16.0),
               arrowprops=dict(arrowstyle="->", color="crimson", lw=1.3), fontsize=9.5, fontweight="bold")

axCap.annotate("Water-filling Power Gain\nat Low SNR", xy=(-4, 1.2), xytext=(-8, 4.5),
               arrowprops=dict(arrowstyle="->", color="mediumblue", lw=1.3), fontsize=9.5, fontweight="bold")

axCap.legend(loc="upper left", fontsize=9.5, framealpha=0.95)
figureCap.tight_layout()
figureCapPath = os.path.join(figuresDirectory, "fig4_capacity_sdm_comparison.png")
figureCap.savefig(figureCapPath, dpi=300)
plt.close(figureCap)

figureWf, axesWf = plt.subplots(1, 3, figsize=(16, 5), dpi=300)

subchannelIndices = [1, 2]
noiseDepths = [noiseFloorFixed1, noiseFloorFixed2]
snrDemoLowLinear = 5.0
pLow1 = snrDemoLowLinear
pLow2 = 0.0

barWidth = 0.55
axesWf[0].bar(subchannelIndices, noiseDepths, width=barWidth, color="#b0bec5", edgecolor="black", label="1 / sigma_i^2 (Inverse Channel Gain)")
axesWf[0].bar(subchannelIndices, [pLow1, pLow2], bottom=noiseDepths, width=barWidth, color="#42a5f5", edgecolor="black", label="Allocated Power p_i")
axesWf[0].axhline(noiseFloorFixed1 + pLow1, color="red", linestyle="--", linewidth=1.5, label="Water Level mu")
axesWf[0].set_xticks(subchannelIndices)
axesWf[0].set_xticklabels(["Subchannel 1\n(sigma_1^2 = 1.011)", "Subchannel 2\n(sigma_2^2 = 0.089)"], fontsize=9.5)
axesWf[0].set_ylabel("Level (Power + 1/sigma^2)", fontsize=10)
axesWf[0].set_title(f"Water-filling at Low SNR ({10*np.log10(snrDemoLowLinear):.1f} dB)\nOnly Strong Mode Activated", fontsize=10.5, fontweight="bold")
axesWf[0].set_ylim(0, 16)
axesWf[0].grid(True, axis="y")
axesWf[0].legend(loc="upper left", fontsize=8.5)

thresholdSnrFixedDb = 10.0 * np.log10(noiseFloorFixed2 - noiseFloorFixed1)

axesWf[1].plot(snrCapacityDbArray, powerRatioFixed1 * 100.0, color="#1976d2", linewidth=2.2, label="Subchannel 1 Power Ratio (p1 / P_total)")
axesWf[1].plot(snrCapacityDbArray, powerRatioFixed2 * 100.0, color="#d32f2f", linewidth=2.2, label="Subchannel 2 Power Ratio (p2 / P_total)")
axesWf[1].axvline(thresholdSnrFixedDb, color="black", linestyle="--", linewidth=1.2, label=f"Threshold SNR = {thresholdSnrFixedDb:.1f} dB")
axesWf[1].axhline(50.0, color="gray", linestyle=":", linewidth=1.0)
axesWf[1].set_xlim(-10, 30)
axesWf[1].set_ylim(-5, 105)
axesWf[1].set_xlabel("Total SNR (dB)", fontsize=10)
axesWf[1].set_ylabel("Power Allocation Percentage (%)", fontsize=10)
axesWf[1].set_title("Power Allocation Percentage vs SNR\nfor Fixed Channel H", fontsize=10.5, fontweight="bold")
axesWf[1].grid(True)
axesWf[1].legend(loc="center right", fontsize=8.5)

capacityDifferenceFixed = capacityFixedH_Wf - capacityFixedH_Epa
capacityDifferenceErgodic = capacityErgodicMimoWf - capacityErgodicMimoEpa

axesWf[2].plot(snrCapacityDbArray, capacityDifferenceFixed, color="blue", linewidth=2.0, label="Fixed Channel (C_WF - C_EPA)")
axesWf[2].plot(snrCapacityDbArray, capacityDifferenceErgodic, color="red", linewidth=2.0, label="Rayleigh Ergodic (C_WF - C_EPA)")
axesWf[2].set_xlim(-10, 30)
axesWf[2].set_xlabel("Total SNR (dB)", fontsize=10)
axesWf[2].set_ylabel("Capacity Gain (bps/Hz)", fontsize=10)
axesWf[2].set_title("Water-filling Gain over Equal Power\n(C_WF - C_EPA) vs SNR", fontsize=10.5, fontweight="bold")
axesWf[2].grid(True)
axesWf[2].legend(loc="upper right", fontsize=8.5)

figureWf.suptitle("Comprehensive Water-Filling Power Allocation Dynamics in MIMO 2x2", fontsize=13, fontweight="bold")
figureWf.tight_layout()
figureWfPath = os.path.join(figuresDirectory, "fig5_waterfilling_allocation.png")
figureWf.savefig(figureWfPath, dpi=300)
plt.close(figureWf)

print("=" * 80)
print("              MIMO 2x2 STBC & SDM SIMULATION VERIFICATION REPORT                ")
print("=" * 80)
print(f"1. STBC Step-by-Step Recovery:")
print(f"   Transmitted: s0 = {s0:.4f}, s1 = {s1:.4f}")
print(f"   Received:    r0 = {receivedSignalR0:.4f}, r1 = {receivedSignalR1:.4f}")
print(f"                r2 = {receivedSignalR2:.4f}, r3 = {receivedSignalR3:.4f}")
print(f"   Combiner:    z0 = {combinerOutputZ0:.4f}, z1 = {combinerOutputZ1:.4f}")
print(f"   Recovered:   s_hat0 = {recoveredSymbolHatS0:.4f} (Err: {errorStbcS0:.2e})")
print(f"                s_hat1 = {recoveredSymbolHatS1:.4f} (Err: {errorStbcS1:.2e})")
print("-" * 80)
print("2. SDM Equalization & SVD Precoding (Norm Errors):")
print(f"   Zero-Forcing (ZF) Error: {errorNormZf:.2e}")
print(f"   MMSE (sigma=0) Error:    {errorNormMmse:.2e}")
print(f"   SVD Precoding Error:     {errorNormSvd:.2e}")
print("-" * 80)
print("3. BER Diversity Comparison (Selected SNR sample points):")
print(f"{'SNR(dB)':<8} | {'SISO Theo':<10} | {'SISO Sim':<10} | {'SIMO SC':<10} | {'SIMO MRC':<10} | {'MISO 2x1':<10} | {'MIMO 2x2 (Th/Sim)':<20}")
print("-" * 80)
for sampleIdx in range(0, numSnrEvaluationPoints, 2):
    snrVal = ebN0DbArray[sampleIdx]
    print(f"{snrVal:<8.1f} | {berTheorySiso[sampleIdx]:<10.2e} | {berSimSiso[sampleIdx]:<10.2e} | {berSimSimoSc[sampleIdx]:<10.2e} | {berSimSimoMrc[sampleIdx]:<10.2e} | {berSimMisoAlamouti[sampleIdx]:<10.2e} | {berTheoryMimoAlamouti[sampleIdx]:.2e} / {berSimMimoAlamouti[sampleIdx]:.2e}")
print("-" * 80)
print("4. MIMO 2x2 Capacity Comparison (bps/Hz):")
print(f"{'SNR(dB)':<8} | {'SISO AWGN':<10} | {'SISO Rayl':<10} | {'Fixed EPA':<10} | {'Fixed WF':<10} | {'Ergodic EPA':<12} | {'Ergodic WF':<12}")
print("-" * 80)
for sampleIdx in range(0, numCapacityPoints, 3):
    snrVal = snrCapacityDbArray[sampleIdx]
    print(f"{snrVal:<8.1f} | {capacitySisoAwgn[sampleIdx]:<10.3f} | {capacityErgodicSiso[sampleIdx]:<10.3f} | {capacityFixedH_Epa[sampleIdx]:<10.3f} | {capacityFixedH_Wf[sampleIdx]:<10.3f} | {capacityErgodicMimoEpa[sampleIdx]:<12.3f} | {capacityErgodicMimoWf[sampleIdx]:<12.3f}")
print("=" * 80)
print(f"Generated Figure 1: {figureStbcPath}")
print(f"Generated Figure 2: {figureSdmPath}")
print(f"Generated Figure 3: {figureBerPath}")
print(f"Generated Figure 4: {figureCapPath}")
print(f"Generated Figure 5: {figureWfPath}")
