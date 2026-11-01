import os
import io
import runpy
from unittest.mock import patch


def assert_ber(sim, theo, n_bits, block_size=1):
    sim_arr, theo_arr = np.atleast_1d(sim), np.atleast_1d(theo)
    assert np.all((sim_arr >= 0.0) & (sim_arr <= 1.0) & np.isfinite(sim_arr))
    tolerance = 7.0 * np.sqrt(block_size * theo_arr * (1.0 - theo_arr) / n_bits) + block_size / n_bits
    assert np.all(np.abs(sim_arr - theo_arr) <= tolerance)

import numpy as np
import scipy.linalg as la

channelMatrixH = np.array([[0.7, 0.3], [0.4, 0.6]], dtype=complex)
symbolVectorX = np.array([1.0 + 1.0j, 1.0 - 1.0j], dtype=complex)

h11, h12 = channelMatrixH[0, 0], channelMatrixH[0, 1]
h21, h22 = channelMatrixH[1, 0], channelMatrixH[1, 1]

s0, s1 = symbolVectorX[0], symbolVectorX[1]

receivedSignalR0 = h11 * s0 + h12 * s1
receivedSignalR1 = -h11 * np.conj(s1) + h12 * np.conj(s0)
receivedSignalR2 = h21 * s0 + h22 * s1
receivedSignalR3 = -h21 * np.conj(s1) + h22 * np.conj(s0)

frobeniusNormSquaredH = np.abs(h11)**2 + np.abs(h12)**2 + np.abs(h21)**2 + np.abs(h22)**2

combinerOutputZ0 = np.conj(h11) * receivedSignalR0 + h12 * np.conj(receivedSignalR1) + np.conj(h21) * receivedSignalR2 + h22 * np.conj(receivedSignalR3)
combinerOutputZ1 = np.conj(h12) * receivedSignalR0 - h11 * np.conj(receivedSignalR1) + np.conj(h22) * receivedSignalR2 - h21 * np.conj(receivedSignalR3)

recoveredSymbolHatS0 = combinerOutputZ0 / frobeniusNormSquaredH
recoveredSymbolHatS1 = combinerOutputZ1 / frobeniusNormSquaredH

errorStbcS0 = float(np.abs(recoveredSymbolHatS0 - s0))
errorStbcS1 = float(np.abs(recoveredSymbolHatS1 - s1))

receivedVectorSdmY = channelMatrixH @ symbolVectorX

weightMatrixZf = la.pinv(channelMatrixH)
recoveredVectorZf = weightMatrixZf @ receivedVectorSdmY
errorNormZf = float(la.norm(recoveredVectorZf - symbolVectorX))

noiseVarianceSdm = 0.0
weightMatrixMmse = la.inv(channelMatrixH.conj().T @ channelMatrixH + noiseVarianceSdm * np.eye(2)) @ channelMatrixH.conj().T
recoveredVectorMmse = weightMatrixMmse @ receivedVectorSdmY
errorNormMmse = float(la.norm(recoveredVectorMmse - symbolVectorX))

leftSingularMatrixU, singularValuesS, rightSingularMatrixVh = la.svd(channelMatrixH)
unitaryMatrixV = rightSingularMatrixVh.conj().T
precodedVectorX = unitaryMatrixV @ symbolVectorX
receivedVectorSvd = channelMatrixH @ precodedVectorX
combinedVectorSvd = leftSingularMatrixU.conj().T @ receivedVectorSvd
recoveredVectorSvd = combinedVectorSvd / singularValuesS
errorNormSvd = float(la.norm(recoveredVectorSvd - symbolVectorX))

assert errorStbcS0 < 1e-12 and errorStbcS1 < 1e-12
assert errorNormZf < 1e-12
assert errorNormMmse < 1e-12
assert errorNormSvd < 1e-12

snrBerDbList = [0.0, 5.0, 10.0, 15.0, 20.0, 25.0]
numBitsSimulation = 500000

