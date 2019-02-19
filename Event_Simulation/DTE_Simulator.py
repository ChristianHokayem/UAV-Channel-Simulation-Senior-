from heapq import heappush, heappop

from Event_Simulation.Event import Event
from Packet.PacketBuffer import FCFSPacketBuffer, PriorityPacketBuffer, ModifiedPriorityPacketBuffer, EDFPacketBuffer
from Packet.TokenBucket import TokenBucket
from simulation_parameters import *
from Utils.generators import add_future_packet_arrival_events_to_heap


if round(sum(PACKET_QCI_DICT[i].proportional_lambda for i in PACKET_QCI_DICT), 3) != 1:
  raise ValueError("Sum of proportional arrival rates does not equal 1.000")


def run_sim(arrival_rate, queueing_system):
  avg_inter_arrival_time = 1 / arrival_rate  # in time unit

  max_sim_time = PACKETS_TARGET * avg_inter_arrival_time / TIME_ADVANCE

  future_events = []

  for packet_qci in PACKET_QCI_DICT:
    add_future_packet_arrival_events_to_heap(future_events, max_sim_time, TIME_ADVANCE,
                                             PACKET_QCI_DICT[packet_qci].proportional_lambda * arrival_rate,
                                             PACKET_QCI_DICT[packet_qci])

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
        bucket.return_resource(packet.required_resources)
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
      has_served_packet = True
      start_packet_service(bucket, future_events, master_clock, popped_packet)

      popped_packet = buffer.pop_packet(bucket.available_tokens)

    if not has_served_packet:
      if len(future_events) > 0:
        master_clock = future_events[0].time
      continue

    master_clock += 1


def start_packet_service(bucket, future_events, master_clock, popped_packet):
  popped_packet.service_start_time = master_clock
  bucket.consume(popped_packet.required_resources)
  heappush(future_events, generate_packet_service_event(master_clock, popped_packet))


def generate_packet_service_event(master_clock, popped_packet):
  return Event(master_clock + (PACKET_SIZE / (ONE_RB_SPEED * popped_packet.required_resources)) / TIME_ADVANCE,
               Event.type_to_num['service end'], popped_packet)
