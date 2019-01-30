from random import expovariate, randint
from heapq import heappush

from Event import Event
from Packet import Packet


def discrete_expovariate_time(mean, time_advance):
    return round(expovariate(1/mean)/time_advance)


def generate_discrete_future_packet_arrivals_heap(packets_target, time_advance, avg_interarrival_time,
                                                  avg_deadline, priority_range, current_time=0):
    future_arrivals = []

    for _ in range(packets_target):
        priority = randint(priority_range[0], priority_range[1])
        arrival_time = current_time + discrete_expovariate_time(avg_interarrival_time, time_advance)
        current_time = arrival_time
        deadline = current_time + discrete_expovariate_time(avg_deadline, time_advance)
        new_packet = Packet(arrival_time, deadline, priority)
        heappush(future_arrivals, Event(arrival_time, Event.type_to_num['arrival'], new_packet))

    return future_arrivals
