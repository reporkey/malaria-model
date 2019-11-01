n = 2;
k = 10;
o = 0.6;
Gmax = 10^3;

x = 0:0.1:28;
G = (x.^n ./ (x.^n + k.^n) - o/(1+o)) * (1+o) * Gmax;

figure
semilogy(x, G)
grid on
