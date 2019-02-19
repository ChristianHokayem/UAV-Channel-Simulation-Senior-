clc
clear

load('simulation_results.mat')
working_table_1 = PRIORITY_p3;
working_table_2 = EDF_p3;
working_table_3 = FCFS_p3;

x1 = table2array(working_table_1(:,Lambda));
x2 = table2array(working_table_2(:,Lambda));
x3 = table2array(working_table_3(:,Lambda));

y1 = 100*table2array(working_table_1(:,q1_drop));
y2 = 100*table2array(working_table_1(:,q2_drop));
y3 = 100*table2array(working_table_1(:,q3_drop));
y4 = 100*table2array(working_table_2(:,q1_drop));
y5 = 100*table2array(working_table_2(:,q2_drop));
y6 = 100*table2array(working_table_2(:,q3_drop));
y7 = 100*table2array(working_table_3(:,q1_drop));
y8 = 100*table2array(working_table_3(:,q2_drop));
y9 = 100*table2array(working_table_3(:,q3_drop));

subplot(2,2,1)
plot(x1,y1,x2,y4,x3,y7)
xlabel('Lambda (aggregate arrivals/second)')
ylabel('Drop rate (%)')
legend('Priority', 'EDF', 'FCFS')
title('Drop rate for realtime services')
xlim([1,4000])
grid on

subplot(2,2,2)
plot(x1,y2,x2,y5,x3,y8)
xlabel('Lambda (aggregate arrivals/second)')
ylabel('Drop rate (%)')
legend('Priority', 'EDF', 'FCFS')
title('Drop rate for conversational services')
xlim([1,4000])
grid on

subplot(2,2,3)
plot(x1,y3,x2,y6,x3,y9)
xlabel('Lambda (aggregate arrivals/second)')
ylabel('Drop rate (%)')
legend('Priority', 'EDF', 'FCFS')
title('Drop rate for background services')
xlim([1,4000])
grid on
