clc;
clear;
close all;

ebN0DbValues = 0:2:25;
ebN0LinearValues = 10.^(ebN0DbValues / 10);
numSnrPoints = length(ebN0DbValues);

numBits = 2e5;

berSimulatedSiso = zeros(1, numSnrPoints);
berSimulatedSimoSc = zeros(1, numSnrPoints);
berSimulatedSimoMrc = zeros(1, numSnrPoints);
berSimulatedMisoAlamouti = zeros(1, numSnrPoints);
berSimulatedMimoAlamouti = zeros(1, numSnrPoints);

berTheoreticalSiso = zeros(1, numSnrPoints);
berTheoreticalSimoSc = zeros(1, numSnrPoints);
berTheoreticalSimoMrc = zeros(1, numSnrPoints);
berTheoreticalMisoAlamouti = zeros(1, numSnrPoints);
berTheoreticalMimoAlamouti = zeros(1, numSnrPoints);

for snrIndex = 1:numSnrPoints
    snrLinear = ebN0LinearValues(snrIndex);
    noiseVariance = 1 / snrLinear;
    noiseStdDev = sqrt(noiseVariance / 2);

    dataBits = randi([0, 1], 1, numBits);
    bpskSymbols = 2 * dataBits - 1;

    hSiso = (randn(1, numBits) + 1i * randn(1, numBits)) / sqrt(2);
    noiseSiso = noiseStdDev * (randn(1, numBits) + 1i * randn(1, numBits));
    receivedSiso = hSiso .* bpskSymbols + noiseSiso;
    equalizedSiso = receivedSiso .* conj(hSiso);
    detectedBitsSiso = real(equalizedSiso) >= 0;
    berSimulatedSiso(snrIndex) = mean(detectedBitsSiso ~= dataBits);

    hSimo1 = (randn(1, numBits) + 1i * randn(1, numBits)) / sqrt(2);
    hSimo2 = (randn(1, numBits) + 1i * randn(1, numBits)) / sqrt(2);
    noiseSimo1 = noiseStdDev * (randn(1, numBits) + 1i * randn(1, numBits));
    noiseSimo2 = noiseStdDev * (randn(1, numBits) + 1i * randn(1, numBits));
    receivedSimo1 = hSimo1 .* bpskSymbols + noiseSimo1;
    receivedSimo2 = hSimo2 .* bpskSymbols + noiseSimo2;

    powerBranch1 = abs(hSimo1).^2;
    powerBranch2 = abs(hSimo2).^2;
    selectBranch1 = powerBranch1 >= powerBranch2;
    equalizedSimoSc = zeros(1, numBits);
    equalizedSimoSc(selectBranch1) = receivedSimo1(selectBranch1) .* conj(hSimo1(selectBranch1));
    equalizedSimoSc(~selectBranch1) = receivedSimo2(~selectBranch1) .* conj(hSimo2(~selectBranch1));
    detectedBitsSimoSc = real(equalizedSimoSc) >= 0;
    berSimulatedSimoSc(snrIndex) = mean(detectedBitsSimoSc ~= dataBits);

    equalizedSimoMrc = receivedSimo1 .* conj(hSimo1) + receivedSimo2 .* conj(hSimo2);
    detectedBitsSimoMrc = real(equalizedSimoMrc) >= 0;
    berSimulatedSimoMrc(snrIndex) = mean(detectedBitsSimoMrc ~= dataBits);

    numBlocks = numBits / 2;
    symbolPairs0 = bpskSymbols(1:2:end);
    symbolPairs1 = bpskSymbols(2:2:end);

    hMiso1 = (randn(1, numBlocks) + 1i * randn(1, numBlocks)) / sqrt(2);
    hMiso2 = (randn(1, numBlocks) + 1i * randn(1, numBlocks)) / sqrt(2);
    noiseMisoTime1 = noiseStdDev * (randn(1, numBlocks) + 1i * randn(1, numBlocks));
    noiseMisoTime2 = noiseStdDev * (randn(1, numBlocks) + 1i * randn(1, numBlocks));

    txScaled0 = symbolPairs0 / sqrt(2);
    txScaled1 = symbolPairs1 / sqrt(2);

    rxMisoTime1 = hMiso1 .* txScaled0 + hMiso2 .* txScaled1 + noiseMisoTime1;
    rxMisoTime2 = -hMiso1 .* conj(txScaled1) + hMiso2 .* conj(txScaled0) + noiseMisoTime2;

    combinedMiso0 = conj(hMiso1) .* rxMisoTime1 + hMiso2 .* conj(rxMisoTime2);
    combinedMiso1 = conj(hMiso2) .* rxMisoTime1 - hMiso1 .* conj(rxMisoTime2);

    detectedBitsMiso0 = real(combinedMiso0) >= 0;
    detectedBitsMiso1 = real(combinedMiso1) >= 0;
    detectedBitsMiso = zeros(1, numBits);
    detectedBitsMiso(1:2:end) = detectedBitsMiso0;
    detectedBitsMiso(2:2:end) = detectedBitsMiso1;
    berSimulatedMisoAlamouti(snrIndex) = mean(detectedBitsMiso ~= dataBits);

    hMimo11 = (randn(1, numBlocks) + 1i * randn(1, numBlocks)) / sqrt(2);
    hMimo12 = (randn(1, numBlocks) + 1i * randn(1, numBlocks)) / sqrt(2);
    hMimo21 = (randn(1, numBlocks) + 1i * randn(1, numBlocks)) / sqrt(2);
    hMimo22 = (randn(1, numBlocks) + 1i * randn(1, numBlocks)) / sqrt(2);

    noiseMimoRx1Time1 = noiseStdDev * (randn(1, numBlocks) + 1i * randn(1, numBlocks));
    noiseMimoRx1Time2 = noiseStdDev * (randn(1, numBlocks) + 1i * randn(1, numBlocks));
    noiseMimoRx2Time1 = noiseStdDev * (randn(1, numBlocks) + 1i * randn(1, numBlocks));
    noiseMimoRx2Time2 = noiseStdDev * (randn(1, numBlocks) + 1i * randn(1, numBlocks));

    rxMimo1Time1 = hMimo11 .* txScaled0 + hMimo12 .* txScaled1 + noiseMimoRx1Time1;
    rxMimo1Time2 = -hMimo11 .* conj(txScaled1) + hMimo12 .* conj(txScaled0) + noiseMimoRx1Time2;
    rxMimo2Time1 = hMimo21 .* txScaled0 + hMimo22 .* txScaled1 + noiseMimoRx2Time1;
    rxMimo2Time2 = -hMimo21 .* conj(txScaled1) + hMimo22 .* conj(txScaled0) + noiseMimoRx2Time2;

    combinedMimo0 = conj(hMimo11) .* rxMimo1Time1 + hMimo12 .* conj(rxMimo1Time2) + ...
                    conj(hMimo21) .* rxMimo2Time1 + hMimo22 .* conj(rxMimo2Time2);
    combinedMimo1 = conj(hMimo12) .* rxMimo1Time1 - hMimo11 .* conj(rxMimo1Time2) + ...
                    conj(hMimo22) .* rxMimo2Time1 - hMimo21 .* conj(rxMimo2Time2);

    detectedBitsMimo0 = real(combinedMimo0) >= 0;
    detectedBitsMimo1 = real(combinedMimo1) >= 0;
    detectedBitsMimo = zeros(1, numBits);
    detectedBitsMimo(1:2:end) = detectedBitsMimo0;
    detectedBitsMimo(2:2:end) = detectedBitsMimo1;
    berSimulatedMimoAlamouti(snrIndex) = mean(detectedBitsMimo ~= dataBits);

    gammaSiso = snrLinear;
    berTheoreticalSiso(snrIndex) = 0.5 * (1 - sqrt(gammaSiso / (1 + gammaSiso)));

    gammaSimoSc = snrLinear;
    berTheoreticalSimoSc(snrIndex) = 0.5 - sqrt(gammaSimoSc / (1 + gammaSimoSc)) + 0.5 * sqrt(gammaSimoSc / (2 + gammaSimoSc));

    gammaSimoMrc = snrLinear;
    muMrc = sqrt(gammaSimoMrc / (1 + gammaSimoMrc));
    berTheoreticalSimoMrc(snrIndex) = ((1 - muMrc) / 2)^2 * (2 + muMrc);

    gammaMiso = snrLinear / 2;
    muMiso = sqrt(gammaMiso / (1 + gammaMiso));
    berTheoreticalMisoAlamouti(snrIndex) = ((1 - muMiso) / 2)^2 * (2 + muMiso);

    gammaMimo = snrLinear / 2;
    muMimo = sqrt(gammaMimo / (1 + gammaMimo));
    pMimo = (1 + muMimo) / 2;
    qMimo = (1 - muMimo) / 2;
    berTheoreticalMimoAlamouti(snrIndex) = (qMimo^4) * (1 + 4 * pMimo + 10 * pMimo^2 + 20 * pMimo^3);
