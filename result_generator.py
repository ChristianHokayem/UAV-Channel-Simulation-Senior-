from DTE_Simulator import run_sim
from Simulation_Parameters import TIME_ADVANCE
from Packet import Packet

OUTPUT_FILE_NAME = 'fifo.csv'


def output_formatted_results(a_list):
    return_string = ""

    for item in a_list:
        return_string += str(item) + ","

    return_string += "\n"
    return return_string


def create_header():
    header = output_formatted_results(["Lambda", "Mu", "Generated Packets", "P1", "P2", "P3", "P4",
                                      "P5", "P6", "P1W", "P2W", "P3W", "P4W", "P5W", "P6W", "Wait Time"])

    with open(OUTPUT_FILE_NAME, 'w') as output_file:
        output_file.write(header)


#create_header()
MU = 250


for LAMBDA in range(511, 612, 10):
    run_sim(LAMBDA, MU)
    waits = [p.service_end_time - p.arrival_time for p in Packet.packets]

    average_total_wait_time = (sum(waits) / len(waits))*TIME_ADVANCE

    avg_packets_waits = [0] * 7

    print("Packet count:")
    for packet in Packet.packets_priority.keys():
        print(f"# of packets, priority {packet}: {len(Packet.packets_priority[packet])}")
    print("-" * 15)

    for i in range(1, len(avg_packets_waits)):
        avg_packets_waits[i] = (sum(p.service_end_time - p.arrival_time for p in Packet.packets_priority[i])
                                / len(Packet.packets_priority[i])) * TIME_ADVANCE

    with open(OUTPUT_FILE_NAME, 'a') as outfile:
        outfile.write(output_formatted_results([LAMBDA, MU, len(Packet.packets)] +
                                               [len(Packet.packets_priority[i]) for i in Packet.packets_priority.keys()]
                                               + avg_packets_waits[1:] + [average_total_wait_time]))

    Packet.clear_packets()
