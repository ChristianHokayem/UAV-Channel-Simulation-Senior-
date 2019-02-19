from Packet.PacketQCI import PacketQCI
from simulation_enums import *

PACKET_SIZE = 1500 * 8
ONE_RB_SPEED = 1008000  # 12 symbols * 7 time slots * 6 bit/symbol (64-QAM)  * 2 blocks/ms

TIME_ADVANCE = 1e-6  # in time unit
PACKETS_TARGET = 1000000  # number of packets to simulate
MAX_RESOURCE_BLOCKS = 100

LAMBDA_SIMULATION_RANGE = [1] + list(range(100, 4501, 100))
QUEUING_SYSTEM = FCFS_QUEUING
OUTPUT_FILE_NAME = "output.csv"

PACKET_QCI_DICT = {1: PacketQCI(1, 1, 0.075/2, proportional_lambda=1/3, description="Real-Time Services"),
                   2: PacketQCI(2, 2, 0.125/2, proportional_lambda=1/3, description="Conversational Services"),
                   3: PacketQCI(3, 3, 0.300/2, proportional_lambda=1/3, description="Background Services")
                   }