berResults = []
np.random.seed(42)

for snrDb in snrBerDbList:
    snrLin = 10.0**(snrDb / 10.0)
    noiseVar = 1.0 / snrLin
    noiseStd = np.sqrt(noiseVar / 2.0)

    pTheorySiso = 0.5 * (1.0 - np.sqrt(snrLin / (1.0 + snrLin)))

    pTheorySimoSc = 0.5 - np.sqrt(snrLin / (1.0 + snrLin)) + 0.5 * np.sqrt(snrLin / (2.0 + snrLin))

    muMrc = np.sqrt(snrLin / (1.0 + snrLin))
    pTheorySimoMrc = ((1.0 - muMrc) / 2.0)**2 * (2.0 + muMrc)

    gammaHalf = snrLin / 2.0
    muMiso = np.sqrt(gammaHalf / (1.0 + gammaHalf))
    pTheoryMiso = ((1.0 - muMiso) / 2.0)**2 * (2.0 + muMiso)

    muMimo = np.sqrt(gammaHalf / (1.0 + gammaHalf))
    pTheoryMimo = ((1.0 - muMimo) / 2.0)**4 * (
        1.0 + 4.0 * ((1.0 + muMimo) / 2.0) +
        10.0 * (((1.0 + muMimo) / 2.0)**2) +
        20.0 * (((1.0 + muMimo) / 2.0)**3)
    )

    bitsStream = np.random.randint(0, 2, numBitsSimulation)
    bpskSignals = 2.0 * bitsStream - 1.0

    hSiso = (np.random.randn(numBitsSimulation) + 1j * np.random.randn(numBitsSimulation)) / np.sqrt(2.0)
    nSiso = noiseStd * (np.random.randn(numBitsSimulation) + 1j * np.random.randn(numBitsSimulation))
    rxSiso = hSiso * bpskSignals + nSiso
    eqSiso = rxSiso * np.conj(hSiso)
    pSimSiso = float(np.mean((eqSiso.real >= 0).astype(int) != bitsStream))

    hSimo1 = (np.random.randn(numBitsSimulation) + 1j * np.random.randn(numBitsSimulation)) / np.sqrt(2.0)
    hSimo2 = (np.random.randn(numBitsSimulation) + 1j * np.random.randn(numBitsSimulation)) / np.sqrt(2.0)
    nSimo1 = noiseStd * (np.random.randn(numBitsSimulation) + 1j * np.random.randn(numBitsSimulation))
    nSimo2 = noiseStd * (np.random.randn(numBitsSimulation) + 1j * np.random.randn(numBitsSimulation))
    rxSimo1 = hSimo1 * bpskSignals + nSimo1
    rxSimo2 = hSimo2 * bpskSignals + nSimo2

    mask1 = (np.abs(hSimo1)**2 >= np.abs(hSimo2)**2)
    eqSimoSc = np.where(mask1, rxSimo1 * np.conj(hSimo1), rxSimo2 * np.conj(hSimo2))
    pSimSimoSc = float(np.mean((eqSimoSc.real >= 0).astype(int) != bitsStream))

    eqSimoMrc = rxSimo1 * np.conj(hSimo1) + rxSimo2 * np.conj(hSimo2)
    pSimSimoMrc = float(np.mean((eqSimoMrc.real >= 0).astype(int) != bitsStream))

    nStbcBlocks = numBitsSimulation // 2
    txPairsS0 = bpskSignals[0::2] / np.sqrt(2.0)
    txPairsS1 = bpskSignals[1::2] / np.sqrt(2.0)

    hMiso1 = (np.random.randn(nStbcBlocks) + 1j * np.random.randn(nStbcBlocks)) / np.sqrt(2.0)
    hMiso2 = (np.random.randn(nStbcBlocks) + 1j * np.random.randn(nStbcBlocks)) / np.sqrt(2.0)
    nMiso1 = noiseStd * (np.random.randn(nStbcBlocks) + 1j * np.random.randn(nStbcBlocks))
    nMiso2 = noiseStd * (np.random.randn(nStbcBlocks) + 1j * np.random.randn(nStbcBlocks))
    rxMiso1 = hMiso1 * txPairsS0 + hMiso2 * txPairsS1 + nMiso1
    rxMiso2 = -hMiso1 * np.conj(txPairsS1) + hMiso2 * np.conj(txPairsS0) + nMiso2
    combMiso0 = np.conj(hMiso1) * rxMiso1 + hMiso2 * np.conj(rxMiso2)
    combMiso1 = np.conj(hMiso2) * rxMiso1 - hMiso1 * np.conj(rxMiso2)
    detMisoBits = np.zeros(numBitsSimulation, dtype=int)
    detMisoBits[0::2] = (combMiso0.real >= 0).astype(int)
    detMisoBits[1::2] = (combMiso1.real >= 0).astype(int)
    pSimMiso = float(np.mean(detMisoBits != bitsStream))

    hM11 = (np.random.randn(nStbcBlocks) + 1j * np.random.randn(nStbcBlocks)) / np.sqrt(2.0)
    hM12 = (np.random.randn(nStbcBlocks) + 1j * np.random.randn(nStbcBlocks)) / np.sqrt(2.0)
    hM21 = (np.random.randn(nStbcBlocks) + 1j * np.random.randn(nStbcBlocks)) / np.sqrt(2.0)
    hM22 = (np.random.randn(nStbcBlocks) + 1j * np.random.randn(nStbcBlocks)) / np.sqrt(2.0)
    nM11 = noiseStd * (np.random.randn(nStbcBlocks) + 1j * np.random.randn(nStbcBlocks))
    nM12 = noiseStd * (np.random.randn(nStbcBlocks) + 1j * np.random.randn(nStbcBlocks))
    nM21 = noiseStd * (np.random.randn(nStbcBlocks) + 1j * np.random.randn(nStbcBlocks))
    nM22 = noiseStd * (np.random.randn(nStbcBlocks) + 1j * np.random.randn(nStbcBlocks))

    rxM11 = hM11 * txPairsS0 + hM12 * txPairsS1 + nM11
    rxM12 = -hM11 * np.conj(txPairsS1) + hM12 * np.conj(txPairsS0) + nM12
    rxM21 = hM21 * txPairsS0 + hM22 * txPairsS1 + nM21
    rxM22 = -hM21 * np.conj(txPairsS1) + hM22 * np.conj(txPairsS0) + nM22

    combM0 = np.conj(hM11) * rxM11 + hM12 * np.conj(rxM12) + np.conj(hM21) * rxM21 + hM22 * np.conj(rxM22)
    combM1 = np.conj(hM12) * rxM11 - hM11 * np.conj(rxM12) + np.conj(hM22) * rxM21 - hM21 * np.conj(rxM22)
    detMimoBits = np.zeros(numBitsSimulation, dtype=int)
    detMimoBits[0::2] = (combM0.real >= 0).astype(int)
    detMimoBits[1::2] = (combM1.real >= 0).astype(int)
    pSimMimo = float(np.mean(detMimoBits != bitsStream))

    berResults.append({
        "snrDb": snrDb,
        "sisoTheo": pTheorySiso,
        "sisoSim": pSimSiso,
        "simoScTheo": pTheorySimoSc,
        "simoSc": pSimSimoSc,
        "simoMrcTheo": pTheorySimoMrc,
        "simoMrc": pSimSimoMrc,
        "misoTheo": pTheoryMiso,
        "misoSim": pSimMiso,
        "mimoTheo": pTheoryMimo,
        "mimoSim": pSimMimo
    })

