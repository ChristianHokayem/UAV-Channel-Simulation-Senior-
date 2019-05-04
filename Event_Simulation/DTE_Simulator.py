from heapq import heappop

from Packet.PacketBuffer import FCFSPacketBuffer, PriorityPacketBuffer, ModifiedPriorityPacketBuffer, EDFPacketBuffer
from Packet.TokenBucket import TokenBucket
from Utils.generators import add_future_packet_arrival_events_to_heap
from Utils.packet_servicing import *
from Event_Simulation.simulation_enums import QueueingModel

QUEUEING_SYSTEM_TO_BUFFER = {QueueingModel.FCFS_QUEUING: FCFSPacketBuffer(),
                             QueueingModel.PRIORITY_QUEUING: PriorityPacketBuffer(),
                             QueueingModel.MODIFIED_PRIORITY_QUEUING: ModifiedPriorityPacketBuffer(),
                             QueueingModel.EDF_QUEUING: EDFPacketBuffer()
                             }


def run_sim(arrival_rate, queueing_system, N0_db, rb_bandwidth, packet_qci_dict, packet_size,
            distance_scale_param, time_advance, target_packets, max_scheduling_blocks, fading_type, transmit_power_db,
            height, k, start_time=0):

  if round(sum(packet_qci_dict[i].proportional_lambda for i in packet_qci_dict), 3) != 1:
    raise ValueError("Sum of proportional arrival rates does not equal 1.000")

  avg_inter_arrival_time = 1 / arrival_rate  # in time unit
  avg_required_scheduling_blocks = max_scheduling_blocks / 2

  rb_noise = 10 ** (N0_db / 10) * rb_bandwidth
  max_sim_time = target_packets * avg_inter_arrival_time / time_advance

  future_events = []

  for packet_qci in packet_qci_dict:
    add_future_packet_arrival_events_to_heap(future_events, max_sim_time, time_advance,
                                             packet_qci_dict[packet_qci].proportional_lambda * arrival_rate,
                                             packet_qci_dict[packet_qci], distance_scale_param,
                                             avg_required_scheduling_blocks, max_scheduling_blocks, packet_size,
                                             start_time)

  master_clock = start_time

  buffer = QUEUEING_SYSTEM_TO_BUFFER[queueing_system]
  bucket = TokenBucket(max_scheduling_blocks)

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
      start_packet_service(bucket, future_events, master_clock, popped_packet, transmit_power_db, time_advance,
                           fading_type, height, rb_noise, rb_bandwidth, k)

      popped_packet = buffer.pop_packet(bucket.available_tokens)

    if not has_served_packet:
      if len(future_events) > 0:
        master_clock = future_events[0].time
      continue

    master_clock += 1
