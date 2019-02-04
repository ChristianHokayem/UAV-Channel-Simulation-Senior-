from heapq import heappush, heappop

from Event import Event
from Packet import Packet
from PacketBuffer import PacketBuffer
from TokenBucket import TokenBucket
from utils import add_future_packet_arrival_events_to_heap, discrete_expovariate_time

TIME_ADVANCE = 1e-6  # in time unit
PACKETS_TARGET = 1000000  # number of packets to simulate)\
MAX_RESOURCE_BLOCKS = 100


def run_sim(arrival_rate, service_rate):

    avg_inter_arrival_time = 1 / arrival_rate  # in time unit

    #  TO-DO: Replace these dictionaries with a class of priorities!!!
    priorities_resource_allocation = {1: 100, 2: 75, 3: 50, 4: 25, 5: 15, 6: 6}
    priorities_arrival_rates = {1: arrival_rate / 12, 2: 2 * arrival_rate / 12, 3: 2 * arrival_rate / 12,
                                4: 3 * arrival_rate / 12, 5: 3 * arrival_rate / 12, 6: 2 * arrival_rate / 12}

    max_sim_time = PACKETS_TARGET*avg_inter_arrival_time/TIME_ADVANCE

    future_events = []

    for priority in priorities_arrival_rates.keys():
        add_future_packet_arrival_events_to_heap(future_events, max_sim_time, TIME_ADVANCE,
                                                 priorities_arrival_rates[priority], 100, priority)

    print("-" * 15)
    print("LAMBDA:", arrival_rate)
    print("MU:", service_rate)
    print("Packets Generated:", len(Packet.packets))
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
                bucket.return_resource(priorities_resource_allocation[current_event.reference_packet.priority])

        if len(buffer.queue) == 0:
            if len(future_events) > 0:
                master_clock = future_events[0].time
            continue

        served_packets = []

        for packet in buffer:
            if bucket.consume(priorities_resource_allocation[packet.priority]):
                served_packets.append(packet)
                packet.service_start_time = master_clock
                heappush(future_events, Event(master_clock + discrete_expovariate_time(service_rate, TIME_ADVANCE),
                                              Event.type_to_num['service end'], packet))

        if len(served_packets) == 0:
            if len(future_events) > 0:
                master_clock = future_events[0].time
            continue

        for packet in served_packets:
            buffer.remove_packet(packet)

        master_clock += 1
