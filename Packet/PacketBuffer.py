from heapq import heappush, heappop
from Packet.PacketQCI import PACKET_QCI_DICT
from abc import ABC, abstractmethod


class PacketBuffer(ABC):
    @abstractmethod
    def add_packet(self, packet):
        pass

    @abstractmethod
    def pop_packet(self, available_resources):
        pass


class PriorityPacketBuffer(PacketBuffer):
    def __init__(self):
        self.queue = {i: [] for i in PACKET_QCI_DICT}

    def add_packet(self, packet):
        heappush(self.queue[packet.qci.qci],
                 (packet.arrival_time, packet))

    def __select_sub_queue_to_be_serviced_by_priority__(self, available_resources):
        for qci in self.queue:
            if self.queue[qci]:
                if available_resources >= self.queue[qci][0][1].required_resources:
                    return qci
                else:
                    return None

        return None

    def pop_packet(self, available_resources):
        try:
            return heappop(self.queue[self.__select_sub_queue_to_be_serviced_by_priority__(available_resources)])[1]
        except KeyError:
            return None


#  similar to priority packet buffer but lets low priority packets pass when high priority are blocked
class ModifiedPriorityPacketBuffer(PacketBuffer):
    def __init__(self):
        self.queue = {i: [] for i in PACKET_QCI_DICT}

    def add_packet(self, packet):
        heappush(self.queue[packet.qci.qci],
                 (packet.arrival_time, packet))

    def __select_sub_queue_to_be_serviced_by_priority__(self, available_resources):
        for qci in self.queue:
            if self.queue[qci]:
                if available_resources >= self.queue[qci][0][1].required_resources:
                    return qci
        return None

    def pop_packet(self, available_resources):
        try:
            return heappop(self.queue[self.__select_sub_queue_to_be_serviced_by_priority__(available_resources)])[1]
        except KeyError:
            return None


class FCFSPacketBuffer(PacketBuffer):

    def __init__(self):
        self.queue = []

    def add_packet(self, packet):
        heappush(self.queue, (packet.arrival_time, packet))

    def pop_packet(self, available_resources):
        if self.queue:
            top_packet = self.queue[0][1]
            if top_packet.required_resources <= available_resources:
                return heappop(self.queue)[1]

        return None


class EDFPacketBuffer(PacketBuffer):

    def __init__(self):
        self.queue = []

    def add_packet(self, packet):
        heappush(self.queue, (packet.deadline, packet))

    def pop_packet(self, available_resources):
        if self.queue:
            top_packet = self.queue[0][1]
            if top_packet.required_resources <= available_resources:
                return heappop(self.queue)[1]

        return None
