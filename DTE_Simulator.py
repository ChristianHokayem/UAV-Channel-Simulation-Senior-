from time import time
from heapq import heappush, heapify
import argparse

from Packet import Packet
from Event import Event
from PacketBuffer import PacketBuffer
from TokenBucket import TokenBucket
from utils import generate_discrete_future_packet_arrivals, discrete_expovariate_time

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
PACKETS_TARGET = 1000  # number of packets to simulate)

RESOURCE_ALLOCATION = {1: 50, 2: 30, 3: 15, 4: 10}
MAX_TOKENS = 80

future_events = generate_discrete_future_packet_arrivals(PACKETS_TARGET, TIME_ADVANCE,
                                                          AVG_INTERARRIVAL_TIME, 1.5 * AVG_SERVICE_TIME)
heapify(future_events)
master_clock = 0

buffer = PacketBuffer()
bucket = TokenBucket(MAX_TOKENS)


while len(future_events) > 0:

    while len(future_events) > 0 and future_events[0].time <= master_clock:

        current_event = future_events.pop(0)

        if current_event.type == Event.type_to_num['arrival']:
            buffer.add_packet(current_event.reference_packet)

        elif current_event.type == Event.type_to_num['service end']:
            current_event.reference_packet.service_end_time = master_clock
            bucket.return_resource(RESOURCE_ALLOCATION[current_event.reference_packet.priority])

    if len(buffer.queue) == 0:
        if len(future_events) > 0:
            master_clock = future_events[0].time
        continue

    served_packets = []
    for packet in buffer:
        if bucket.consume(RESOURCE_ALLOCATION[packet.priority]):
            served_packets.append(packet)
            packet.service_start_time = master_clock
            heappush(future_events, Event(master_clock + discrete_expovariate_time(AVG_SERVICE_TIME,TIME_ADVANCE),
                                           Event.type_to_num['service end'], packet))

    if len(served_packets) == 0:
        if len(future_events) > 0:
            master_clock = future_events[0].time
        continue

    for packet in served_packets:
        buffer.remove_packet(packet)

    master_clock += 1


waits = [p.service_end_time - p.arrival_time for p in Packet.Packets]
print("AVERAGE TOTAL WAIT TIME: " + str((sum(waits)/len(waits))*TIME_ADVANCE))

END_TIME = time()

print("SCRIPT TIME:", END_TIME - START_TIME)

print("-"*10)
