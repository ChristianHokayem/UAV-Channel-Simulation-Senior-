from random import expovariate

TIME_ADVANCE = 1e-3 #in time unit
MAX_REAL_TIME = 60 #in time unit
AVG_INTERARRIVAL_TIME = 4 #in time unit
AVG_SERVICE_TIME = 2 #in time unit

MAX_SIM_TIME = int(MAX_REAL_TIME//TIME_ADVANCE)

def discrete_expovariate_time(mean):
    global TIME_ADVANCE
    return round(expovariate(1/mean)/TIME_ADVANCE)

def generate_discrete_future_packet_times(start_time = 0, end_time = MAX_SIM_TIME, avg_interarrival_time = AVG_INTERARRIVAL_TIME):
    arrival_times = []

    packet_arrival = start_time + discrete_expovariate_time(AVG_INTERARRIVAL_TIME)
    while packet_arrival < MAX_SIM_TIME:

        arrival_times.append(packet_arrival)
        packet_arrival += discrete_expovariate_time(AVG_INTERARRIVAL_TIME)

    return arrival_times

print("Generated packet arrival times:", generate_discrete_future_packet_times())

master_clk = 0
future_events = generate_discrete_future_packet_times()

wait_times = []
serviced_times = []
busy = False

for master_clk in range(master_clk, MAX_SIM_TIME+1):
    if len(future_events) == 0:
        continue
    
    if not(busy):
        if future_events[0] <= master_clk:
            next_service = master_clk + discrete_expovariate_time(AVG_SERVICE_TIME)
            busy = True
    else:
        if next_service == master_clk:
            start_time = future_events.pop(0)
            end_time = master_clk
            serviced_times.append(end_time)
            wait_times.append(end_time - start_time)
            busy = False

print("Serviced at:", serviced_times)
print("Wait times:", wait_times)

wait_time_string = "AVERAGE WAIT TIME: " + str((sum(wait_times)/len(wait_times))*TIME_ADVANCE)
print("-"*len(wait_time_string))
print(wait_time_string)
print("-"*len(wait_time_string))
print("PACKETS WAITING:", len(future_events))
print("PACKETS SERVICED:", len(wait_times))

