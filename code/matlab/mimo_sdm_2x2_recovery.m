clc;
clear;
close all;

H = [0.7, 0.3; 0.4, 0.6];
x = [1 + 1i; 1 - 1i];

y = H * x;

weightMatrixZf = pinv(H);
recoveredX_Zf = weightMatrixZf * y;
errorZf = norm(recoveredX_Zf - x);

noiseVariance = 0;
weightMatrixMmse = (H' * H + noiseVariance * eye(2)) \ H';
recoveredX_Mmse = weightMatrixMmse * y;
errorMmse = norm(recoveredX_Mmse - x);

[U, S, V] = svd(H);
xPrecoded = V * x;
ySvd = H * xPrecoded;
yCombinedSvd = U' * ySvd;
recoveredX_Svd = S \ yCombinedSvd;
errorSvd = norm(recoveredX_Svd - x);

fprintf('========================================================\n');
fprintf('       MIMO 2x2 SDM STEP-BY-STEP SIGNAL RECOVERY        \n');
fprintf('========================================================\n');
fprintf('Channel Matrix H:\n');
disp(H);
fprintf('Transmitted Symbol Vector x:\n');
disp(x);
fprintf('Received Vector y without precoding (y = H * x):\n');
disp(y);

fprintf('--------------------------------------------------------\n');
fprintf('1. ZERO-FORCING (ZF) DETECTION\n');
fprintf('Weight Matrix W_ZF = pinv(H):\n');
disp(weightMatrixZf);
fprintf('Recovered Symbol Vector x_hat_ZF = W_ZF * y:\n');
disp(recoveredX_Zf);
fprintf('ZF Norm Error: %.2e\n', errorZf);

fprintf('--------------------------------------------------------\n');
fprintf('2. MINIMUM MEAN SQUARE ERROR (MMSE) DETECTION\n');
fprintf('Noise Variance: %.4f\n', noiseVariance);
fprintf('Weight Matrix W_MMSE = inv(H''*H + sigma^2*I) * H'':\n');
disp(weightMatrixMmse);
fprintf('Recovered Symbol Vector x_hat_MMSE = W_MMSE * y:\n');
disp(recoveredX_Mmse);
fprintf('MMSE Norm Error: %.2e\n', errorMmse);

fprintf('--------------------------------------------------------\n');
fprintf('3. SVD TRANSMIT PRECODING & RECEIVER DECOUPLING\n');
fprintf('Unitary Matrix U (Left Singular Vectors):\n');
disp(U);
fprintf('Singular Value Matrix S:\n');
disp(S);
fprintf('Unitary Matrix V (Right Singular Vectors / Precoding):\n');
disp(V);
fprintf('Precoded Vector x_tx = V * x:\n');
disp(xPrecoded);
fprintf('Channel Output y_svd = H * x_tx:\n');
disp(ySvd);
fprintf('Decoupled Received Vector y_tilde = U'' * y_svd = S * x:\n');
disp(yCombinedSvd);
fprintf('Recovered Vector x_hat_SVD = inv(S) * y_tilde:\n');
disp(recoveredX_Svd);
fprintf('SVD Norm Error: %.2e\n', errorSvd);
fprintf('========================================================\n');
