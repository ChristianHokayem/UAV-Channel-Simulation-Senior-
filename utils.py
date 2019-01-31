from heapq import heappush
from random import expovariate

from Event import Event
from Packet import Packet


def discrete_expovariate_time(rate, time_advance):
    return round(expovariate(rate)/time_advance)


def add_future_packet_arrival_events_to_heap(events_heap, max_time, time_advance, arrival_rate,
                                             avg_deadline, priority, current_time=0):

    while current_time < max_time:
        arrival_time = current_time + discrete_expovariate_time(arrival_rate, time_advance)
        current_time = arrival_time
        deadline = current_time + discrete_expovariate_time(avg_deadline, time_advance)
        new_packet = Packet(arrival_time, deadline, priority)
        heappush(events_heap, Event(arrival_time, Event.type_to_num['arrival'], new_packet))

    return events_heap
