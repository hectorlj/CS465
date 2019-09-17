# Hector Lopez
# 65-764-0379
# AES
# September 16, 2019
import numpy as np
import copy as copy

def Cipher (key, data):
    print("\nCIPHER (ENCRYPT):")
    print("round[0].input\t"+hexToKey(data.transpose()))
    Nb = 4
    expandedKey = KeyExpansion(key)
    data = AddRoundKey(data.transpose(), expandedKey[0:4])
    print("round[0].k_sch\t"+hexToKey(data))
    for i in range(Nr-1):
        currRound = str(i+1)
        print("round["+currRound+"].start\t\t"+hexToKey(data))
        data = SubBytes(data)
        print("round["+currRound+"].s_box\t\t"+hexToKey(data))
        data = ShiftRows(data)
        print("round["+currRound+"].s_row\t\t"+hexToKey(data))
        data = MixColumns(data)
        print("round["+currRound+"].m_col\t\t"+hexToKey(data))
        data = AddRoundKey(data, expandedKey[((i + 1) * 4):(((i + 1) * 4) + 4)])
        printRound(i, expandedKey)

    print("round["+str(Nr)+"].start\t"+hexToKey(data))
    data = SubBytes(data)
    print("round["+str(Nr)+"].s_box\t"+hexToKey(data))
    data = ShiftRows(data)
    print("round["+str(Nr)+"].s_row\t"+hexToKey(data))
    data = AddRoundKey(data, expandedKey[Nr*4 : (Nr+1) * 4])
    printRound(Nr-1, expandedKey)
    print("round["+str(Nr)+"].output\t"+hexToKey(data))

    return data

def InvCipher(key, data):
    print("\nINVERSE CIPHER (DECRYPT):")
    print("round[0].iinput\t\t"+hexToKey(data))
    expandedKey = KeyExpansion(key)
    printRound(Nr, expandedKey, 0)
    data = AddRoundKey(data, expandedKey[Nr*4:(Nr+1)*4])
    y = Nr - 1
    for i in range(Nr-1):
        currRound = str(i+1)
        print("round["+currRound+"].istart\t\t"+hexToKey(data))
        data = InvShiftRows(data)
        print("round["+currRound+"].is_row\t\t"+hexToKey(data))
        data = InvSubBytes(data)
        print("round["+currRound+"].is_box\t\t"+hexToKey(data))
        data = AddRoundKey(data, expandedKey[y*4 : (y*4) + 4])
        printRound(y, expandedKey, i + 1)
        print("round["+str(Nr)+"].ik_add\t"+hexToKey(data))
        data = InvMixColumns(data)
        print("round["+currRound+"].im_col\t\t"+hexToKey(data))
        y-=1
    
    print("round["+str(Nr)+"].istart\t"+hexToKey(data))
    data = InvShiftRows(data)
    print("round["+str(Nr)+"].is_row\t"+hexToKey(data))
    data = InvSubBytes(data)
    print("round["+str(Nr)+"].is_box\t"+hexToKey(data))
    data = AddRoundKey(data, expandedKey[0:4])
    print("round["+str(Nr)+"].ik_add\t"+hexToKey(data))

    printRound(0, expandedKey, Nr)
    print("round["+str(Nr)+"].ioutput\t"+hexToKey(data))
    return data.transpose()


