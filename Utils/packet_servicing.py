from heapq import heappush

from numpy.ma import log2, sqrt, log10, exp
from numpy.random.mtrand import rayleigh
from scipy.stats import rice, rayleigh

from Event_Simulation.Event import Event
from Event_Simulation.simulation_enums import Fading


def start_packet_service(bucket, future_events, master_clock, popped_packet, transmit_power_db,
                         time_advance, fading_type, height, rb_noise, rb_bandwidth, k=0):
  popped_packet.service_start_time = master_clock
  bucket.consume(popped_packet.required_resources)
  heappush(future_events, generate_packet_service_event(master_clock, popped_packet, transmit_power_db,
                                                        time_advance, fading_type, height, rb_noise, rb_bandwidth, k))


def generate_packet_service_event(master_clock, popped_packet, transmit_power_db, time_advance,
                                  fading_type, height, rb_noise, rb_bandwidth, k):
  service_time = None
  if fading_type == Fading.RICIAN:
    service_time = (popped_packet.size / compute_rice_capacity(
      compute_a2g_received_power(transmit_power_db, popped_packet.distance, height),
      popped_packet.required_resources, rb_noise, rb_bandwidth, k)) / time_advance

  elif fading_type == Fading.RAYLEIGH:
    service_time = (popped_packet.size / compute_rayleigh_capacity(
      compute_g2g_received_power(transmit_power_db, popped_packet.distance),
      popped_packet.required_resources, rb_noise, rb_bandwidth)) / time_advance

  return Event(master_clock + service_time, Event.type_to_num['service end'], popped_packet)


def compute_rayleigh_capacity(pr_avg, allocated_resource_blocks, rb_noise, rb_bandwidth):
  sigma = sqrt(pr_avg / 2)
  faded_power = rayleigh.rvs(scale=sigma) ** 2
  rb_capacity = allocated_resource_blocks * rb_bandwidth * log2(1 + faded_power / rb_noise)
  return rb_capacity


def compute_rice_capacity(pr_avg, allocated_resource_blocks, rb_noise, rb_bandwidth, k):
  scale_param = sqrt(pr_avg / (2 * (k + 1)))
  b = sqrt(pr_avg*k/(1+k))/scale_param
  faded_power = rice.rvs(b=b, scale=scale_param) ** 2
  rb_capacity = allocated_resource_blocks * rb_bandwidth * log2(1 + faded_power / rb_noise)
  return rb_capacity


def compute_a2g_received_power(transmit_power_db, distance, height):
  received_power_db = transmit_power_db - (46.4 + 20.1 * log10(sqrt(distance ** 2 + height ** 2)))
  return 10 ** (received_power_db / 10)


def compute_g2g_received_power(transmit_power_db, distance):
  los_probability = g2g_los_probability(distance * 0.001)
  received_power_db = transmit_power_db - ((103.4 + 24.2 * log10(distance * 0.001)) * los_probability
                                           + (131.1 + 42.8 * log10(distance * 0.001)) * (1 - los_probability))
  return 10 ** (received_power_db / 10)


def g2g_los_probability(R):
  return min(0.018 / R, 1) * (1 - exp(-R / 0.063)) + exp(-R / 0.063)
