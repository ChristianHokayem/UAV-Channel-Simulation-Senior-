class Packet:
    Packets = []

    def __init__(self, arrival_time, deadline, priority):
        self.arrival_time = arrival_time
        self.service_start_time = None
        self.deadline = deadline
        self.service_end_time = None
        self.wait = None
        self.priority = priority
        Packet.Packets.append(self)
