from math import floor
from onesCompliment import stringToBinary, onesCompliment
import socket
import struct
import sys
import os
from multiprocessing.pool import ThreadPool
import time


def rdt_send(MSS, fileObj, seqNum, byte):
    '''
    Function to buffer and compile a message at a max size of the specified
    MSS by reading a file specified in the CLI.

    Accepts MSS and filename.
    '''
    # Gathers the segments to pack
    for i in range(0, MSS-1):
        byte += f.read(1)

    # Converting string to 16 bit binary strings
    binaryList = stringToBinary(byte)

    # Computing checksum
    checksum = onesCompliment(*binaryList, type='data')

    if checksum != None:
        # Specifies data packet
        dataPkt = '0101010101010101'

        return seqNum, checksum, dataPkt, byte
    else:
        return None


def unpack(pkt):
    '''
    Function to unpack the pkt tuple to an encoded string
    '''
    send_seqNum = bin(int(pkt[0]))[2:].zfill(32)
    send_checksum = pkt[1]
    send_dataPkt = pkt[2]
    send_data = pkt[3]
    formatPkt = '{}\n{}{}\n-----\n{}'.format(
        send_seqNum, send_dataPkt,
        send_checksum, send_data
    )
    return formatPkt.encode()


def thread_send(pkt, host):
    '''
    Thread to send UDP segment
    '''
    data = unpack(pkt)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(0.1)
    sent = sock.sendto(data, host)
    while True:
        try:
            dataRecv, host = sock.recvfrom(2048)
            return dataRecv.decode(), host
        except socket.timeout:
            print('Timeout', pkt[0])
            return None, host


def multicast(pkt, hosts):
    '''
    Function to start threads and multicast to all listed hosts
    '''
    # Assigns process count to pool of threads
    pool = ThreadPool(processes=5)
    # List comprehension to gather thread outputs
    threads = [
        pool.apply_async(thread_send, (pkt, host)).get() for host in hosts
    ]
    pool.close()
    return threads


def parse_response(*args, seqNum):
    '''
    Parses the thread responses to locate threads for another transfer
    '''
    resend_list = []
    for arg in args:
        # print(arg)
        if arg[0] == None or int(arg[0].split('\n')[0], 2) != seqNum:
            resend_list.append(arg[1])
    return resend_list


if __name__ == '__main__':
    start = time.time()
    # Main code
    arguments = sys.argv
    MSS = int(arguments.pop())
    filename = arguments.pop()
    port = int(arguments.pop())
    del arguments[0]

    # Can be any IP above 172.17.0.2 which is running the client
    hosts = []
    for arg in arguments:
        hosts.append((arg, port))

    seqNum = 0
    f = open(filename, 'r')
    byte = f.read(1)
    sum = 0
    while byte:
        # Pack the data
        pkt = rdt_send(MSS, f, seqNum, byte)
        # If there are still packets to be sent
        if pkt == None:
            break
        else:
            # Send the data
            thread_out = multicast(pkt, hosts)
            # Find any non ack'd segments
            resend_hosts = parse_response(*thread_out, seqNum=seqNum)
            while len(resend_hosts) > 0:
                # Result of resending threads
                thread_out = multicast(pkt, resend_hosts)
                # Calculates the hosts that need to be resent
                resend_hosts = parse_response(*thread_out, seqNum=seqNum)
            seqNum += 1
            byte = f.read(1)

    f.close()
    end = time.time() - start
    print('Total time:', end)