end

figureVisibility = 'off';
if feature('ShowFigureWindows')
    figureVisibility = 'on';
end

figHandle = figure('Name', 'BER Comparison of Diversity Schemes', 'Color', 'w', 'Visible', figureVisibility);
semilogy(ebN0DbValues, berTheoreticalSiso, 'k-', 'LineWidth', 1.8); hold on;
semilogy(ebN0DbValues, berSimulatedSiso, 'ko', 'LineWidth', 1.2, 'MarkerSize', 6);

semilogy(ebN0DbValues, berTheoreticalSimoSc, 'm--', 'LineWidth', 1.8);
semilogy(ebN0DbValues, berSimulatedSimoSc, 'ms', 'LineWidth', 1.2, 'MarkerSize', 6);

semilogy(ebN0DbValues, berTheoreticalSimoMrc, 'b--', 'LineWidth', 1.8);
semilogy(ebN0DbValues, berSimulatedSimoMrc, 'b^', 'LineWidth', 1.2, 'MarkerSize', 6);

semilogy(ebN0DbValues, berTheoreticalMisoAlamouti, 'r-.', 'LineWidth', 1.8);
semilogy(ebN0DbValues, berSimulatedMisoAlamouti, 'rd', 'LineWidth', 1.2, 'MarkerSize', 6);

