from time import time
from heapq import heappush, heappop
import argparse

from Packet import Packet
from Event import Event
from PacketBuffer import PacketBuffer
from TokenBucket import TokenBucket
from utils import add_future_packet_arrival_events_to_heap, discrete_expovariate_time

parent_parser = argparse.ArgumentParser(add_help=False)
parent_parser.add_argument('LAMBDA', type=float)
args = parent_parser.parse_args()

START_TIME = time()

LAMBDA = args.LAMBDA
MU = 250


TIME_ADVANCE = 1e-6  # in time unit
AVG_INTER_ARRIVAL_TIME = 1 / LAMBDA  # in time unit
AVG_SERVICE_TIME = 1 / MU  # in time unit
PACKETS_TARGET = 100000  # number of packets to simulate)\

#  TO-DO: Replace these dictionaries with a class of priorities!!!
PRIORITIES_RESOURCE_ALLOCATION = {1: 100, 2: 75, 3: 50, 4: 25, 5: 15, 6: 6}
PRIORITIES_ARRIVAL_RATES = {1: LAMBDA/12, 2: 2*LAMBDA/12, 3: 2*LAMBDA/12, 4: 3*LAMBDA/12, 5: 3*LAMBDA/12, 6: 2*LAMBDA/12}

MAX_RESOURCE_BLOCKS = 10000
max_sim_time = PACKETS_TARGET*AVG_INTER_ARRIVAL_TIME/TIME_ADVANCE

future_events = []

for priority in PRIORITIES_ARRIVAL_RATES.keys():
    add_future_packet_arrival_events_to_heap(future_events, max_sim_time, TIME_ADVANCE,
                                             PRIORITIES_ARRIVAL_RATES[priority], 100, priority)

print("-" * 15)
print("LAMBDA:", LAMBDA)
print("MU:", MU)
print("Packets Generated:", len(Packet.packets))
print("-" * 15)

packets_priority_count = [0] * 7

print("Packet count:")
for packet in Packet.packets:
    packets_priority_count[packet.priority] += 1

for i in range(1, len(packets_priority_count)):
    print(f"Packet priority {i}: {packets_priority_count[i]}")
print("-" * 15)


master_clock = 0

buffer = PacketBuffer()
bucket = TokenBucket(MAX_RESOURCE_BLOCKS)

while len(future_events) > 0:

    if future_events[0].time <= master_clock:

        current_event = heappop(future_events)

        if current_event.type == Event.type_to_num['arrival']:
            buffer.add_packet(current_event.reference_packet)

        elif current_event.type == Event.type_to_num['service end']:
            current_event.reference_packet.service_end_time = master_clock
            bucket.return_resource(PRIORITIES_RESOURCE_ALLOCATION[current_event.reference_packet.priority])

    if len(buffer.queue) == 0:
        if len(future_events) > 0:
            master_clock = future_events[0].time
        continue

    served_packets = []

    for packet in buffer:
        if bucket.consume(PRIORITIES_RESOURCE_ALLOCATION[packet.priority]):
            served_packets.append(packet)
            packet.service_start_time = master_clock
            heappush(future_events, Event(master_clock + discrete_expovariate_time(MU, TIME_ADVANCE),
                                          Event.type_to_num['service end'], packet))

    if len(served_packets) == 0:
        if len(future_events) > 0:
            master_clock = future_events[0].time
        continue

    for packet in served_packets:
        buffer.remove_packet(packet)

    master_clock += 1

waits = [p.service_end_time - p.arrival_time for p in Packet.packets]
print("AVERAGE TOTAL WAIT TIME: " + str((sum(waits) / len(waits)) * TIME_ADVANCE))

END_TIME = time()

print("SCRIPT TIME:", END_TIME - START_TIME)

print("-" * 15)
