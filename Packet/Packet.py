from simulation_parameters import PACKET_QCI_DICT


class Packet:

    packets_by_qci = {qci: [] for qci in PACKET_QCI_DICT}
    all_packets = []

    def __init__(self, arrival_time, deadline, required_resources, qci, distance):
        self.id = len(Packet.all_packets)
        self.arrival_time = arrival_time
        self.service_start_time = None
        self.deadline = deadline
        self.service_end_time = None
        self.wait = None
        self.required_resources = required_resources
        self.distance = distance
        self.priority = qci.priority
        self.qci = qci
        Packet.packets_by_qci[qci.qci].append(self)
        Packet.all_packets.append(self)

    @staticmethod
    def clear_packets():
        Packet.all_packets.clear()
        for packet_qci in Packet.packets_by_qci:
            Packet.packets_by_qci[packet_qci] = []

    def __str__(self):
        return f"Packet ID: {self.id}"

    def __lt__(self, other):
        return self.priority < other.priority
