clc;
clear;
close all;

snrDbValues = -10:2:30;
snrLinearValues = 10.^(snrDbValues / 10);
numSnrPoints = length(snrDbValues);

fixedH = [0.7, 0.3; 0.4, 0.6];
singularValuesFixed = svd(fixedH);
eigenvaluesFixed = singularValuesFixed.^2;

capacitySisoAwgn = log2(1 + snrLinearValues);

capacityFixedEpa = zeros(1, numSnrPoints);
capacityFixedWf = zeros(1, numSnrPoints);

powerAllocFixed1 = zeros(1, numSnrPoints);
powerAllocFixed2 = zeros(1, numSnrPoints);

noiseFloor1 = 1 / eigenvaluesFixed(1);
noiseFloor2 = 1 / eigenvaluesFixed(2);

for snrIndex = 1:numSnrPoints
    snrLinear = snrLinearValues(snrIndex);

    capacityFixedEpa(snrIndex) = sum(log2(1 + (snrLinear / 2) * eigenvaluesFixed));

    if snrLinear <= (noiseFloor2 - noiseFloor1)
        p1 = snrLinear;
        p2 = 0;
    else
        waterLevel = (snrLinear + noiseFloor1 + noiseFloor2) / 2;
        p1 = waterLevel - noiseFloor1;
        p2 = waterLevel - noiseFloor2;
    end
    powerAllocFixed1(snrIndex) = p1;
    powerAllocFixed2(snrIndex) = p2;
    capacityFixedWf(snrIndex) = log2(1 + p1 * eigenvaluesFixed(1)) + log2(1 + p2 * eigenvaluesFixed(2));
end

numRayleighRealizations = 5000;
capacityErgodicSiso = zeros(1, numSnrPoints);
capacityErgodicEpa = zeros(1, numSnrPoints);
capacityErgodicWf = zeros(1, numSnrPoints);

rng(123, 'twister');

for realizationIndex = 1:numRayleighRealizations
    hScalar = (randn + 1i * randn) / sqrt(2);
    channelGainSiso = abs(hScalar)^2;

    hMimo = (randn(2, 2) + 1i * randn(2, 2)) / sqrt(2);
    singularValuesMimo = svd(hMimo);
    eigenvaluesMimo = singularValuesMimo.^2;
    noiseLevels = 1 ./ eigenvaluesMimo;

    for snrIndex = 1:numSnrPoints
        snrLinear = snrLinearValues(snrIndex);

        capacityErgodicSiso(snrIndex) = capacityErgodicSiso(snrIndex) + log2(1 + snrLinear * channelGainSiso);

        capacityErgodicEpa(snrIndex) = capacityErgodicEpa(snrIndex) + sum(log2(1 + (snrLinear / 2) * eigenvaluesMimo));

        if snrLinear <= (noiseLevels(2) - noiseLevels(1))
            pAlloc1 = snrLinear;
            pAlloc2 = 0;
        else
            waterLevel = (snrLinear + noiseLevels(1) + noiseLevels(2)) / 2;
            pAlloc1 = waterLevel - noiseLevels(1);
            pAlloc2 = waterLevel - noiseLevels(2);
        end
        capacityInstantWf = log2(1 + pAlloc1 * eigenvaluesMimo(1)) + log2(1 + pAlloc2 * eigenvaluesMimo(2));
        capacityErgodicWf(snrIndex) = capacityErgodicWf(snrIndex) + capacityInstantWf;
    end
end

capacityErgodicSiso = capacityErgodicSiso / numRayleighRealizations;
capacityErgodicEpa = capacityErgodicEpa / numRayleighRealizations;
capacityErgodicWf = capacityErgodicWf / numRayleighRealizations;

figureVisibility = 'off';
if feature('ShowFigureWindows')
    figureVisibility = 'on';
end

figCapHandle = figure('Name', 'MIMO 2x2 vs SISO Capacity Comparison', 'Color', 'w', 'Visible', figureVisibility);
plot(snrDbValues, capacitySisoAwgn, 'k--', 'LineWidth', 1.8); hold on;
plot(snrDbValues, capacityErgodicSiso, 'k:', 'LineWidth', 2.0);
plot(snrDbValues, capacityFixedEpa, 'b--', 'LineWidth', 1.8);
plot(snrDbValues, capacityFixedWf, 'b-', 'LineWidth', 2.0);
plot(snrDbValues, capacityErgodicEpa, 'r--', 'LineWidth', 1.8);
plot(snrDbValues, capacityErgodicWf, 'r-', 'LineWidth', 2.0);

grid on;
set(gca, 'FontSize', 12);
xlim([-10, 30]);
xlabel('SNR (dB)', 'FontSize', 14, 'FontWeight', 'bold');
ylabel('Channel Capacity (bps/Hz)', 'FontSize', 14, 'FontWeight', 'bold');
title('Shannon Capacity vs SNR for SISO and MIMO 2x2 Systems', 'FontSize', 14, 'FontWeight', 'bold');
legend({'SISO AWGN', 'SISO Rayleigh Ergodic', ...
        'MIMO 2x2 Fixed H (EPA)', 'MIMO 2x2 Fixed H (Water-filling)', ...
        'MIMO 2x2 Rayleigh Ergodic (EPA)', 'MIMO 2x2 Rayleigh Ergodic (Water-filling)'}, ...
        'Location', 'northwest', 'FontSize', 11);

fprintf('========================================================================================\n');
fprintf('SNR(dB) | SISO AWGN | SISO Rayl | Fixed EPA | Fixed WF  | Ergodic EPA | Ergodic WF \n');
fprintf('========================================================================================\n');
for i = 1:3:numSnrPoints
    fprintf('%7.1f | %9.3f | %9.3f | %9.3f | %9.3f | %11.3f | %10.3f\n', ...
        snrDbValues(i), capacitySisoAwgn(i), capacityErgodicSiso(i), ...
        capacityFixedEpa(i), capacityFixedWf(i), capacityErgodicEpa(i), capacityErgodicWf(i));
end
fprintf('========================================================================================\n');