snrCapDbList = [-10.0, 0.0, 10.0, 20.0, 30.0]
eigenvaluesFixedH = (la.svd(channelMatrixH)[1])**2
noiseFloor1 = 1.0 / eigenvaluesFixedH[0]
noiseFloor2 = 1.0 / eigenvaluesFixedH[1]

numErgodicTrials = 15000
np.random.seed(123)

ergodicGainSiso = np.abs((np.random.randn(numErgodicTrials) + 1j * np.random.randn(numErgodicTrials)) / np.sqrt(2.0))**2

ergodicEigMimo = np.zeros((numErgodicTrials, 2))
for tIndex in range(numErgodicTrials):
    hTrial = (np.random.randn(2, 2) + 1j * np.random.randn(2, 2)) / np.sqrt(2.0)
    ergodicEigMimo[tIndex, :] = (la.svd(hTrial, compute_uv=False))**2

capResults = []

for snrDb in snrCapDbList:
    snrLin = 10.0**(snrDb / 10.0)

    capSisoAwgn = np.log2(1.0 + snrLin)
    capSisoRayl = np.mean(np.log2(1.0 + snrLin * ergodicGainSiso))

    capFixedEpa = np.sum(np.log2(1.0 + (snrLin / 2.0) * eigenvaluesFixedH))

    if snrLin <= (noiseFloor2 - noiseFloor1):
        p1 = snrLin
        p2 = 0.0
    else:
        w = (snrLin + noiseFloor1 + noiseFloor2) / 2.0
        p1 = w - noiseFloor1
        p2 = w - noiseFloor2
    capFixedWf = np.log2(1.0 + p1 * eigenvaluesFixedH[0]) + np.log2(1.0 + p2 * eigenvaluesFixedH[1])

    capErgEpa = np.mean(np.sum(np.log2(1.0 + (snrLin / 2.0) * ergodicEigMimo), axis=1))

    noiseFloorTrials = 1.0 / ergodicEigMimo
    trialThreshold = noiseFloorTrials[:, 1] - noiseFloorTrials[:, 0]
    maskLowSnr = (snrLin <= trialThreshold)

    pTrial1 = np.where(maskLowSnr, snrLin, (snrLin + noiseFloorTrials[:, 0] + noiseFloorTrials[:, 1]) / 2.0 - noiseFloorTrials[:, 0])
    pTrial2 = np.where(maskLowSnr, 0.0, (snrLin + noiseFloorTrials[:, 0] + noiseFloorTrials[:, 1]) / 2.0 - noiseFloorTrials[:, 1])

    capTrialWf = np.log2(1.0 + pTrial1 * ergodicEigMimo[:, 0]) + np.log2(1.0 + pTrial2 * ergodicEigMimo[:, 1])
    capErgWf = np.mean(capTrialWf)

    capResults.append({
        "snrDb": snrDb,
        "sisoAwgn": capSisoAwgn,
        "sisoRayl": capSisoRayl,
        "fixedEpa": capFixedEpa,
        "fixedWf": capFixedWf,
        "ergEpa": capErgEpa,
        "ergWf": capErgWf,
        "gain": capErgWf - capErgEpa
    })

