class Packet:

    packets = []
    packets_priority = {1: [], 2: [], 3: [], 4: [], 5: [], 6: []}

    def __init__(self, arrival_time, deadline, priority):
        self.id = len(Packet.packets)
        self.arrival_time = arrival_time
        self.service_start_time = None
        self.deadline = deadline
        self.service_end_time = None
        self.wait = None
        self.priority = priority
        Packet.packets_priority[priority].append(self)
        Packet.packets.append(self)

    @staticmethod
    def clear_packets():
        Packet.packets = []
        for packet_priority in Packet.packets_priority.keys():
            Packet.packets_priority[packet_priority] = []

    def __lt__(self, other):
        return self.priority < other.priority

    def __gt__(self, other):
        return self.priority > other.priority

    def __le__(self, other):
        return self.priority <= other.priority

    def __ge__(self, other):
        return self.priority >= other.priority

    def __str__(self):
        return f"Packet ID: {self.id}"
