clc
clear

load('results-pres.mat')
working_table_1 = g2g;
working_table_2 = a2g_10;
working_table_3 = a2g_25;
working_table_4 = a2g_40;

wait_column = 6;
drop_column = 7;

x1 = table2array(working_table_1(:,Lambda));
x2 = table2array(working_table_2(:,Lambda));
x3 = table2array(working_table_3(:,Lambda));
x4 = table2array(working_table_4(:,Lambda));
y1 = 100*table2array(working_table_1(:,drop_column));
y2 = 100*table2array(working_table_2(:,drop_column));
y3 = 100*table2array(working_table_3(:,drop_column));
y4 = 100*table2array(working_table_4(:,drop_column));

plot(x1,y1,x2,y2,x3,y3,x4,y4)
xlabel('Lambda (arrivals/second)')
ylabel('Drop Rates (%)')
legend('GRN', 'ARN h=10m', 'ARN h=25m', 'ARN h=40m')
title('Average Drop Rates')

grid on
