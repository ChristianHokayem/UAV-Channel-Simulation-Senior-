from Packet.PacketQCI import PacketQCI
from simulation_enums import *

PACKET_SIZE = 1500 * 8  # 1.5kB packets
RB_BANDWIDTH = 180e3  # typical OFDM sub-band
N0_DB = -204  # -174 dBm/Hz typical noise level
DISTANCE_SCALE_PARAMETER = 125
TRANSMIT_POWER_DB = 0  # 43 – 48 dBm typical LTE transmit power values

TIME_ADVANCE = 1e-6  # in time unit
PACKETS_TARGET = 1000000  # number of packets to simulate
MAX_SCHEDULING_BLOCKS = 50
AVERAGE_REQUIRED_RESOURCE_BLOCKS = MAX_SCHEDULING_BLOCKS/2

LAMBDA_SIMULATION_RANGE = [1] + list(range(500, 7000, 500)) + list(range(7000, 10001, 100))
QUEUING_SYSTEM = QueueingModel.EDF_QUEUING
FADING = Fading.RICIAN
HEIGHT = 10

K_options = {10: 3.533, 25: 10.120, 40: 10.048}
K = K_options[HEIGHT]

OUTPUT_FILE_NAME = QUEUING_SYSTEM.value + '-' + FADING.value + '-HEIGHT = ' + str(HEIGHT) + '-realtime.csv'


PACKET_QCI_DICT = {1: PacketQCI(1, 1, 0.075/2, proportional_lambda=0.8, description="Real-Time Services"),
                   2: PacketQCI(2, 2, 0.125/2, proportional_lambda=0.1, description="Conversational Services"),
                   3: PacketQCI(3, 3, 0.300/2, proportional_lambda=0.1, description="Background Services")
                   }
