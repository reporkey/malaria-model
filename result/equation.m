n = 2;
k = 10;
o = 0.6;
o1 = 0.2;
o2 = 0.6;
o3 = 1;

x = 0:0.1:30;
G = (x.^n ./ (x.^n + k.^n) - o/(1+o)) * (1+o);
G1 = (x.^n ./ (x.^n + k.^n) - o1/(1+o1)) * (1+o1);
G2 = (x.^n ./ (x.^n + k.^n) - o2/(1+o2)) * (1+o2);
G3 = (x.^n ./ (x.^n + k.^n) - o3/(1+o3)) * (1+o3);
figure
semilogy(x, G)
plot(x, G1)
hold on
plot(x, G2)
hold on
plot(x, G3)
ylim([0 1])
xlabel('Time(day)')
ylabel('Gametocyte load')
hold off
legend('o = 0.2','o = 0.6','o = 1')
grid on