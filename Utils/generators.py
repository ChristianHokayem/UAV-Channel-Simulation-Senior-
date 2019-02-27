from heapq import heappush
from random import expovariate
from numpy.random import geometric, normal

from Event_Simulation.Event import Event
from Packet.Packet import Packet
from simulation_parameters import *


def discrete_rb_requirement_generator(avg_rb):
  rb_required = 0
  while rb_required <= 0 or rb_required > MAX_SCHEDULING_BLOCKS:
    rb_required = geometric(1/avg_rb)
  return rb_required


def discrete_expovariate_time(rate, time_advance):
  return round(expovariate(rate) / time_advance)


def add_future_packet_arrival_events_to_heap(events_heap, max_time, time_advance, arrival_rate,
                                             packet_qci, current_time=0):
  while current_time < max_time:
    arrival_time = current_time + discrete_expovariate_time(arrival_rate, time_advance)
    current_time = arrival_time

    deadline = current_time + discrete_expovariate_time(2/packet_qci.delay_budget, time_advance)

    new_packet = Packet(arrival_time, deadline, discrete_rb_requirement_generator(MAX_SCHEDULING_BLOCKS / 2),
                        packet_qci, generate_random_snr_db(10, 1))
    heappush(events_heap, Event(arrival_time, Event.type_to_num['arrival'], new_packet))

  return events_heap


#  A Model of the Probability Distribution of the Signal-to-Noise Ratio Estimated from BER Measurements
#  https://usatcorp.com/faqs/understanding-lte-signal-strength-values/
#  would it make more sense to generate random distances uniformly distributed, and from them infer the avg snr?
def generate_random_snr_db(mean, stdev):
  return normal(mean, stdev)
