from heapq import heappush
from random import expovariate
from numpy.random import geometric
from scipy.stats import rayleigh

from Event_Simulation.Event import Event
from Packet.Packet import Packet
from simulation_parameters import *


def discrete_rb_requirement_generator(avg_rb):
  rb_required = geometric(1 / avg_rb)
  while rb_required > MAX_SCHEDULING_BLOCKS:
    rb_required = geometric(1/avg_rb)
  return rb_required


def discrete_expovariate_time(rate, time_advance):
  return round(expovariate(rate) / time_advance)


#  https://arxiv.org/pdf/1404.3099.pdf distance is rayleigh distributed
def generate_random_distance(scale_parameter):
  return rayleigh.rvs(scale=scale_parameter)


def add_future_packet_arrival_events_to_heap(events_heap, max_time, time_advance, arrival_rate,
                                             packet_qci, distance_scale_param, current_time=0):
  while current_time < max_time:
    arrival_time = current_time + discrete_expovariate_time(arrival_rate, time_advance)
    current_time = arrival_time

    deadline = current_time + discrete_expovariate_time(2/packet_qci.delay_budget, time_advance)

    new_packet = Packet(arrival_time, deadline, discrete_rb_requirement_generator(AVERAGE_REQUIRED_RESOURCE_BLOCKS),
                        packet_qci, generate_random_distance(distance_scale_param))
    heappush(events_heap, Event(arrival_time, Event.type_to_num['arrival'], new_packet))

  return events_heap