def KeyExpansion(key):
    Nb = 4
    i = 0
    answer = []
    while i < Nk:
        byte_array = bytearray([key[(4*i)], key[(4*i)+1], key[(4*i)+2], key[(4*i)+3]])
        answer.append(int.from_bytes(byte_array, byteorder="big", signed=False))
        i = i + 1
    i = Nk

    while i < Nb * (Nr+1):
        word = answer[i-1]
        if i % Nk == 0:
            word = SubWord(RotWord(word)) ^ Rcon[i//Nk]
        elif (Nk > 6) and (i % Nk == 4):
            word = SubWord(word)
        answer.append(answer[i-Nk] ^ word)
        i = i + 1
    return answer

def SubWord(word):
    obj = word.to_bytes(4, byteorder="big", signed=False)
    array = []
    for i in range(4):
        byte = obj[i]
        array.append(Sbox[byte >> 4][byte & 0x0f])
    return int.from_bytes(array, byteorder="big", signed=False)

def RotWord(word):
    obj = word.to_bytes(4, byteorder="big", signed=False)
    array = []
    array.append(obj[1])
    array.append(obj[2])
    array.append(obj[3])
    array.append(obj[0])
    return int.from_bytes(array, byteorder="big", signed=False)

def Xtime(word):
    if word & 0x80:
        return (word << 1) ^ 0x11b
    return word << 1

def FFMultiply(a, b):
    answer = 0
    # array of bits right shifted from b
    right_bits = [(b >> bit) & 1 for bit in range(8)]
    for i in range(len(right_bits)):
        if right_bits[i] & 0x01:
            answer = answer ^ a
        a = Xtime(a)
    return answer

def SubBytes(state):
    for i in range(len(state)):
        for j in range(len(state[i])):
            byte = state[i][j]
            state[i][j] = Sbox[byte >> 4][byte & 0x0f]
    return state

def InvSubBytes(state):
    for i in range(len(state)):
        for j in range(len(state[i])):
            byte = state[i][j]
            state[i][j] = InverseSbox[byte >> 4][byte & 0x0f]
    return state

def ShiftRows(state):
    for i in range(len(state)):
        temp = copy.deepcopy(state[i])
        if i is 1:
            state[i][0] = temp[1]
            state[i][1] = temp[2]
            state[i][2] = temp[3]
            state[i][3] = temp[0]
        elif i is 2:
            state[i][0] = temp[2]
            state[i][1] = temp[3]
            state[i][2] = temp[0]
            state[i][3] = temp[1]
        elif i is 3:
            state[i][0] = temp[3]
            state[i][1] = temp[0]
            state[i][2] = temp[1]
            state[i][3] = temp[2]
    return state

def InvShiftRows(state):
    for i in range(len(state)):
        temp = copy.deepcopy(state[i])
        if i is 1:
            state[i][0] = temp[3]
            state[i][1] = temp[0]
            state[i][2] = temp[1]
            state[i][3] = temp[2]
        elif i is 2:
            state[i][0] = temp[2]
            state[i][1] = temp[3]
            state[i][2] = temp[0]
            state[i][3] = temp[1]
        elif i is 3:
            state[i][0] = temp[1]
            state[i][1] = temp[2]
            state[i][2] = temp[3]
            state[i][3] = temp[0]
    return state

def MixColumns(state):
    # columns are now rows
    state = state.transpose()
    for i in range(len(state)):
        temp = copy.deepcopy(state[i])
        state[i][0] = FFMultiply(temp[0], 0x02) ^ FFMultiply(temp[1], 0x03) ^ temp[2] ^ temp[3]
        state[i][1] = temp[0] ^ FFMultiply(temp[1], 0x02) ^ FFMultiply(temp[2], 0x03) ^ temp[3]
        state[i][2] = temp[0] ^ temp[1] ^ FFMultiply(temp[2], 0x02) ^ FFMultiply(temp[3], 0x03)
        state[i][3] = FFMultiply(temp[0], 0x03) ^ temp[1] ^ temp[2] ^ FFMultiply(temp[3], 0x02)
    # revert rows to columns
    return state.transpose()

def InvMixColumns(state):
    # columns are now rows
    state = state.transpose()
    for i in range(len(state)):
        temp = copy.deepcopy(state[i])
        state[i][0] = FFMultiply(temp[0], 0x0e) ^ FFMultiply(temp[1], 0x0b) ^ FFMultiply(temp[2], 0x0d) ^ FFMultiply(temp[3], 0x09)
        state[i][1] = FFMultiply(temp[0], 0x09) ^ FFMultiply(temp[1], 0x0e) ^ FFMultiply(temp[2], 0x0b) ^ FFMultiply(temp[3], 0x0d)
        state[i][2] = FFMultiply(temp[0], 0x0d) ^ FFMultiply(temp[1], 0x09) ^ FFMultiply(temp[2], 0x0e) ^ FFMultiply(temp[3], 0x0b)
        state[i][3] = FFMultiply(temp[0], 0x0b) ^ FFMultiply(temp[1], 0x0d) ^ FFMultiply(temp[2], 0x09) ^ FFMultiply(temp[3], 0x0e)
    # revert rows to columns
    return state.transpose()

# FIXME: 
def AddRoundKey(state, key):
    # columns are now rows
    state = state.transpose()
    for i in range(len(state)):
        state[i][0] = state[i][0] ^ (key[i] >> 24)
        state[i][1] = state[i][1] ^ ((key[i] >> 16) & 0x00ff)
        state[i][2] = state[i][2] ^ ((key[i] >> 8) & 0x0000ff)
        state[i][3] = state[i][3] ^ (key[i] & 0x000000ff)
    # revert rows to columns
    return state.transpose()


def keyToHex(string):
    key = []
    array = bytes.fromhex(string)
    for i in array:
        key.append(i)
    return key

def hexToKey(state):
    key = ""
    state = state.transpose()
    for i in state:
        for j in i:
            key += str(format(j, 'x'))
    return key


def printRound(i, key, currRound=None):
    if currRound is None :
        print("round["+str(i+1)+"].k_sch\t\t"+str(format(key[(i+1)*4], 'x'))+
        str(format(key[(((i+1)*4)+1)], 'x'))+
        str(format(key[(((i+1)*4)+2)], 'x'))+
        str(format(key[(((i+1)*4)+3)], 'x')))
    else:
        # Inverse round
        print("round["+str(currRound)+"].ik_sch\t\t"+str(format(key[i*4], 'x'))+
        str(format(key[((i*4)+1)], 'x'))+
        str(format(key[((i*4)+2)], 'x'))+
        str(format(key[((i*4)+3)], 'x')))
    

Sbox = np.array([
    [0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76],
    [0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0],
    [0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15],
    [0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75],
    [0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84],
    [0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf],
    [0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8],
    [0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2],
    [0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73],
    [0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb],
    [0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79],
    [0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08],
    [0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a],
    [0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e],
    [0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf],
    [0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16]
])

InverseSbox = np.array([
    [0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb],
    [0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb],
    [0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e],
    [0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25],
    [0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92],
    [0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84],
    [0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06],
    [0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b],
    [0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73],
    [0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e],
    [0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b],
    [0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4],
    [0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f],
    [0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef],
    [0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61],
    [0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d]
])

Rcon = [0x00000000, 0x01000000, 0x02000000, 0x04000000, 0x08000000, 0x10000000, 0x20000000, 0x40000000, 0x80000000, 0x1B000000, 0x36000000, 
        0x6C000000, 0xD8000000, 0xAB000000, 0x4D000000, 0x9A000000, 0x2F000000, 0x5E000000, 0xBC000000, 0x63000000, 0xC6000000, 0x97000000, 
        0x35000000, 0x6A000000, 0xD4000000, 0xB3000000, 0x7D000000, 0xFA000000, 0xEF000000, 0xC5000000, 0x91000000, 0x39000000, 0x72000000,
        0xE4000000, 0xD3000000, 0xBD000000, 0x61000000, 0xC2000000, 0x9F000000, 0x25000000, 0x4A000000, 0x94000000, 0x33000000, 0x66000000, 
        0xCC000000, 0x83000000, 0x1D000000, 0x3A000000, 0x74000000, 0xE8000000, 0xCB000000, 0x8D000000
        ]


Nk = 4
Nr = 10

plaintext = "00112233445566778899aabbccddeeff"
keyString = "000102030405060708090a0b0c0d0e0f"
originalPlaintextArray = np.array([
    [0x00, 0x11, 0x22, 0x33],
    [0x44, 0x55, 0x66, 0x77],
    [0x88, 0x99, 0xaa, 0xbb],
    [0xcc, 0xdd, 0xee, 0xff] 
])

plaintextArray = copy.deepcopy(originalPlaintextArray)
key = keyToHex(keyString)
print("Plaintext: \t", plaintext)
print("Key: \t\t", keyString)

encryptedText = Cipher(key, plaintextArray)
decryptedText = InvCipher(key, encryptedText)

print("\nTest Passed!" if hexToKey(decryptedText) == hexToKey(originalPlaintextArray) else "Test Failed\n")


Nk = 6
Nr = 12
plaintextArray = copy.deepcopy(originalPlaintextArray)

keyString = "000102030405060708090a0b0c0d0e0f1011121314151617"
key = keyToHex(keyString)
print("Plaintext: \t", plaintext)
print("Key: \t\t", keyString)
encryptedText = Cipher(key, plaintextArray)
decryptedText = InvCipher(key, encryptedText)
print("\nTest Passed!" if hexToKey(decryptedText) == hexToKey(plaintextArray) else "Test Failed\n")

Nk = 8
Nr = 14
plaintextArray = copy.deepcopy(originalPlaintextArray)

keyString = "000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f"
key = keyToHex(keyString)
print("Plaintext: \t", plaintext)
print("Key: \t\t", keyString)

encryptedText = Cipher(key, plaintextArray)
decryptedText = InvCipher(key, encryptedText)
decrypt = decryptedText
plain = plaintextArray
print("\nTest Passed!" if hexToKey(decryptedText) == hexToKey(plaintextArray) else "Test Failed\n")