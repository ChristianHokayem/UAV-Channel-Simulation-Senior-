from heapq import heappush, heappop
from Simulation_Parameters import HIGH_PRIORITY, LOW_PRIORITY
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
        self.queue = {HIGH_PRIORITY: [], LOW_PRIORITY: []}

    def add_packet(self, packet):
        heappush(self.queue[packet.priority],
                 (packet.arrival_time, packet))

    def __select_sub_queue_to_be_serviced_by_priority__(self, available_resources):
        if self.queue[HIGH_PRIORITY]:
            if available_resources >= self.queue[HIGH_PRIORITY][0][1].required_resources:
                return HIGH_PRIORITY
            else:
                return None

        elif self.queue[LOW_PRIORITY]:
            if available_resources >= self.queue[LOW_PRIORITY][0][1].required_resources:
                return LOW_PRIORITY

        return None

    def pop_packet(self, available_resources):
        try:
            return heappop(self.queue[self.__select_sub_queue_to_be_serviced_by_priority__(available_resources)])[1]
        except KeyError:
            return None


#  similar to priority packet buffer but lets low priority packets pass when high priority are blocked
class ModifiedPriorityPacketBuffer(PacketBuffer):
    def __init__(self):
        self.queue = {HIGH_PRIORITY: [], LOW_PRIORITY: []}

    def add_packet(self, packet):
        heappush(self.queue[packet.priority],
                 (packet.arrival_time, packet))

    def __select_sub_queue_to_be_serviced_by_priority__(self, available_resources):
        if self.queue[HIGH_PRIORITY]:
            if available_resources >= self.queue[HIGH_PRIORITY][0][1].required_resources:
                return HIGH_PRIORITY
        elif self.queue[LOW_PRIORITY]:
            if available_resources >= self.queue[LOW_PRIORITY][0][1].required_resources:
                return LOW_PRIORITY

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
