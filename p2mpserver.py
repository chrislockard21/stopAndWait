import socket
import random
import sys
from onesCompliment import stringToBinary, onesCompliment

def ack(ackNum):
    '''
    Function to buld the ack segment
    '''
    ackChecksum = '0000000000000000'
    ackpkt = '1010101010101010'
    formatpkt = '{}\n{}{}\n-----\nACK'.format(
        ackNum, ackpkt, ackChecksum
    ).encode()
    return formatpkt


if __name__ == '__main__':

    auguments = sys.argv

    port = auguments[1]
    filename = auguments[2]
    p = float(auguments[3])

    # Runs code when it is called

    # Address for the server to bind too
    server_address = ('', int(port))

    # UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Binds socket to server address
    sock.bind(server_address)

    # Opens the file to be received
    f = open(filename, 'w')

    # Collects the sequence numbers
    cache = []

    # The next expected sequence number
    seqNumExp = 0

    # Listen for transmissions
    while True:
        try:
            # Data received
            data, addr = sock.recvfrom(1024)

            # Calculates random number number and compares it to thre
            if random.uniform(0, 1) >= p:
                # Received data
                dataRecv = data.decode().split('\n-----\n')

                # Gets sequence number from the data
                seqNum = int(dataRecv[0].split('\n')[0], 2)

                # Gets pkt type from data
                pktType = dataRecv[0].split('\n')[1][:16]

                # Gets checksum from data
                checksumRecv = dataRecv[0].split('\n')[1][16:]

                # Gets the payload
                dataToCommit = dataRecv[-1]

                if seqNum == seqNumExp:
                    sumBinary = stringToBinary(dataToCommit)
                    checksum = onesCompliment(*sumBinary, type='ack')
                    if bin(int(checksumRecv, 2) + int(checksum, 2))[2:].find('0') == -1:
                        # Adds seqNum to the cache to indicate that it has been
                        # received
                        cache.append(seqNum)
                        # Next expected seq number
                        seqNumExp += 1
                        # Writes data to the file
                        f.write(dataToCommit)
                        ackNum = bin(seqNum)[2:].zfill(32)
                        formatpkt = ack(ackNum)
                        sock.sendto(formatpkt, addr)
                    else:
                        pass
                else:
                    # Gets previous ack and sends the packet
                    ackNum = cache[-1]
                    formatpkt = ack(ackNum)
                    sock.sendto(formatpkt, addr)
            else:
                # Indicates that the packet is lost
                print('Packet lost', int(data.decode().split('\n')[0], 2))

        # Breaks out of the loop only catching a KeyboardInterrupt
        except KeyboardInterrupt:
            break

    f.close()
