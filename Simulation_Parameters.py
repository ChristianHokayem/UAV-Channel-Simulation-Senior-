from Packet.PacketQCI import PacketQCI

LOW_PRIORITY = 0
HIGH_PRIORITY = 1

FCFS_QUEUING = 0
PRIORITY_QUEUING = 1
MODIFIED_PRIORITY_QUEUING = 2
EDF_QUEUING = 3

PACKET_SIZE = 1500 * 8
ONE_RB_SPEED = 1008000  # 12 symbols * 7 time slots * 6 bit/symbol (64-QAM)  * 2 blocks/ms

TIME_ADVANCE = 1e-6  # in time unit
PACKETS_TARGET = 1000000  # number of packets to simulate
MAX_RESOURCE_BLOCKS = 100
DISCRETE_RESOURCE_ALLOCATIONS = [6, 15, 25, 50, 75, 100]

PACKET_QCI_DICT = {1: PacketQCI(1, True, 2, 0.100, proportional_lambda=0.1, description="Conversational Voice"),
                   2: PacketQCI(2, True, 4, 0.150, proportional_lambda=0.1, description="Conversational Video"),
                   3: PacketQCI(3, True, 5, 0.300, proportional_lambda=0.1, description="Buffered Video"),
                   4: PacketQCI(4, True, 3, 0.050, proportional_lambda=0.1, description="Real Time Gaming"),
                   5: PacketQCI(5, False, 1, 0.100, proportional_lambda=0.1, description="IMS Signaling"),
                   6: PacketQCI(6, False, 7, 0.100, proportional_lambda=0.2, description="Voice, video, gaming"),
                   7: PacketQCI(7, False, 6, 0.300, proportional_lambda=0.3, description="Video & TCP Based (QCI 7,8,9)")}

if round(sum(PACKET_QCI_DICT[i].proportional_lambda for i in PACKET_QCI_DICT), 3) != 1:
  raise ValueError("Sum of proportional arrival rates does not equal 1.000")

