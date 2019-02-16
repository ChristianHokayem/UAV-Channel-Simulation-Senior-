from Simulation_Parameters import PACKET_QCI_DICT


class Packet:

    packets_by_qci = {qci: [] for qci in PACKET_QCI_DICT}
    packet_counter = 0

    def __init__(self, arrival_time, deadline, priority, required_resources, qci):
        self.id = Packet.packet_counter
        Packet.packet_counter += 1
        self.arrival_time = arrival_time
        self.service_start_time = None
        self.deadline = deadline
        self.service_end_time = None
        self.wait = None
        self.required_resources = required_resources
        self.allocated_resources = None
        self.priority = priority
        self.qci = qci
        Packet.packets_by_qci[qci.qci].append(self)

    @staticmethod
    def clear_packets():
        Packet.packet_counter = 0
        for packet_qci in Packet.packets_by_qci:
            Packet.packets_by_qci[packet_qci] = []

    def __str__(self):
        return f"Packet ID: {self.id}"

    def __lt__(self, other):
        return self.priority < other.priority