for row in berResults:
    assert row["sisoTheo"] > 0
    assert row["mimoTheo"] > 0
    assert row["mimoTheo"] < row["sisoTheo"]
    for observed, expected, block_size in [("sisoSim", "sisoTheo", 1), ("simoSc", "simoScTheo", 1), ("simoMrc", "simoMrcTheo", 1), ("misoSim", "misoTheo", 2), ("mimoSim", "mimoTheo", 2)]:
        assert_ber(row[observed], row[expected], numBitsSimulation, block_size)

for i in range(len(berResults) - 1):
    assert berResults[i]["sisoTheo"] > berResults[i + 1]["sisoTheo"]
    assert berResults[i]["mimoTheo"] > berResults[i + 1]["mimoTheo"]

for row in capResults:
    assert row["fixedWf"] >= row["fixedEpa"] - 1e-9
    assert row["ergWf"] >= row["ergEpa"] - 1e-9

for i in range(len(capResults) - 1):
    assert capResults[i]["sisoAwgn"] < capResults[i + 1]["sisoAwgn"]
    assert capResults[i]["ergWf"] < capResults[i + 1]["ergWf"]

print("=" * 104)
print("                    MIMO 2x2 WIRELESS COMMUNICATIONS SIMULATION SUMMARY                   ")
print("=" * 104)
print("PART 1: STEP-BY-STEP SIGNAL RECOVERY VERIFICATION (Fixed H = [0.7 0.3; 0.4 0.6])")
print("-" * 104)
print("[STBC Alamouti 2x2]")
print(f"  Transmitted: s0 = {s0.real:+.4f} {s0.imag:+.4f}i, s1 = {s1.real:+.4f} {s1.imag:+.4f}i")
print(f"  Received:    r0 = {receivedSignalR0.real:+.4f} {receivedSignalR0.imag:+.4f}i, r1 = {receivedSignalR1.real:+.4f} {receivedSignalR1.imag:+.4f}i (Rx1)")
print(f"               r2 = {receivedSignalR2.real:+.4f} {receivedSignalR2.imag:+.4f}i, r3 = {receivedSignalR3.real:+.4f} {receivedSignalR3.imag:+.4f}i (Rx2)")
print(f"  Combiner:    z0 = {combinerOutputZ0.real:+.4f} {combinerOutputZ0.imag:+.4f}i, z1 = {combinerOutputZ1.real:+.4f} {combinerOutputZ1.imag:+.4f}i (Frobenius norm sq = {frobeniusNormSquaredH:.4f})")
print(f"  Recovered:   s_hat0 = {recoveredSymbolHatS0.real:+.4f} {recoveredSymbolHatS0.imag:+.4f}i, s_hat1 = {recoveredSymbolHatS1.real:+.4f} {recoveredSymbolHatS1.imag:+.4f}i")
print(f"  Errors:      |s_hat0 - s0| = {errorStbcS0:.2e}, |s_hat1 - s1| = {errorStbcS1:.2e} -> STATUS: PERFECT RECOVERY\n")

