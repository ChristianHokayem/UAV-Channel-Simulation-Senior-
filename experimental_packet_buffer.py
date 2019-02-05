from heapq import heappush, heappop
from Simulation_Parameters import PRIORITIES_RESOURCE_ALLOCATION


class PacketBuffer:
    def __init__(self):
        self.queue = {1: [], 2: [], 3: [],
                      4: [], 5: [], 6: []}

    def add_packet(self, packet):
        heappush(self.queue[packet.priority],
                 (packet.arrival_time, packet))

    def __select_sub_queue_to_be_serviced_by_priority__(self, available_resources):
        for i in range(1, 7):
            if len(self.queue[i]) > 0 and available_resources >= PRIORITIES_RESOURCE_ALLOCATION[i]:
                return i
        return None

    def pop_packet(self, available_resources):
        return heappop(self.queue[self.__select_sub_queue_to_be_serviced_by_priority__(available_resources)])

    def __str__(self):
        return_str = ""
        for q in self.queue.keys():
            return_str += f"Priority {q} buffer: " + "|".join(str(p) for p in self.queue[q]) + "\n"
        return return_str
