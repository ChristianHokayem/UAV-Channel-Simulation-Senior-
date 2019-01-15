from threading import Thread
from time import sleep
from numpy.random import exponential
from datetime import datetime

buffer = []
running = 1

def packet_generator(average = 1):
    print("initialised packet generator...")
    global running
    while running:
        sleep(exponential(scale=average))
        log("oooh a packet")
        buffer.append(1)

def log(text):
    print('[' + str(datetime.now())[:-7] + ']' + text)

def packet_servicer(average_service_time = 1):
    global running
    while running:
        while(len(buffer) == 0):
            pass
        sleep(exponential(scale=average_service_time))
        buffer.pop()
        log("packet popped!")
        
try:
    generator_thread = Thread(target = packet_generator, args = (1,))
    service_thread = Thread(target = packet_servicer, args = (2,))

    generator_thread.start()
    service_thread.start()

    sleep(10)

finally:
    running = 0
