from DTE_Simulator import run_sim
from Simulation_Parameters import *
from Packet import Packet

OUTPUT_FILE_NAME = 'test.csv'


def output_formatted_results(a_list):
    return_string = ""

    for item in a_list:
        return_string += str(item) + ","

    return_string += "\n"
    return return_string


def create_header():
    header = output_formatted_results(["Lambda", "Mu", "Generated Packets", "Valid LP", "Dropped LP",
                                       "Valid HP", "Dropped HP", "Avg LP Wait", "Avg HP Wait", "Avg Total Wait"])

    with open(OUTPUT_FILE_NAME, 'w') as output_file:
        output_file.write(header)


create_header()
MU = 250

for LAMBDA in [1000]:
    print()
    simulation_start_string = f" Running simulation with lambda = {LAMBDA} "
    print("*" * len(simulation_start_string))
    print(simulation_start_string)
    print("*" * len(simulation_start_string))

    run_sim(LAMBDA, MU, EDF_QUEUING)

    print("LAMBDA:", LAMBDA)
    print("MU:", MU)
    print("Packets Generated:", Packet.packet_counter)
    print("-" * 15)

    valid_low_priority_packets = [p for p in Packet.packets_by_priority[LOW_PRIORITY] if p.service_end_time is not None]
    valid_high_priority_packets = [p for p in Packet.packets_by_priority[HIGH_PRIORITY] if
                                   p.service_end_time is not None]

    dropped_low_priority_packets = [p for p in Packet.packets_by_priority[LOW_PRIORITY] if p.service_end_time is None]
    dropped_high_priority_packets = [p for p in Packet.packets_by_priority[HIGH_PRIORITY] if p.service_end_time is None]

    valid_packets = valid_low_priority_packets + valid_high_priority_packets
    dropped_packets = dropped_low_priority_packets + dropped_high_priority_packets

    valid_packet_waits = [p.service_end_time - p.arrival_time for p in valid_packets]

    number_of_serviced_packets = len(valid_packets)
    number_of_dropped_packets = len(dropped_packets)

    print("Packet count:")
    print(f"    High Priority")
    print(f"        Serviced: {len(valid_high_priority_packets)}")
    print(f"        Dropped:  {len(dropped_high_priority_packets)}")
    print(f"    Low Priority")
    print(f"        Serviced: {len(valid_low_priority_packets)}")
    print(f"        Dropped:  {len(dropped_low_priority_packets)}")

    low_priority_wait_time = [p.service_end_time - p.arrival_time for p in valid_low_priority_packets]
    high_priority_wait_time = [p.service_end_time - p.arrival_time for p in valid_high_priority_packets]

    average_low_priority_wait_time = (sum(low_priority_wait_time)/len(low_priority_wait_time)) * TIME_ADVANCE
    average_high_priority_wait_time = (sum(high_priority_wait_time)/len(high_priority_wait_time)) * TIME_ADVANCE

    average_total_wait_time = (average_high_priority_wait_time + average_low_priority_wait_time)/2

    with open(OUTPUT_FILE_NAME, 'a') as outfile:
        outfile.write(output_formatted_results([LAMBDA, MU, number_of_serviced_packets + number_of_dropped_packets,
                                                len(valid_low_priority_packets), len(dropped_low_priority_packets),
                                                len(valid_high_priority_packets), len(dropped_high_priority_packets),
                                                average_low_priority_wait_time, average_high_priority_wait_time,
                                                average_total_wait_time])
                      )

    Packet.clear_packets()
