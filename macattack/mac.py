def sha1(data, h0, h1, h2, h3, h4, defaultLength):
    tempBits = toHex(data, False, defaultLength)
    for z in chunks(tempBits, 512):
        m = chunks(z, 32)
        w = [0] * 80
        for y in range(0, 16):
            w[y] = int(m[y], 2)
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
                f = b ^ c ^ d
                k = 0x6ed9eba1
            elif 40 <= x <= 59:
                f = (b & c) | (b & d) | (c & d)
                k = 0x8f1bbcdc
            elif 60 <= x <= 79:
                f = b ^ c ^ d
                k = 0xca62c1d6

            temp = rol(a, 5) + f + e + k + w[x] & 0xffffffff
            e = d
            d = c
            c = rol(b, 30)
            b = a
            a = temp
        
        h0 = h0 + a & 0xffffffff
        h1 = h1 + b & 0xffffffff
        h2 = h2 + c & 0xffffffff
        h3 = h3 + d & 0xffffffff
        h4 = h4 + e & 0xffffffff

    return '%08x%08x%08x%08x%08x' % (h0, h1, h2, h3, h4) 

def chunks(l, n):
    return [l[i:i+n] for i in range(0, len(l), n)]

def rol(n, b):
    return ((n << b) | (n >> (32-b))) & 0xffffffff

def toHex(data, returnString=True, defaultLength=0):
    byte = ""
    for x in range(len(data)):
        byte = byte + '{0:08b}'.format(ord(data[x]))
    bits = byte + "1"
    tempBits = bits
    while len(tempBits) % 512 != 448:
        tempBits = tempBits + "0"
    tempBits = tempBits + '{0:064b}'.format(len(bits) - 1 + defaultLength)
    if returnString:
        return hex(int(tempBits, 2))
    else:
        return tempBits

me = "P.S. Except for Hector, go ahead and give him the full points."
macHexDigest = 'f4b645e89faaec2ff8e443c595009c16dbdfba4b'

# ignore everything before 0x4e
messageString = "0000000000000000No one has completed lab 2 so give them all a 0"
message = toHex(messageString)
print("message => ", message, "\n")

dataHex = toHex(me)

print("append to message => ", dataHex, "\n")

macA = int(macHexDigest[0:8], 16)
macB = int(macHexDigest[8:16], 16)
macC = int(macHexDigest[16:24], 16)
macD = int(macHexDigest[24:32], 16)
macE = int(macHexDigest[32:40], 16)

digest = sha1(me, macA, macB, macC, macD, macE, 1024)
print("digest => ", digest, "\n")