print("[SDM Multiplexing 2x2]")
print(f"  Zero-Forcing (ZF) Detection Error:         ||x_hat_ZF   - x|| = {errorNormZf:.2e} -> STATUS: PASSED")
print(f"  MMSE Detection (sigma=0) Error:            ||x_hat_MMSE - x|| = {errorNormMmse:.2e} -> STATUS: PASSED")
print(f"  SVD Precoding & Decoupling Error:          ||x_hat_SVD  - x|| = {errorNormSvd:.2e} -> STATUS: PASSED")
print("-" * 104)
print("PART 2: BIT ERROR RATE (BER) DIVERSITY COMPARISON AT KEY EVALUATION SNRs")
print("-" * 104)
print(" SNR(dB) | SISO Theo   | SISO Sim    | SIMO SC     | SIMO MRC    | MISO Theo   | MIMO 2x2 (Th / Sim) ")
print("---------+-------------+-------------+-------------+-------------+-------------+-----------------------")
for row in berResults:
    print(f" {row['snrDb']:4.0f} dB | {row['sisoTheo']:1.4e}  | {row['sisoSim']:1.4e}  | {row['simoSc']:1.4e}  | {row['simoMrc']:1.4e}  | {row['misoTheo']:1.4e}  | {row['mimoTheo']:1.4e} / {row['mimoSim']:1.4e}")
print("-" * 104)
print("PART 3: SHANNON CAPACITY & ERGODIC SPECTRAL EFFICIENCY (bps/Hz) AT KEY SNRs")
print("-" * 104)
print(" SNR(dB) | SISO AWGN   | SISO Rayl   | Fixed EPA   | Fixed WF    | Ergodic EPA | Ergodic WF  | Gain(WF-EPA)")
print("---------+-------------+-------------+-------------+-------------+-------------+-------------+-------------")
for row in capResults:
    print(f" {row['snrDb']:4.0f} dB | {row['sisoAwgn']:1.4f}      | {row['sisoRayl']:1.4f}      | {row['fixedEpa']:1.4f}      | {row['fixedWf']:1.4f}      | {row['ergEpa']:1.4f}      | {row['ergWf']:1.4f}      | +{row['gain']:1.4f}")
