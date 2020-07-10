x = logspace(0, 5);

y = normcdf(log(x*0.00031)/3.91);

figure
semilogx(x, y);
hold on;
grid on;
semilogx(x, y.^2)