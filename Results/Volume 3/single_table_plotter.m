clc
clear

load('simulation_results.mat')
working_table = PRIORITY_p3;
out_string = "background services dominance with priority queuing";

x = table2array(working_table(:,Lambda));
y1 = 1000*table2array(working_table(:,q1_wait));
y2 = 1000*table2array(working_table(:,q2_wait));
y3 = 1000*table2array(working_table(:,q3_wait));

subplot(2,1,1)
plot(x,y1,x,y2,x,y3)
xlabel('Lambda (aggregate arrivals/second)')
ylabel('Wait Times (ms)')
legend('Real Time Services', 'Conversational Services', 'Background Services')
title('Wait times for ' + out_string)
xlim([1,4200])
grid on

subplot(2,1,2)
drop1 = 100*table2array(working_table(:,q1_drop));
drop2 = 100*table2array(working_table(:,q2_drop));
drop3 = 100*table2array(working_table(:,q3_drop));
plot(x,drop1,x,drop2,x,drop3)
xlabel('Lambda (aggregate arrivals/second)')
ylabel('Drop Rate (%)')
legend('Real Time Services', 'Conversational Services', 'Background Services')
title('Drop rates for ' + out_string)
xlim([1,4200])
grid on

