clc
clear

load('r-r-results.mat')
working_table_1 = rice_edf;
working_table_2 = rayleigh_edf;
working_table_3 = rice_fcfs;



x1 = table2array(working_table_1(:,Lambda));
x2 = table2array(working_table_2(:,Lambda));
x3 = table2array(working_table_3(:,Lambda));

y1 = 1000*table2array(working_table_1(:,q1_wait));
y2 = 1000*table2array(working_table_1(:,q2_wait));
y3 = 1000*table2array(working_table_1(:,q3_wait));
y4 = 1000*table2array(working_table_2(:,q1_wait));
y5 = 1000*table2array(working_table_2(:,q2_wait));
y6 = 1000*table2array(working_table_2(:,q3_wait));
y7 = 1000*table2array(working_table_3(:,q1_wait));
y8 = 1000*table2array(working_table_3(:,q2_wait));
y9 = 1000*table2array(working_table_3(:,q3_wait));

%subplot(2,2,1)
plot(x1,y1,x2,y4)
xlabel('Lambda (aggregate arrivals/second)')
ylabel('Wait Times (ms)')
legend('a2g', 'g2g')
title('Wait times for realtime services')
xlim([1,1700])
grid on