semilogy(ebN0DbValues, berTheoreticalMimoAlamouti, 'g-', 'LineWidth', 2.0);
semilogy(ebN0DbValues, berSimulatedMimoAlamouti, 'gx', 'LineWidth', 1.5, 'MarkerSize', 8);

grid on;
set(gca, 'YScale', 'log', 'FontSize', 12);
ylim([1e-6, 1]);
xlim([0, 25]);
xlabel('E_b/N_0 (dB)', 'FontSize', 14, 'FontWeight', 'bold');
ylabel('Bit Error Rate (BER)', 'FontSize', 14, 'FontWeight', 'bold');
title('BER vs E_b/N_0 for Various Diversity Schemes in Rayleigh Fading', 'FontSize', 14, 'FontWeight', 'bold');
legend({'SISO Theoretical', 'SISO Monte Carlo', ...
        'SIMO 1x2 SC Theoretical', 'SIMO 1x2 SC Monte Carlo', ...
        'SIMO 1x2 MRC Theoretical', 'SIMO 1x2 MRC Monte Carlo', ...
        'MISO 2x1 Alamouti Theoretical', 'MISO 2x1 Alamouti Monte Carlo', ...
        'MIMO 2x2 Alamouti Theoretical', 'MIMO 2x2 Alamouti Monte Carlo'}, ...
        'Location', 'southwest', 'FontSize', 10);

fprintf('========================================================================================\n');
fprintf('SNR(dB) | SISO Theo | SISO Sim  | SIMO SC   | SIMO MRC  | MISO 2x1  | MIMO 2x2 (Theo/Sim)\n');
fprintf('========================================================================================\n');
for i = 1:numSnrPoints
    fprintf('%7.1f | %9.2e | %9.2e | %9.2e | %9.2e | %9.2e | %9.2e / %9.2e\n', ...
        ebN0DbValues(i), berTheoreticalSiso(i), berSimulatedSiso(i), ...
        berSimulatedSimoSc(i), berSimulatedSimoMrc(i), berSimulatedMisoAlamouti(i), ...
        berTheoreticalMimoAlamouti(i), berSimulatedMimoAlamouti(i));
end
fprintf('========================================================================================\n');
