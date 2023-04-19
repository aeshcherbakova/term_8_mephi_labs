from scapy.all import *
import socket
from config import *
# client outside the IS who recieves the legal info as well as secrete message that was added by proxy


print("Client 2 has started")
random.seed(1000000)
soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # udp - "socket.SOCK_DGRAM", tcp - Stream
soc.bind(SECOND_CLIENT_ADDRESS)
soc.connect(PROXY_ADDRESS)


def listener():
    cur_i = 0
    bits_of_msg = ''
    while True:
        data = soc.recv(10240)
        #pac = sniff(filter="src port 65012 and dst port 65011")
        #print(pac)
        print(len(data))
        bits_of_msg += decoder(data, cur_i)
        cur_i += 1
        if cur_i == K // W:
            print('Bits of msg:', bits_of_msg)
            print('Decoded msg:', ''.join([chr(int(bits_of_msg[i:i+8], 2)) for i in range(0, len(bits_of_msg), 8)]))
            break


def decoder(msg, cur_i):
    l_next = len(msg)
    l_max = 0
    all_ls = []
    with open('Dictionary.txt', 'r') as f:
        all_ls = f.read().split('\n')
        l_max = int(all_ls[cur_i])

    sum_i = l_next - l_max
    w_i = sum_i
    if cur_i % 2 == 0:
        w_i += 2 ** (W - 1)
    else:
        w_i += (2 ** (W - 1) - 1)
    return format(w_i, f'0{W}b')


if __name__ == '__main__':
    listener()
