clc
clear

load('pres-results.mat')
working_table_1 = g2g_drop;
working_table_2 = a2g10_drop;
working_table_3 = a2g25_drop;
working_table_4 = a2g40_drop;

x1 = table2array(working_table_1(:,X));
x2 = table2array(working_table_2(:,X));
x3 = table2array(working_table_3(:,X));
x4 = table2array(working_table_4(:,X));
y1 = 100*table2array(working_table_1(:,Y));
y2 = 100*table2array(working_table_2(:,Y));
y3 = 100*table2array(working_table_3(:,Y));
y4 = 100*table2array(working_table_4(:,Y));

plot(x1,y1,x2,y2,x3,y3,x4,y4)
xlabel('Lambda (arrivals/second)')
ylabel('Drop Rate (%)')
legend('GRN', 'ARN h=10m', 'ARN h=25m', 'ARN h=40m')
title('Average Drop Rates')
ylim([0, 10])
grid on
