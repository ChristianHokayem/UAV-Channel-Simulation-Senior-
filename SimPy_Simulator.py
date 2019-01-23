import simpy
from random import expovariate
from time import time

START_TIME = time()

N = 0
packet_counter = 0
AVG_INTERARRIVAL_TIME = 1/97
AVG_SERVICE_TIME = 1/250
MAX_REAL_TIME = 6000

ENVIRONMENT = simpy.Environment()
SERVER = simpy.Resource(ENVIRONMENT, 1)

packet_list = []

class Packet():
    def __init__(self):
        self.Id = None
        self.arrival_time = None
        self.serviced_time = None
        self.wait_time = None

def packet_servicer():
     global ENVIRONMENT, AVG_INTERARRIVAL_TIME, AVG_SERVICE_TIME, packet_counter, packet_list
     packet_counter += 1
     new_packet = Packet()
     new_packet.Id = packet_counter
     new_packet.arrival_time = ENVIRONMENT.now
     packet_list.append(new_packet)
     #print('Packet #{0}: Arrived at {1:05.2f}'.format(new_packet.Id, new_packet.arrival_time))
     with SERVER.request() as req:
         yield req
         new_packet.serviced_time = ENVIRONMENT.now
         #print('Packet #{0}: Begins servicing {1:05.2f}'.format(new_packet.Id, new_packet.serviced_time))
         service_duration = expovariate(1/AVG_SERVICE_TIME)
         yield ENVIRONMENT.timeout(service_duration)
         #print('Packet #{0}: Serviced at {1:05.2f}'.format(new_packet.Id, ENVIRONMENT.now))
         new_packet.wait_time = ENVIRONMENT.now - new_packet.arrival_time


def packet_generator():
    while True:
        arrival_time = expovariate(1/AVG_INTERARRIVAL_TIME)
        yield ENVIRONMENT.timeout(arrival_time)
        ENVIRONMENT.process(packet_servicer())

ENVIRONMENT.process(packet_generator())
ENVIRONMENT.run(until=MAX_REAL_TIME)

sum_of_wait = 0

for packet in packet_list:
    if packet.wait_time is not None:
        sum_of_wait += packet.wait_time

avg_wait = sum_of_wait/len(packet_list)

print("---------------------------------------")
print("AVERAGE WAIT TIME IN SYSTEM:", avg_wait)
print("---------------------------------------")
END_TIME = time()

print("SCRIPT TIME:", END_TIME - START_TIME)
