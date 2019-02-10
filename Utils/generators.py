from heapq import heappush
from random import expovariate, choice, uniform
from Simulation_Parameters import *
from Event_Simulation.Event import Event
from Packet import Packet


def discrete_expovariate_time(rate, time_advance):
    return round(expovariate(rate) / time_advance)


def add_future_packet_arrival_events_to_heap(events_heap, max_time, time_advance, arrival_rate,
                                             priority, current_time=0):
    while current_time < max_time:
        arrival_time = current_time + discrete_expovariate_time(arrival_rate, time_advance)
        current_time = arrival_time

        try:
            deadline = current_time + round(uniform(PRIORITIES_DEADLINE_RANGES[priority][0],
                                                    PRIORITIES_DEADLINE_RANGES[priority][1]) / TIME_ADVANCE)
        except KeyError:
            raise ValueError("Deadline is not valid!")

        new_packet = Packet(arrival_time, deadline, priority, choice(DISCRETE_RESOURCE_ALLOCATIONS))
        heappush(events_heap, Event(arrival_time, Event.type_to_num['arrival'], new_packet))

    return events_heap
