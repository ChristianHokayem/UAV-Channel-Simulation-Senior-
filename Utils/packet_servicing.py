from heapq import heappush

from numpy.ma import log2, sqrt
from numpy.random.mtrand import rayleigh
from scipy.stats import rice

from Event_Simulation.Event import Event
from simulation_parameters import PACKET_SIZE, TIME_ADVANCE, RB_BANDWIDTH, FADING, RICIAN, RAYLEIGH


def start_packet_service(bucket, future_events, master_clock, popped_packet):
  popped_packet.service_start_time = master_clock
  bucket.consume(popped_packet.required_resources)
  heappush(future_events, generate_packet_service_event(master_clock, popped_packet))


def generate_packet_service_event(master_clock, popped_packet):
  if FADING == RICIAN:
    service_time = (PACKET_SIZE / compute_rice_capacity(popped_packet.snr, popped_packet.required_resources))/TIME_ADVANCE
  elif FADING == RAYLEIGH:
    service_time = (PACKET_SIZE / compute_rayleigh_capacity(popped_packet.snr, popped_packet.required_resources))/TIME_ADVANCE
  return Event(master_clock + service_time, Event.type_to_num['service end'], popped_packet)


def compute_rayleigh_capacity(snr, allocated_resource_blocks):
  faded_snr = rayleigh(10**(snr/10))
  rb_capacity = allocated_resource_blocks * RB_BANDWIDTH * log2(1 + faded_snr)
  return rb_capacity


def compute_rice_capacity(snr, allocated_resource_blocks):
  k = 10.048
  sigma = 10**(snr/10)/sqrt(k+1)
  s = sqrt(k*2)*sigma
  faded_snr = rice.rvs(sigma, s)
  rb_capacity = allocated_resource_blocks * RB_BANDWIDTH * log2(1 + faded_snr)
  return rb_capacity
