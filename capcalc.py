from Utils.packet_servicing import *

PACKET_SIZE = 1500 * 8  # 1.5kB packets
RB_BANDWIDTH = 180e3  # typical OFDM sub-band
N0_DB = -204  # -174 dBm/Hz typical noise level
DISTANCE_SCALE_PARAMETER = 125
rb_noise = 10 ** (N0_DB / 10) * RB_BANDWIDTH
MAX_SCHEDULING_BLOCKS = 50

PR_AVG = 10**(-8.8)

capacity = [0]*3
k = [3.533, 10.120, 10.048]
sim_points = 10000

for j in range(3):
    for i in range(sim_points):
        capacity[j] += compute_rice_capacity(PR_AVG, 1, rb_noise, RB_BANDWIDTH, k[j])
    capacity[j] /= sim_points

ray_cap = 0
for i in range(sim_points):
    ray_cap += compute_rayleigh_capacity(PR_AVG, 1, rb_noise, RB_BANDWIDTH)
ray_cap /= sim_points

with open('outcap.csv', 'w+') as outfile:
    for j in range(3):
        outfile.write(str(k[j]) + ',' + str(capacity[j]) + '\n')
    outfile.write("RAY," + str(ray_cap))
