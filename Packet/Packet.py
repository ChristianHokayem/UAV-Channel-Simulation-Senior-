from Simulation_Parameters import LOW_PRIORITY, HIGH_PRIORITY


class Packet:

    packets_by_priority = {LOW_PRIORITY: [], HIGH_PRIORITY: []}
    packet_counter = 0

    def __init__(self, arrival_time, deadline, priority, required_resources):
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
        Packet.packets_by_priority[priority].append(self)

    @staticmethod
    def clear_packets():
        Packet.packet_counter = 0
        for packet_priority in Packet.packets_by_priority.keys():
            Packet.packets_by_priority[packet_priority] = []

    def __str__(self):
        return f"Packet ID: {self.id}"

    def __lt__(self, other):
        return self.priority < other.priority
