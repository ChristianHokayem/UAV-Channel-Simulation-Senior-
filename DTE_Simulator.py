from random import expovariate
from time import time

START_TIME = time()

TIME_ADVANCE = 1e-6 #in time unit
MAX_REAL_TIME = 6000 #in time unit
AVG_INTERARRIVAL_TIME = 1/97 #in time unit
AVG_SERVICE_TIME = 1/250 #in time unit

MAX_SIM_TIME = int(MAX_REAL_TIME//TIME_ADVANCE)

def sayHi(name):
	print("Hi,", name)

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


future_events = generate_discrete_future_packet_times()
master_clock = 0

wait_times = []
serviced_times = []
busy = False

while master_clock <= MAX_SIM_TIME:
    if len(future_events) == 0:
        break
    
    if not(busy):
        if future_events[0] <= master_clock:
            next_service = master_clock + discrete_expovariate_time(AVG_SERVICE_TIME)
            busy = True
        else:
            master_clock = future_events[0]
            continue
    else:
        if next_service == master_clock:
            start_time = future_events.pop(0)
            end_time = master_clock
            serviced_times.append(end_time)
            wait_times.append(end_time - start_time)
            busy = False
        else:
            master_clock = next_service
            continue
        
    master_clock += 1

wait_time_string = "AVERAGE TOTAL WAIT TIME: " + str((sum(wait_times)/len(wait_times))*TIME_ADVANCE)
print("-"*len(wait_time_string))
print(wait_time_string)
print("-"*len(wait_time_string))
print("PACKETS WAITING:", len(future_events))
print("PACKETS SERVICED:", len(wait_times))

END_TIME = time()

print("SCRIPT TIME:", END_TIME - START_TIME)
