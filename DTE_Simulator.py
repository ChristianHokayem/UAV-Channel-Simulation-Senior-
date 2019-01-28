from time import time
import argparse

from Event import Event
from TokenBucket import TokenBucket
from utils import generate_discrete_future_packet_arrivals

parent_parser = argparse.ArgumentParser(add_help=False)
parent_parser.add_argument('LAMBDA', type=float)
args = parent_parser.parse_args()

START_TIME = time()
LAMBDA = args.LAMBDA
print("\n"*2)
print("-"*10)
print("LAMBDA:", LAMBDA)

TIME_ADVANCE = 1e-6  # in time unit
AVG_INTERARRIVAL_TIME = 1/LAMBDA  # in time unit
AVG_SERVICE_TIME = 1/250  # in time unit
PACKETS_TARGET = 5  # number of packets to simulate
RESOURCE_ALLOCATION = {1: 50, 2: 30, 3: 15, 4: 10}

future_events = []
bucket = TokenBucket(80)

future_events += generate_discrete_future_packet_arrivals(PACKETS_TARGET, TIME_ADVANCE,
                                                          AVG_INTERARRIVAL_TIME, 1.5 * AVG_SERVICE_TIME)

# while len(future_events) > 0 or busy == True:
#     if not(busy):
#         if future_events[0] <= master_clock:
#             next_service = master_clock + discrete_expovariate_time(AVG_SERVICE_TIME)
#             busy = True
#         else:
#             master_clock = future_events[0]
#             continue
#     else:
#         if next_service == master_clock:
#             start_time = future_events.pop(0)
#             end_time = master_clock
#             serviced_times.append(end_time)
#             wait_times.append(end_time - start_time)
#             busy = False
#         else:
#             master_clock = next_service
#             continue
#
#     master_clock += 1

#Waits = [a.wait for a in Packets]
#print("AVERAGE TOTAL WAIT TIME: " + str((sum(Waits)/len(Waits))*TIME_ADVANCE))

END_TIME = time()

print("SCRIPT TIME:", END_TIME - START_TIME)

print("-"*10)
