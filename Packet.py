class Packet:

    Packets = []

    def __init__(self, arrival_time, deadline, priority):
        self.id = len(Packet.Packets)
        self.arrival_time = arrival_time
        self.service_start_time = None
        self.deadline = deadline
        self.service_end_time = None
        self.wait = None
        self.priority = priority
        Packet.Packets.append(self)

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
