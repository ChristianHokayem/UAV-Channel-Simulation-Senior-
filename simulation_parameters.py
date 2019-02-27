from Packet.PacketQCI import PacketQCI
from simulation_enums import *

PACKET_SIZE = 1500 * 8
RB_BANDWIDTH = 180e3  # 12 symbols * 7 time slots * 6 bit/symbol (64-QAM)  * 2 blocks/ms

TIME_ADVANCE = 1e-6  # in time unit
PACKETS_TARGET = 1000000  # number of packets to simulate
MAX_SCHEDULING_BLOCKS = 50

LAMBDA_SIMULATION_RANGE = [1] + list(range(100, 1701, 100))
QUEUING_SYSTEM = FCFS_QUEUING
FADING = RAYLEIGH
OUTPUT_FILE_NAME = "fcfs-rayleigh.csv"


PACKET_QCI_DICT = {1: PacketQCI(1, 1, 0.075/2, proportional_lambda=1/3, description="Real-Time Services"),
                   2: PacketQCI(2, 2, 0.125/2, proportional_lambda=1/3, description="Conversational Services"),
                   3: PacketQCI(3, 3, 0.300/2, proportional_lambda=1/3, description="Background Services")
                   }
