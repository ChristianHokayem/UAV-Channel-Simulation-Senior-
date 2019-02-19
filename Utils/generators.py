from heapq import heappush
from random import expovariate

from Event_Simulation.Event import Event
from Packet.Packet import Packet
from simulation_parameters import *


def discrete_rb_requirement_generator(avg_rb):
  rb_required = 0
  while rb_required <= 0 or rb_required > MAX_RESOURCE_BLOCKS:
    rb_required = round(expovariate(1/avg_rb))
  return rb_required


def discrete_expovariate_time(rate, time_advance):
  return round(expovariate(rate) / time_advance)


def add_future_packet_arrival_events_to_heap(events_heap, max_time, time_advance, arrival_rate,
                                             packet_qci, current_time=0):
  while current_time < max_time:
    arrival_time = current_time + discrete_expovariate_time(arrival_rate, time_advance)
    current_time = arrival_time

    deadline = current_time + discrete_expovariate_time(2/packet_qci.delay_budget, time_advance)

    new_packet = Packet(arrival_time, deadline, discrete_rb_requirement_generator(MAX_RESOURCE_BLOCKS/2), packet_qci)
    heappush(events_heap, Event(arrival_time, Event.type_to_num['arrival'], new_packet))

  return events_heap
