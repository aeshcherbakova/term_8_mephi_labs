import random
import socket
import time
from random import randint
from config import *


print("Client 1 has started")
soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
soc.bind(FIRST_CLIENT_ADDRESS)


def sender():
    while True:
        try:
            time_parameter = random.uniform(2, 3)
            buffer = random.randbytes(randint(1024, 2048)) # по условию передаются пакеты случайной длины
            soc.sendto(buffer, PROXY_ADDRESS)
            time.sleep(time_parameter)   # по условию пакеты передаются в случайные моменты времени
        except (KeyboardInterrupt, EOFError) as e:
            soc.close()
            break;


if __name__ == '__main__':
    sender()
