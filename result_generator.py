from Event_Simulation.DTE_Simulator import run_sim
from Simulation_Parameters import *
from Packet.Packet import Packet

OUTPUT_FILE_NAME = 'idk.csv'


def output_formatted_results(a_list):
  return_string = ""

  for item in a_list:
    return_string += str(item) + ","

  return_string += "\n"
  return return_string


def create_header():
  header = output_formatted_results(["Lambda", "Generated Packets", "Avg Total Wait"])

  with open(OUTPUT_FILE_NAME, 'w') as output_file:
    output_file.write(header)


#create_header()

for LAMBDA in range(4600, 5500, 100):
  print()
  simulation_start_string = f"Running simulation with lambda = {LAMBDA}"
  print("*" * len(simulation_start_string))
  print(simulation_start_string)
  print("*" * len(simulation_start_string))

  run_sim(LAMBDA, PRIORITY_QUEUING)

  print("LAMBDA:", LAMBDA)
  print("Packets Generated:", Packet.packet_counter)

  for packet_qci in Packet.packets_by_qci:
    print("---")
    print(f"QCI = {packet_qci}:")
    print((sum(i.service_end_time - i.arrival_time
               for i in Packet.packets_by_qci[packet_qci] if i.service_end_time is not None)
          / len(Packet.packets_by_qci[packet_qci]))*TIME_ADVANCE)

    print("Drop rate: {:.6}".format((len([i for i in Packet.packets_by_qci[packet_qci] if i.service_end_time is None])
          / len(Packet.packets_by_qci[packet_qci]))*TIME_ADVANCE))

#  with open(OUTPUT_FILE_NAME, 'a') as outfile:
#    outfile.write(output_formatted_results([LAMBDA, Packet.packet_counter, average_total_wait_time])
#                  )

  Packet.clear_packets()
