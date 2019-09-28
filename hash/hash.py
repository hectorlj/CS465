import hashlib
import string
import random as rand 

# time = 2**(n/2) n = bits
def collision (n):
    temp = string.hexdigits
    count = ''.join(rand.choice(temp) for i in range(20))
    hashSet = set()
    counter = -1
    while 1:
        newhash = hash(count, n)
        count = str(hex(int(count, 16) + 1))
        counter = counter + 1
        if newhash in set(hashSet):
            return counter
        hashSet.add(newhash)

# time = 2**n n = bits
def preimage (hashString, n):
    prehash = hash(hashString, n)
    temp = string.hexdigits
    count = ''.join(rand.choice(temp) for i in range(10))
    newHash = ''
    counter = 0
    while prehash != newHash:
        newHash = hash(count, n)
        count = str(hex(int(count, 16) + 1))
        counter = counter + 1
    return counter

def hash(myString, n):
    myString = bytes(myString, 'utf-8')
    hash = hashlib.sha1(myString).hexdigest()
    binaryHash = bin(int(hash, 16))[2:]
    shortHash = binaryHash[0:n + 1]
    return shortHash

n = 16
# while n < 33:

expectedPreimage = 2**n
expectedCollision = 2**(n/2)
totalTrials = 100
currTrial = 0
x = 0
average = 0
for x in range(totalTrials):
    currTrial = preimage("hello there", n)
    average = average + currTrial

print("n = ", str(n), "\n Average preimage: ", str(average/totalTrials), " \n Expected preimage: ", str(expectedPreimage))

average = 0
currTrial = 0
x = 0

for x in range(totalTrials):
    currTrial = collision(n)
    average = average + currTrial

print("n = ", str(n), "\n Average collision: ", str(average/totalTrials), " \n Expected collision: ", str(expectedCollision))

    # n = n + 4