print("=" * 104)
prod_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mimo_full_simulation.py")
with patch("matplotlib.figure.Figure.savefig", lambda *args, **kwargs: None), patch("sys.stdout", new_callable=io.StringIO):
    prod = runpy.run_path(prod_path)
assert prod["numMonteCarloBits"] == 500000
assert np.all(np.isin(snrBerDbList, prod["ebN0DbArray"]))
assert np.all(np.isin(snrCapDbList, prod["snrCapacityDbArray"]))
for name in ["errorStbcS0", "errorStbcS1", "errorNormZf", "errorNormMmse", "errorNormSvd"]:
    assert prod[name] < 1e-12
assert np.allclose([prod["receivedSignalR0"], prod["receivedSignalR1"], prod["receivedSignalR2"], prod["receivedSignalR3"]], [receivedSignalR0, receivedSignalR1, receivedSignalR2, receivedSignalR3])
assert np.allclose([prod["recoveredSymbolHatS0"], prod["recoveredSymbolHatS1"]], [s0, s1])
for name in ["recoveredVectorZf", "recoveredVectorMmse", "recoveredVectorSvd"]:
    assert np.allclose(prod[name], symbolVectorX)
for row in berResults:
    b_idx = int(np.flatnonzero(prod["ebN0DbArray"] == row["snrDb"])[0])
    for name, key in [("Siso", "sisoTheo"), ("SimoSc", "simoScTheo"), ("SimoMrc", "simoMrcTheo"), ("MisoAlamouti", "misoTheo"), ("MimoAlamouti", "mimoTheo")]:
        assert np.isclose(prod["berTheory" + name][b_idx], row[key], rtol=1e-12, atol=1e-15)
for name, block_size in [("Siso", 1), ("SimoSc", 1), ("SimoMrc", 1), ("MisoAlamouti", 2), ("MimoAlamouti", 2)]:
    assert_ber(prod["berSim" + name], prod["berTheory" + name], prod["numMonteCarloBits"], block_size)
for row in capResults:
    c_idx = int(np.flatnonzero(prod["snrCapacityDbArray"] == row["snrDb"])[0])
    for name, key in [("capacitySisoAwgn", "sisoAwgn"), ("capacityFixedH_Epa", "fixedEpa"), ("capacityFixedH_Wf", "fixedWf")]:
        assert np.isclose(prod[name][c_idx], row[key], rtol=1e-12, atol=1e-15)
    for name, key in [("Siso", "sisoRayl"), ("MimoEpa", "ergEpa"), ("MimoWf", "ergWf")]:
        assert np.isclose(prod["capacityErgodic" + name][c_idx], row[key], rtol=0.03, atol=0.1)
assert np.allclose(prod["powerRatioFixed1"] + prod["powerRatioFixed2"], 1.0)
assert np.all(prod["powerRatioFixed1"] >= 0.0) and np.all(prod["powerRatioFixed2"] >= 0.0)
assert np.all(prod["capacityFixedH_Wf"] >= prod["capacityFixedH_Epa"] - 1e-9)
assert np.all(prod["capacityErgodicMimoWf"] >= prod["capacityErgodicMimoEpa"] - 1e-9)
print("[PRODUCTION AUDIT] Direct production recovery, all five BER modes, capacity references and power budgets verified.")
print("[WARN: STATISTICAL CEILING] Zero observed errors do not establish zero BER or validate tiny theoretical BER.")
print("[SIMULATION VERIFICATION COMPLETE] All 5 mathematical modules verified against analytical models.")
