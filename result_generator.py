from Event_Simulation.DTE_Simulator import run_sim
from Packet.Packet import Packet
from Packet.PacketQCI import PACKET_QCI_DICT
from Event_Simulation.simulation_enums import QueueingModel, Fading

PACKET_SIZE = 1500 * 8  # 1.5kB packets
RB_BANDWIDTH = 180e3  # typical OFDM sub-band
N0_DB = -204  # -174 dBm/Hz typical noise level
DISTANCE_SCALE_PARAMETER = 125
TRANSMIT_POWER_DB = 0

TIME_ADVANCE = 1e-6  # in time unit
PACKETS_TARGET = 100  # approximate number of packets to simulate
MAX_SCHEDULING_BLOCKS = 50

LAMBDA_SIMULATION_RANGE = [1] + list(range(500, 7000, 500)) + list(range(7000, 10001, 100))
QUEUING_SYSTEM = QueueingModel.EDF_QUEUING
FADING = Fading.RICIAN
HEIGHT = 10

K_options = {10: 3.533, 25: 10.120, 40: 10.048}
K = K_options[HEIGHT]

OUTPUT_FILE_NAME = QUEUING_SYSTEM.value + '-' + FADING.value + '-h=' + str(HEIGHT) + '.csv'


def return_formatted_output_results(a_list):
  return_string = ""

  for item in a_list:
    return_string += str(item) + ","

  return_string += "\n"
  return return_string


def output_header():
  header = ["Lambda", "Generated Packets"]
  for i in PACKET_QCI_DICT:
    header.append(f"Q{i}#")
    header.append(f"Q{i} Avg Wait")
    header.append(f"Q{i} Drop Rate")

  header.append("Total Avg Wait Time")
  header.append("Total Avg Drop Rate")

  with open(OUTPUT_FILE_NAME, 'w') as output_file:
    output_file.write(return_formatted_output_results(header))


output_header()
Packet.clear_packets()

for LAMBDA in LAMBDA_SIMULATION_RANGE:
  ordered_packet_qci_stats = []

  print()
  simulation_start_string = f"Running simulation with lambda = {LAMBDA}"
  print("*" * len(simulation_start_string))
  print(simulation_start_string)
  print("*" * len(simulation_start_string))

  run_sim(LAMBDA, QUEUING_SYSTEM, N0_DB, RB_BANDWIDTH, PACKET_QCI_DICT, PACKET_SIZE, DISTANCE_SCALE_PARAMETER,
          TIME_ADVANCE, PACKETS_TARGET, MAX_SCHEDULING_BLOCKS, FADING, TRANSMIT_POWER_DB, HEIGHT, K)

  print("LAMBDA:", LAMBDA)
  print("Packets Generated:", len(Packet.all_packets))

  for packet_qci in Packet.packets_by_qci:
    number_of_packets = len(Packet.packets_by_qci[packet_qci])
    average_wait = (sum(i.service_end_time - i.arrival_time
                        for i in Packet.packets_by_qci[packet_qci] if i.service_end_time is not None)
                    / len(Packet.packets_by_qci[packet_qci])) * TIME_ADVANCE
    drop_rate = len([i for i in Packet.packets_by_qci[packet_qci] if i.service_end_time is None]) / number_of_packets

    print("---")
    print(f"QCI = {packet_qci}:")
    print(f"# of packets: {number_of_packets}")
    print(f"Average wait: {average_wait}")
    print("Drop rate: {:.4%}".format(drop_rate))
    ordered_packet_qci_stats.append(number_of_packets)
    ordered_packet_qci_stats.append(average_wait)
    ordered_packet_qci_stats.append(drop_rate)

  total_average_wait = TIME_ADVANCE * sum(
    i.service_end_time - i.arrival_time for i in Packet.all_packets if i.service_end_time is not None) / len(
    Packet.all_packets)
  total_drop_rate = len([i for i in Packet.all_packets if i.service_end_time is None]) / len(Packet.all_packets)
  ordered_packet_qci_stats.append(total_average_wait)
  ordered_packet_qci_stats.append(total_drop_rate)

  print("---")
  print(f"Average wait: {total_average_wait}")
  print("Average Drop rate: {:.4%}".format(total_drop_rate))

  with open(OUTPUT_FILE_NAME, 'a') as outfile:
    outfile.write(return_formatted_output_results([LAMBDA, len(Packet.all_packets)] + ordered_packet_qci_stats))

  Packet.clear_packets()
