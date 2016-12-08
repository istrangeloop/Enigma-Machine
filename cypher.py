#!/usr/bin/python

import argparse, sys
ALPHABET_SIZE = 26
parser = argparse.ArgumentParser(description='Encrypts a message from a text file.')
parser.add_argument('walzenlage1', metavar='w1', type=int, action='store',
                    help='')

parser.add_argument('walzenlage2', metavar='w2', type=int, action='store',
                    help='')

parser.add_argument('walzenlage3', metavar='w3', type=int, action='store',
                    help='')
parser.add_argument('ringstellung', metavar='rs', type=str, action='store',
                    help='')
#parser.add_argument('--decrypt', nargs='?', const=decrypt, default=encrypt,
                    #help='decrypts the message')
parser.add_argument('file', metavar='filename', type=str,
                    help='name or path to the file wich contains your message')
args = parser.parse_args()

text = open(args.file, 'r')
msg = text.read()
lenmsg = len(msg)
w1 = args.walzenlage1
w2 = args.walzenlage2
w3 = args.walzenlage3
rs1 = args.ringstellung
#inicia os rotores
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
            self.rotate
    def do(self, previousOut):
        if previousOut < 0:
            pass
        return self.numbers[previousOut]

#inicia a maquina baseada na configuração da chave
class Enigma:
    counter = [0, 0, 0]
    def __init__(self, r1, r2, r3, ref):
        self.r1 = r1
        self.r2 = r2
        self.r3 = r3
        self.ref = ref
    def ringset(self, rs):
        self.r1.set(int(rs[0])-96)
        self.r2.set(int(rs[1])-96)
        self.r3.set(int(rs[2])-96)
    def encrypt(self, message):
        EncryptedMessage = []
        for i in message:
            EncryptedMessage.append(self.newLetter(ord(i.lower())-96, message))
            self.rotateAll()
        return EncryptedMessage
#    def decrypt(self, message)
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

E = Enigma(Rotor(w1), Rotor(w2), Rotor(w3), Rotor('Reflector'))
E.ringset(rs)
print(E.r1)
