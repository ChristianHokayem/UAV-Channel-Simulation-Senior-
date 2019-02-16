from Event_Simulation.DTE_Simulator import run_sim
from Simulation_Parameters import *
from Packet.Packet import Packet

OUTPUT_FILE_NAME = 'output.csv'


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
  with open(OUTPUT_FILE_NAME, 'w') as output_file:
    output_file.write(return_formatted_output_results(header))


output_header()

for LAMBDA in [2500]:
  ordered_packet_qci_stats = []

  print()
  simulation_start_string = f"Running simulation with lambda = {LAMBDA}"
  print("*" * len(simulation_start_string))
  print(simulation_start_string)
  print("*" * len(simulation_start_string))

  run_sim(LAMBDA, PRIORITY_QUEUING)

  print("LAMBDA:", LAMBDA)
  print("Packets Generated:", Packet.packet_counter)

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

  with open(OUTPUT_FILE_NAME, 'a') as outfile:
    outfile.write(return_formatted_output_results([LAMBDA, Packet.packet_counter] + ordered_packet_qci_stats))

  Packet.clear_packets()
