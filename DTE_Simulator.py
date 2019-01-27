from random import expovariate
from random import randint
from time import time
import argparse

parent_parser = argparse.ArgumentParser(add_help=False)
parent_parser.add_argument('LAMBDA', type=float)
args = parent_parser.parse_args()

START_TIME = time()
LAMBDA = args.LAMBDA
print("\n"*2)
print("-"*10)
print("LAMBDA:", LAMBDA)

TIME_ADVANCE = 1e-6 #in time unit
AVG_INTERARRIVAL_TIME = 1/LAMBDA #in time unit
AVG_SERVICE_TIME = 1/250 #in time unit
PACKETS_TARGET = 100000 #number of pcakets to simulate


class TokenBucket:
    def __init__(self, tokens):
        self.capacity = float(tokens)
        self.available_tokens = float(tokens)

    def consume(self, number_of_tokens):
        if number_of_tokens <= self.available_tokens:
            self.available_tokens -= number_of_tokens
        else:
            return False
        return True


class Packet:
    def __init__(self, arrival_date, service_start_date, service_time):
        self.arrival_date = arrival_date
        self.service_start_date = service_start_date
        self.service_time = service_time
        self.service_end_date = self.service_start_date + self.service_time
        self.wait = self.service_start_date - self.arrival_date
        self.priority = randint(1, 4)


def discrete_expovariate_time(mean):
    global TIME_ADVANCE
    return round(expovariate(1/mean)/TIME_ADVANCE)

def generate_discrete_future_packets():
    for _ in range(PACKETS_TARGET):
        if len(Packets) == 0:
            arrival_date = discrete_expovariate_time(AVG_INTERARRIVAL_TIME)
            service_start_date = arrival_date
        else:
            arrival_date += discrete_expovariate_time(AVG_INTERARRIVAL_TIME)
            service_start_date = max(arrival_date, Packets[-1].service_end_date)

        service_time = discrete_expovariate_time(AVG_SERVICE_TIME)

        Packets.append(Packet(arrival_date, service_start_date, service_time))

Packets = []
bucket = TokenBucket(80)

generate_discrete_future_arrival_date_times()
master_clock = 0

wait_times = []
serviced_times = []
busy = False


while len(future_events) > 0 or busy == True:
    if not(busy):
        if future_events[0] <= master_clock:
            next_service = master_clock + discrete_expovariate_time(AVG_SERVICE_TIME)
            busy = True
        else:
            master_clock = future_events[0]
            continue
    else:
        if next_service == master_clock:
            start_time = future_events.pop(0)
            end_time = master_clock
            serviced_times.append(end_time)
            wait_times.append(end_time - start_time)
            busy = False
        else:
            master_clock = next_service
            continue

    master_clock += 1

print("AVERAGE TOTAL WAIT TIME: " + str((sum(wait_times)/len(wait_times))*TIME_ADVANCE))

END_TIME = time()

print("SCRIPT TIME:", END_TIME - START_TIME)

print("-"*10)
