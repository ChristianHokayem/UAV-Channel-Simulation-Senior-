class PacketBuffer:
    def __init__(self):
        self.queue = []

    def add_packet(self, packet):
        self.queue.append(packet)
        self.queue.sort(key=lambda x:x.priority, reverse=True)

    def remove_packet(self, packet):
        self.queue.remove(packet)

    def __iter__(self):
        for element in self.queue:
            yield element

