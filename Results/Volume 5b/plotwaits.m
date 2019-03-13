clc
clear

load('results-pathloss-fading.mat')
working_table_1 = g2g;
working_table_2 = a2g_10;
working_table_3 = a2g_40;



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
y_avg_1 = 1000*table2array(working_table_1(:,wait_avg));
y_avg_2 = 1000*table2array(working_table_2(:,wait_avg));
y_avg_3 = 1000*table2array(working_table_3(:,wait_avg));

subplot(2,2,1)
plot(x1,y1,x2,y4,x3,y7)
xlabel('Lambda (aggregate arrivals/second)')
ylabel('Wait Times (ms)')
legend('g2g', 'a2g h=10m', 'a2g h=40m')
title('Wait times for realtime services')

grid on

subplot(2,2,2)
plot(x1,y2,x2,y5,x3,y8)
xlabel('Lambda (aggregate arrivals/second)')
ylabel('Wait Times (ms)')
legend('g2g', 'a2g h=10m', 'a2g h=40m')
title('Wait times for conversational services')

grid on

subplot(2,2,3)
plot(x1,y3,x2,y6,x3,y9)
xlabel('Lambda (aggregate arrivals/second)')
ylabel('Wait Times (ms)')
legend('g2g', 'a2g h=10m', 'a2g h=40m')
title('Wait times for background services')

grid on

subplot(2,2,4)
plot(x1,y_avg_1,x2,y_avg_2,x3,y_avg_3)
xlabel('Lambda (aggregate arrivals/second)')
ylabel('Wait Times (ms)')
legend('g2g', 'a2g h=10m', 'a2g h=40m')
title('Average wait times')
grid on