from multiprocessing import Process
import os
from queue import Queue
from select import select
from socket import *
import struct
import sys
import time


class Channel:
    BUFFER_SIZE = 8
    ICMP_TYPE = 8
    TIME_INTERVAL = 1

    def __init__(self, destination_address):
        self.buffer = Queue(maxsize=self.BUFFER_SIZE)
        self.destination_address = destination_address
        self.process_id = os.getpid() & 0xffff

        for counter in range(self.BUFFER_SIZE // 2):
            self.prepare_packet()

    def calculate_checksum(self, data):
        data = bytearray(data)
        length = (len(data) // 2) * 2
        sum = 0

        for counter in range(0, length, 2):
            value = data[counter + 1] * 256 + data[counter]
            sum = sum + value
            sum = sum & 0xffffffff

        if length < len(data):
            sum = sum + data[-1]
            sum = sum & 0xffffffff

        sum = (sum >> 16) + (sum & 0xffff)
        sum = sum + (sum >> 16)
        checksum = ~sum
        checksum = checksum & 0xffff
        checksum = checksum >> 8 | (checksum << 8 & 0xff00)
        return checksum

    def prepare_packet(self):
        header = struct.pack("bbHHh", self.ICMP_TYPE, 0, 0, self.process_id, 1)
        data = struct.pack("d", time.time())
        checksum = self.calculate_checksum(header + data)

        if sys.platform == "darwin":
            checksum = htons(checksum) & 0xffff
        else:
            checksum = htons(checksum)

        header = struct.pack("bbHHh", self.ICMP_TYPE, 0, checksum, self.process_id, 1)
        packet = header + data
        self.buffer.put(packet)

    def receive_packet(self, sock, timeout=1):
        while True:
            start = time.time()
            flag = select([sock], [], [], timeout)
            difference = time.time() - start

            if flag[0] == []:
                return "Request timed out."

            receiving_time = time.time()
            packet, address = sock.recvfrom(1024)
            icmp_header = packet[20:28]
            icmp_type, code, checksum, packet_id, sequence = struct.unpack("bbHHh", icmp_header)

            if icmp_type != 8 and packet_id == self.process_id:
                byte_array = struct.calcsize("d")
                sending_time = struct.unpack("d", packet[28: 28 + byte_array])[0]
                return receiving_time - sending_time

            timeout = timeout - difference

            if timeout <= 0:
                return "Request timed out."

    def send_packet(self):
        sock = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP)
        sock.sendto(self.buffer.get(), (self.destination_address, 1))
        sock.close()

    def process_buffer(self, *functions):
        processes = []

        for function in functions:
            process = Process(target=function)
            process.start()
            processes.append(process)

        for process in processes:
            process.join()

    def send_message(self, message):
        for bit in message:
            time.sleep(self.TIME_INTERVAL - int(bit))
            self.process_buffer(self.prepare_packet, self.send_packet)


if __name__ == "__main__":
    channel = Channel(sys.argv[1])
    channel.send_message(sys.argv[2])