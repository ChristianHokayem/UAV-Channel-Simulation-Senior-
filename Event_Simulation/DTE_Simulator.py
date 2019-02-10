from heapq import heappush, heappop

from Event_Simulation.Event import Event
from Packet.PacketBuffer import FCFSPacketBuffer, PriorityPacketBuffer, ModifiedPriorityPacketBuffer, EDFPacketBuffer
from Simulation_Parameters import *
from Packet.TokenBucket import TokenBucket
from Utils.generators import add_future_packet_arrival_events_to_heap, discrete_expovariate_time


def run_sim(arrival_rate, service_rate, queueing_system):
  avg_inter_arrival_time = 1 / arrival_rate  # in time unit

  priorities_arrival_rates = {LOW_PRIORITY: PRIORITIES_ARRIVAL_RATE_PROPORTION[LOW_PRIORITY] * arrival_rate,
                              HIGH_PRIORITY: PRIORITIES_ARRIVAL_RATE_PROPORTION[HIGH_PRIORITY] * arrival_rate}

  max_sim_time = PACKETS_TARGET * avg_inter_arrival_time / TIME_ADVANCE

  future_events = []

  for priority in priorities_arrival_rates.keys():
    add_future_packet_arrival_events_to_heap(future_events, max_sim_time, TIME_ADVANCE,
                                             priorities_arrival_rates[priority], priority)

  master_clock = 0

  if queueing_system == FCFS_QUEUING:
    buffer = FCFSPacketBuffer()
  elif queueing_system == PRIORITY_QUEUING:
    buffer = PriorityPacketBuffer()
  elif queueing_system == MODIFIED_PRIORITY_QUEUING:
    buffer = ModifiedPriorityPacketBuffer()
  elif queueing_system == EDF_QUEUING:
    buffer = EDFPacketBuffer()
  else:
    raise TypeError("UNKNOWN PACKET BUFFER TYPE!")

  bucket = TokenBucket(MAX_RESOURCE_BLOCKS)

  while len(future_events) > 0:

    if future_events[0].time <= master_clock:

      current_event = heappop(future_events)

      if current_event.type == Event.type_to_num['arrival']:
        buffer.add_packet(current_event.reference_packet)

      elif current_event.type == Event.type_to_num['service end']:
        packet = current_event.reference_packet
        bucket.return_resource(packet.allocated_resources)
        if packet.deadline >= master_clock:
          packet.service_end_time = master_clock
        else:
          pass  # no service end time

    if len(buffer.queue) == 0:
      if len(future_events) > 0:
        master_clock = future_events[0].time
      continue

    has_served_packet = False
    popped_packet = buffer.pop_packet(bucket.available_tokens)
    while popped_packet is not None:
      # TODO: POSSIBLE PREMATURE DEPARTURE | if popped_packet.deadline >= master_clock:
      has_served_packet = True
      start_packet_service(bucket, future_events, master_clock, popped_packet, service_rate)

      popped_packet = buffer.pop_packet(bucket.available_tokens)

    if not has_served_packet:
      if len(future_events) > 0:
        master_clock = future_events[0].time
      continue

    master_clock += 1


def start_packet_service(bucket, future_events, master_clock, popped_packet, service_rate):
  popped_packet.service_start_time = master_clock
  popped_packet.allocated_resources = popped_packet.required_resources
  bucket.consume(popped_packet.allocated_resources)
  heappush(future_events, Event(master_clock + discrete_expovariate_time(service_rate, TIME_ADVANCE),
                                Event.type_to_num['service end'], popped_packet))
