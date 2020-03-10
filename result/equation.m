n = 2;
k = 10;
o = 0.6;
Gmax = 1;

x = 0:0.1:28;
G = (x.^n ./ (x.^n + k.^n) - o/(1+o)) * (1+o) * Gmax;

figure
semilogy(x, G)
xlabel('time(day)')
ylabel('Gametocyte load')
grid on