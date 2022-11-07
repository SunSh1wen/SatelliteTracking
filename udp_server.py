from socketserver import TCPServer
import struct
import socket
from typing import Text
import logging
import sys
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.settimeout(1.0)
udp_addr = '192.168.50.48'

#logging.basicConfig(
#    level=logging.INFO,
#    format="%(asctime)s [%(levelname)s] %(message)s",
#    handlers=[
#        logging.FileHandler("cmd-log.txt"),
#        logging.StreamHandler(sys.stdout)
#    ]
#)

#------------------------------------------------------------------
def build_command(address, cmd, data1, data2):
    sync = 0xff
    b = [sync, address, 0, cmd, data1, data2]
    crc = sum(b[1:]) % 256
    b.append(crc)
    logging.info(str(b))
    return struct.pack("7B", *b)
#------------------------------------------------------------------

def rotate_to_degree(address, deg, hori=True):
    deg = int(deg * 100) if hori else int(min(deg, 60) * 100)

    #logging.info(f"Rotote to {deg/100} {'hori' if hori else 'vert'}")
    if (deg < 0):
        arg1, arg2 = deg.to_bytes(2, 'big', signed=True)
    else:
        arg1 = (deg >> 8)
        arg2 = (deg & 0xff)
    cmd = 0x4b if hori else 0x4d
    udp_socket.sendto(build_command(address, cmd, arg1, arg2), (udp_addr, 6666))
    try:
        data, server = udp_socket.recvfrom(1024)
    except socket.timeout:
        print('REQUEST TIMED OUT')
        raise

def get_degree(address, hori=True):
    cmd = 0x51 if hori else 0x53
    udp_socket.sendto(build_command(address, cmd, 0 ,0), (udp_addr, 6666))
    try:
        data, server = udp_socket.recvfrom(1024)
        val = (struct.unpack(">H", data[4:6])[0] / 100) if hori else (struct.unpack(">h", data[4:6])[0] / 100)
        #logging.info(f"Get degree {val/100} {'hori' if hori else 'vert'}")
        return val
    except socket.timeout:
        print('REQUEST TIMED OUT')
        raise

def turn_left(address, H_speed):
    cmd = 0x04
    udp_socket.sendto(build_command(address, cmd, int(H_speed*10), 0) , (udp_addr, 6666))
    try:
        data, server = udp_socket.recvfrom(1024)
    except socket.timeout:
        print('REQUEST TIMED OUT')
        raise

def turn_right(address, H_speed):
    cmd = 0x02
    udp_socket.sendto(build_command(address, cmd, int(H_speed*10), 0 ), (udp_addr, 6666))
    try:
        data, server = udp_socket.recvfrom(1024)
    except socket.timeout:
        print('REQUEST TIMED OUT')
        raise

def turn_up(address, V_speed):
    cmd = 0x08
    udp_socket.sendto(build_command(address, cmd, 0, int(V_speed*10)) , (udp_addr, 6666))
    try:
        data, server = udp_socket.recvfrom(1024)
    except socket.timeout:
        print('REQUEST TIMED OUT')
        raise

def turn_down(address, V_speed):
    cmd = 0x10
    udp_socket.sendto(build_command(address, cmd, 0, int(V_speed*10)) , (udp_addr, 6666))
    try:
        data, server = udp_socket.recvfrom(1024)
    except socket.timeout:
        print('REQUEST TIMED OUT')
        raise

def rotator_stop(address=1):
    cmd = 0x00
    udp_socket.sendto(build_command(address, cmd, 0, 0) , (udp_addr, 6666))
    try:
        data, server = udp_socket.recvfrom(1024)
    except socket.timeout:
        print('REQUEST TIMED OUT')
        raise

if __name__ == "__main__":
    print(build_command(1, 0x51))
    udp_socket.sendto(build_command(1, 0x51), (udp_addr, 6666))
    try:
        data, server = udp_socket.recvfrom(1024)
        val = struct.unpack(">h", data[4:6])[0] / 100
        print(f'{data} {val}')

    except socket.timeout:
        print('REQUEST TIMED OUT')

