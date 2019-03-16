from heapq import heappush

from numpy.ma import log2, sqrt, log10, exp
from numpy.random.mtrand import rayleigh
from scipy.stats import rice, rayleigh

from Event_Simulation.Event import Event
from simulation_enums import Fading
from simulation_parameters import PACKET_SIZE, TIME_ADVANCE, RB_BANDWIDTH, FADING, N0_DB, K, TRANSMIT_POWER_DB, HEIGHT

RB_NOISE = 10 ** (N0_DB / 10) * RB_BANDWIDTH
ALPHA_A2G = 2.01


def start_packet_service(bucket, future_events, master_clock, popped_packet):
  popped_packet.service_start_time = master_clock
  bucket.consume(popped_packet.required_resources)
  heappush(future_events, generate_packet_service_event(master_clock, popped_packet))


def generate_packet_service_event(master_clock, popped_packet):
  service_time = None
  if FADING == Fading.RICIAN:
    service_time = (PACKET_SIZE / compute_rice_capacity(
      compute_a2g_received_power(TRANSMIT_POWER_DB, popped_packet.distance, HEIGHT),
      popped_packet.required_resources)) / TIME_ADVANCE

  elif FADING == Fading.RAYLEIGH:
    service_time = (PACKET_SIZE / compute_rayleigh_capacity(
      compute_g2g_received_power(TRANSMIT_POWER_DB, popped_packet.distance),
      popped_packet.required_resources)) / TIME_ADVANCE

  return Event(master_clock + service_time, Event.type_to_num['service end'], popped_packet)


def compute_rayleigh_capacity(pr_avg, allocated_resource_blocks):
  sigma = sqrt(pr_avg)
  faded_power = rayleigh.rvs(scale=sigma)
  rb_capacity = allocated_resource_blocks * RB_BANDWIDTH * log2(1 + faded_power / RB_NOISE)
  return rb_capacity


def compute_rice_capacity(pr_avg, allocated_resource_blocks):
  v = sqrt(K * 2) * sqrt(pr_avg)
  scale_param = v ** 2 + 2 * sqrt(pr_avg) ** 2
  faded_power = rice.rvs(b=K, scale=scale_param)
  rb_capacity = allocated_resource_blocks * RB_BANDWIDTH * log2(1 + faded_power / RB_NOISE)
  return rb_capacity


def compute_a2g_received_power(transmit_power_db, distance, height):
  received_power_db = transmit_power_db - (46.4 + 10 * ALPHA_A2G * log10(sqrt(distance ** 2 + height ** 2)))
  return 10 ** (received_power_db / 10)


def compute_g2g_received_power(transmit_power_db, distance):
  los_probability = g2g_los_probability(distance)
  received_power_db = transmit_power_db - ((103.4 + 24.2 * log10(distance)) * los_probability
                                           + (131.1 + 42.8 * log10(distance)) * (1 - los_probability))
  return 10 ** (received_power_db / 10)


def g2g_los_probability(R):
  return min(0.018 / R, 1) * (1 - exp(-R / 0.063)) + exp(-R / 0.063)
