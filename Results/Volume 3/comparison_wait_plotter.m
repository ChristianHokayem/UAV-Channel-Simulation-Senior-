clc
clear

load('simulation_results.mat')
working_table_1 = PRIORITY_equal;
working_table_2 = EDF_equal;
working_table_3 = FCFS_equal;

out_string = "background services dominance";
title(out_string)

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

subplot(2,2,1)
plot(x1,y1,x2,y4,x3,y7)
xlabel('Lambda (aggregate arrivals/second)')
ylabel('Wait Times (ms)')
legend('Priority', 'EDF', 'FCFS')
title('Wait times for realtime services')
xlim([1,4000])
grid on

subplot(2,2,2)
plot(x1,y2,x2,y5,x3,y8)
xlabel('Lambda (aggregate arrivals/second)')
ylabel('Wait Times (ms)')
legend('Priority', 'EDF', 'FCFS')
title('Wait times for conversational services')
xlim([1,4000])
grid on

subplot(2,2,3)
plot(x1,y3,x2,y6,x3,y9)
xlabel('Lambda (aggregate arrivals/second)')
ylabel('Wait Times (ms)')
legend('Priority', 'EDF', 'FCFS')
title('Wait times for background services')
xlim([1,4000])
grid on


% subplot(2,1,2)
% drop1 = 100*table2array(working_table_1(:,q1_drop));
% drop2 = 100*table2array(working_table_1(:,q2_drop));
% drop3 = 100*table2array(working_table_1(:,q3_drop));
% drop4 = 100*table2array(working_table_2(:,q1_drop));
% drop5 = 100*table2array(working_table_2(:,q2_drop));
% drop6 = 100*table2array(working_table_2(:,q3_drop));
% drop7 = 100*table2array(working_table_3(:,q1_drop));
% drop8 = 100*table2array(working_table_3(:,q2_drop));
% drop9 = 100*table2array(working_table_3(:,q3_drop));
% plot(x,drop1,x,drop2,x,drop3,x,drop4,x,drop5,x,drop6,x,drop7,x,drop8,x,drop9)
% xlabel('Lambda (aggregate arrivals/second)')
% ylabel('Drop Rate (%)')
% legend('Priority: RTS', 'Priority: CS', 'Priority: BGS', 'EDF: RTS', 'EDF: CS', 'EDF: BGS', 'FCFS: RTS', 'FCFS: CS', 'FCFS: BGS')
% title('Drop rates for ' + out_string)
% xlim([1,4200])
% grid on

