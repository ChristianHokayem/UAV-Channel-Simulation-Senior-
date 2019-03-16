clc
clear

load('r-r-results.mat')
working_table_1 = rayleigh_priority;
working_table_2 = rice_priority;

%out_string = "Rayleigh Vs Rice FCFS Wait Times";
%title(out_string)

x1 = table2array(working_table_1(:,Lambda));
x2 = table2array(working_table_2(:,Lambda));

y1 = 1000*table2array(working_table_1(:,q1_drop));
y2 = 1000*table2array(working_table_1(:,q2_drop));
y3 = 1000*table2array(working_table_1(:,q3_drop));
y4 = 1000*table2array(working_table_2(:,q1_drop));
y5 = 1000*table2array(working_table_2(:,q2_drop));
y6 = 1000*table2array(working_table_2(:,q3_drop));

subplot(2,2,1)
plot(x1,y1,x2,y4)
xlabel('Lambda (aggregate arrivals/second)')
ylabel('Drop rate')
legend('G2G', 'A2G')
title('Drop rate for realtime services')
xlim([1,1700])
grid on

subplot(2,2,2)
plot(x1,y2,x2,y5)
xlabel('Lambda (aggregate arrivals/second)')
ylabel('Drop rate')
legend('G2G', 'A2G')
xlim([1,1700])
title('Drop rate for conversational services')
grid on

subplot(2,2,3)
plot(x1,y3,x2,y6)
xlabel('Lambda (aggregate arrivals/second)')
ylabel('Drop rate')
legend('G2G', 'A2G')
title('Drop rate for background services')
xlim([1,1700])
grid on