def sha1(data, h0, h1, h2, h3, h4, defaultLength=0):
    bytes = ""

    for x in range(len(data)):
        bytes += '{0:08b}'.format(ord(data[x]))
    bits = bytes + "1"
    tempBits = bits

    while len(tempBits) % 512 != 448:
        tempBits = tempBits + "0"
    tempBits = tempBits + '{0:064b}'.format(len(bits) - 1 + defaultLength)
    hexdata = hex(int(tempBits, 2))
    

    for x in chunks(tempBits, 512):
        m = chunks(x, 32)
        w = [0] * 80
        for y in range(0, 16):
            w[y] = int(m[x], 2)
        for y in range(16, 80):
            w[y] = rol((w[y - 3] ^ w[y - 8] ^ w[y - 14] ^ w[ y - 16]), 1)
    a = h0
    b = h1
    c = h2
    d = h3
    e = h4

    for x in range(0, 80):
        if 0 <= x <=19:
            f = (b & c) | ((~b) & d)
            k = 0x5A827999
        elif 20 <= x <=39:
            k = 0x6ed9eba1
        elif 40 <= x <= 59:
            k = 0x8f1bbcdc
        elif 60 <= x <= 79:
            k = 0xca62c1d6

def chunks(l, n):
    return [l[i:i+n] for i in range(0, len(l), n)]

def rol(n, b):
    return ((n << b) | (n >> (32-b))) & 0xffffffff

macHexDigest = 'f4b645e89faaec2ff8e443c595009c16dbdfba4b'