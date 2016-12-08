#!/usr/bin/python

import argparse, sys
ALPHABET_SIZE = 26
parser = argparse.ArgumentParser(description='Encrypts a message from a text file.')
parser.add_argument('walzenlage1', metavar='walzenlage1', type=int, action='store',
                    help='number of the rotor to use for position 1')

parser.add_argument('walzenlage2', metavar='walzenlage2', type=int, action='store',
                    help='number of the rotor to use for position 2')

parser.add_argument('walzenlage3', metavar='walzenlage3', type=int, action='store',
                    help='number of the rotor to use for position 3')
parser.add_argument('ringstellung', metavar='ringstellung', type=str, action='store',
                    help='three letters to be at the initial position of the ring')
parser.add_argument('--decrypt', nargs='?',
                    help='add this argument to decrypt the message')
parser.add_argument('filei', metavar='Input', nargs='?', type=str,
                    help='name or path to the file wich contains your message. Leave blank if stdin')
parser.add_argument('fileo', metavar='Output', nargs='?', type=str,
                    help='name or path to the file wich you\'d like to print the output. Leave blank if stdout')
args = parser.parse_args()

# machine classes
class Rotor:
    config = {'1':[13, 17, 21, 16, 15, 24, 9, 25, 4, 18, 14, 8, 0, 20, 10, 19, 11, 1, 12, 22, 3, 6, 23, 5, 7, 2],
              '2':[17, 8, 18, 2, 11, 1, 6, 19, 24, 10, 16, 14, 7, 4, 23, 13, 0, 25, 20, 12, 22, 5, 9, 15, 21, 3],
              '3':[24, 16, 13, 0, 18, 12, 3, 25, 21, 8, 10, 15, 22, 2, 6, 7, 5, 17, 14, 1, 9, 11, 20, 23, 4, 19],
              'Reflector':[14, 18, 1, 19, 25, 21, 5, 3, 24, 7, 8, 23, 4, 0, 9, 15, 6, 16, 12, 13, 10, 22, 20, 2, 17, 11]
              }
    def __init__(self, Id):
        self.len = ALPHABET_SIZE
        self.numbers = self.config[Id]
    def rotate(self):
        init = self.numbers[0]
        for index in range (0, self.len-1):
            self.numbers[index] = self.numbers[index+1]
        self.numbers[self.len-1] = init
    def set(self, rs):
        while self.numbers[0] != rs:
            self.rotate()
    def do(self, previousOut):
        if previousOut < 0:
            return -65
        return self.numbers[previousOut]

class Enigma:
    counter = [0, 0, 0]
    def __init__(self, r1, r2, r3, ref):
        self.r1 = r1
        self.r2 = r2
        self.r3 = r3
        self.ref = ref
    def ringset(self, rs):
        self.r1.set(ord(rs[0])-96)
        self.r2.set(ord(rs[1])-96)
        self.r3.set(ord(rs[2])-96)
    def encrypt(self, message):
        EncryptedMessage = []
        for i in message:
            EncryptedMessage.append(self.newLetter(ord(i.lower())-96))
            self.rotateAll()
        NewMessage = ''.join(chr(i + 97) for i in EncryptedMessage)
        return NewMessage
    def decrypt(self, message):
        pass
    def newLetter(self, num):
        return self.r1.do(self.r2.do(self.r3.do(self.ref.do(self.r3.do(self.r2.do(self.r1.do(num)))))))
    def rotateAll(self):
        self.r1.rotate()
        self.counter[0] = self.counter[0] + 1
        if self.counter[0] == ALPHABET_SIZE:
            self.r2.rotate()
            self.counter[1] = self.counter[1] + 1
            self.counter[0] = 0
            if self.counter[1] == ALPHABET_SIZE:
                self.r3.rotate()
                self.counter[2] = self.counter[2] + 1
                self.counter[1] = 0

#input treatment
if args.filei:
    text = open(args.filei, 'r')
    msg = text.read()
else: msg = input()
lenmsg = len(msg)
w1 = args.walzenlage1
w2 = args.walzenlage2
w3 = args.walzenlage3
rs = args.ringstellung

#setup
E = Enigma(Rotor(str(w1)), Rotor(str(w2)), Rotor(str(w3)), Rotor('Reflector'))
E.ringset(rs)
EncryptedMessage = E.encrypt(msg)
if args.fileo:
    outext = open(args.fileo, 'w')
    outext.write(EncryptedMessage)
else: print (EncryptedMessage)
