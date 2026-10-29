clc;
clear;
close all;

H = [0.7, 0.3; 0.4, 0.6];
h11 = H(1,1);
h12 = H(1,2);
h21 = H(2,1);
h22 = H(2,2);

s0 = 1 + 1i;
s1 = 1 - 1i;

r0 = h11 * s0 + h12 * s1;
r1 = -h11 * conj(s1) + h12 * conj(s0);
r2 = h21 * s0 + h22 * s1;
r3 = -h21 * conj(s1) + h22 * conj(s0);

frobeniusNormSquared = abs(h11)^2 + abs(h12)^2 + abs(h21)^2 + abs(h22)^2;

combinerOutput0 = conj(h11) * r0 + h12 * conj(r1) + conj(h21) * r2 + h22 * conj(r3);
combinerOutput1 = conj(h12) * r0 - h11 * conj(r1) + conj(h22) * r2 - h21 * conj(r3);

recoveredSymbol0 = combinerOutput0 / frobeniusNormSquared;
recoveredSymbol1 = combinerOutput1 / frobeniusNormSquared;

errorSymbol0 = abs(recoveredSymbol0 - s0);
errorSymbol1 = abs(recoveredSymbol1 - s1);

fprintf('========================================================\n');
fprintf('     MIMO 2x2 ALAMOUTI STBC STEP-BY-STEP RECOVERY       \n');
fprintf('========================================================\n');
fprintf('Channel Matrix H:\n');
disp(H);
fprintf('Frobenius Norm Squared ||H||_F^2: %.4f\n\n', frobeniusNormSquared);

fprintf('Transmitted Symbols:\n');
fprintf('  s0 = %+.4f %+.4fi\n', real(s0), imag(s0));
fprintf('  s1 = %+.4f %+.4fi\n\n', real(s1), imag(s1));

fprintf('Received Signals (Noise = 0):\n');
fprintf('  Time Slot 1, Antenna Rx1: r0 = %+.4f %+.4fi\n', real(r0), imag(r0));
fprintf('  Time Slot 2, Antenna Rx1: r1 = %+.4f %+.4fi\n', real(r1), imag(r1));
fprintf('  Time Slot 1, Antenna Rx2: r2 = %+.4f %+.4fi\n', real(r2), imag(r2));
fprintf('  Time Slot 2, Antenna Rx2: r3 = %+.4f %+.4fi\n\n', real(r3), imag(r3));

fprintf('Combiner Outputs (z = H_eff^H * r):\n');
fprintf('  z0 = %+.4f %+.4fi\n', real(combinerOutput0), imag(combinerOutput0));
fprintf('  z1 = %+.4f %+.4fi\n\n', real(combinerOutput1), imag(combinerOutput1));

fprintf('Recovered Symbols (s_hat = z / ||H||_F^2):\n');
fprintf('  s_hat0 = %+.4f %+.4fi (Error: %.2e)\n', real(recoveredSymbol0), imag(recoveredSymbol0), errorSymbol0);
fprintf('  s_hat1 = %+.4f %+.4fi (Error: %.2e)\n\n', real(recoveredSymbol1), imag(recoveredSymbol1), errorSymbol1);
fprintf('========================================================\n');
