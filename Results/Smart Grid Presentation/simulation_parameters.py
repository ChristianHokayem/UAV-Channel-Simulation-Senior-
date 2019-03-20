from Packet.PacketQCI import PacketQCI
from simulation_enums import *

PACKET_SIZE = 120 * 8  # 1.5kB packets
RB_BANDWIDTH = 180e3  # typical OFDM sub-band
N0_DB = -204  # -174 dBm/Hz typical noise level
DISTANCE_SCALE_PARAMETER = 500
TRANSMIT_POWER_DB = 0  # 43 – 48 dBm typical LTE transmit power values

TIME_ADVANCE = 1e-6  # in time unit
PACKETS_TARGET = 1000000  # number of packets to simulate
MAX_SCHEDULING_BLOCKS = 10
AVERAGE_REQUIRED_RESOURCE_BLOCKS = MAX_SCHEDULING_BLOCKS/2

LAMBDA_SIMULATION_RANGE = list(range(5000, 8000, 500)) + list(range(30000, 32700, 100)) + list(range(32710, 32800, 10))#[1] + list(range(200, 6001, 200)) + list(range(6100, 10000, 100)) + list(range(10100, 11601, 50))
QUEUING_SYSTEM = QueueingModel.FCFS_QUEUING
FADING = Fading.RICIAN
HEIGHT = 40

K_options = {10: 3.533, 25: 10.120, 40: 10.048}
K = K_options[HEIGHT]

OUTPUT_FILE_NAME = QUEUING_SYSTEM.value + '-' + FADING.value + '-HEIGHT = ' + str(HEIGHT) + '-APPEND.csv'


PACKET_QCI_DICT = {1: PacketQCI(1, 1, 0.075/2, proportional_lambda=1, description="Real-Time Services")#,
                   #2: PacketQCI(2, 2, 0.125/2, proportional_lambda=1/3, description="Conversational Services"),
                   #3: PacketQCI(3, 3, 0.300/2, proportional_lambda=1/3, description="Background Services")
                   }
