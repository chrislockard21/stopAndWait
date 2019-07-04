def stringToBinary(string):
    '''
    Converts string to a list of 16 bit binary values. The string is
    first converted to a sha224 hash value to simulate hashing in the UDP
    protocol.

    Accepts a string or payload of data.
    '''
    import re
    words = re.findall(r'..', string)
    bitWords = []
    for word in words:
        bits = ''
        for w in word:
            bits += bin(ord(w))[2:].zfill(8)
        bitWords.append(bits)
    return bitWords


def onesCompliment(*args, type):
    '''
    Calculates the ones compliment of a string by adding the 16 bit binary
    strings, accounting for wrap around 1s and flipping 1s and 0s in the
    output value.

    Accepts a list of 16 bit binary strings.
    '''
    if len(args) != 0:
        sumBinary = args[0]
        i = 1
        while i < len(args):
            sumBinary = bin(int(sumBinary, 2) + int(args[i], 2))[2:]
            if len(sumBinary) > 16:
                sumBinary = bin(int(sumBinary[1:], 2) + int('0000000000000001', 2))[2:].zfill(16)
            i += 1
        if type == 'data':
            return ''.join(['0' if num == '1' else '1' for num in sumBinary])
        elif type == 'ack':
            return ''.join(sumBinary)
        else:
            return None
    else:
        return None

if __name__ == '__main__':
    pass
