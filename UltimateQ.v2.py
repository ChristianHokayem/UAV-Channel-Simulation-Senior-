from random import expovariate

TIME_ADVANCE = 1e-3 #in time unit
MAX_REAL_TIME = 6000 #in time unit
AVG_INTERARRIVAL_TIME = 3 #in time unit
AVG_SERVICE_TIME = 2 #in time unit

MAX_SIM_TIME = int(MAX_REAL_TIME//TIME_ADVANCE)

class Event():
    type_toString = {1:"ARRIVAL", 2:"START_SERVICE", 3:"END_SERVICE"}
    arrival = 1
    service_start = 2
    end_service = 3
    def __init__(self, event_type = None, event_time = None, associated_packet = None):
        self.event_type = event_type
        self.event_time = event_time
        self.associated_packet = associated_packet

    def __str__(self):
        return "EVENT_TYPE=" + str(Event.type_toString[self.event_type]) + "|EVENT_TIME=" + str(self.event_time) + "|ASSOCIATED_PACKET=" + str(self.associated_packet)

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

events_list = []
packet_counter = 1
for arrival_time in generate_discrete_future_packet_times():
    events_list.append(Event(event_type = 1, event_time = arrival_time, associated_packet = packet_counter))
    packet_counter += 1

for event in events_list:        
    print("Generated packet arrival time:", event)
    
##master_clock = 0
##
##wait_times = []
##serviced_times = []
##busy = False
##
##while master_clock <= MAX_SIM_TIME:
##    if len(future_events) == 0:
##        break
##    
##    if not(busy):
##        if future_events[0] <= master_clock:
##            next_service = master_clock + discrete_expovariate_time(AVG_SERVICE_TIME)
##            busy = True
##        else:
##            master_clock = future_events[0]
##            continue
##    else:
##        if next_service == master_clock:
##            start_time = future_events.pop(0)
##            end_time = master_clock
##            serviced_times.append(end_time)
##            wait_times.append(end_time - start_time)
##            busy = False
##        else:
##            master_clock = next_service
##            continue
##
##        
##    master_clock += 1
##
##print("Serviced at:", serviced_times)
##print("Wait times:", wait_times)
##
##wait_time_string = "AVERAGE TOTAL WAIT TIME: " + str((sum(wait_times)/len(wait_times))*TIME_ADVANCE)
##print("-"*len(wait_time_string))
##print(wait_time_string)
##print("-"*len(wait_time_string))
##print("PACKETS WAITING:", len(future_events))
##print("PACKETS SERVICED:", len(wait_times))
##
