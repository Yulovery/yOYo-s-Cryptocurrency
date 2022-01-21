#yOYo's Crypto 1
#Dec 14 2pm - 3pm

from collections import UserDict
from hashlib import sha256
import base64
from itertools import starmap
from os import nice
from signal import siginterrupt
from typing import Optional
import pickle
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

genesis_hash = 'yoyo' + "0" * 42

def updatehash(*args):                  #create and return a ahsh based on the information given
    hashing_text = "" #instance of the imported hash "class"
    #h =sha256()
    for arg in args:
        hashing_text += str(arg)
    h = sha256(hashing_text.encode('utf-8'))
    return base64.b64encode(h.digest()).decode('utf-8')
    #h.update(hashing_text.encode('utf-8'))
    #return h.hexdigest()
        # print (hashing_text.encode('utf-8'))
        # print (h.digest())
        # print (h.hexdigest())

def loadChain(handel = 'yOChain.p'):
    with open(handel, 'rb') as inp:
        yc = pickle.load(inp)
        print ('The Chain Object is called: yc', yc)
    return yc


# see who has the longest chain, aka the valid one
def compareValid(blockchain1, blockchain2):
    if blockchain1.isValid() == True:
        if blockchain2.isValid() == True:
            if len(blockchain1.chain) > len(blockchain2.chain):
                print (blockchain1, ' is the longest and valid one')
            else:
                print (blockchain2, ' is the longest and valid one')
        else: 
            print(blockchain2, 'is not Valid')
    else:
        print(blockchain2, 'is not Valid')


def loginPriKey(path = 'private.pem'):
    with open(path, 'r') as f:
        private_key = RSA.import_key(f.read())
    return private_key

def loginPubKey(path = 'public.pem'):
    with open(path, 'r') as f:
        public_key = RSA.import_key(f.read())
    return public_key

def get_key(val, my_dict):
#     key_list = list(my_dict.keys())
#     val_list = list(my_dict.values())
 
# # print key with val 100
#     position = val_list.index(val)
#     print(key_list[position])
#     return key_list[position]
    for key, value in dict.items():
         if val == value:
             return key
    return "key doesn't exist"
    
# print (updatehash('yoyo', "ssad"))
# quit()

class Block (object):
    number: int
    previous: Optional['Block']
    data: Optional[dict]
    nonce: int

    def __init__(self, previous=None, data=None, nonce = 0):
        
        self.data = data
        self.previous = previous
        if previous is None:
            self.number = 0
        else:
            self.number = self.get_num()

        self.nonce = nonce

    def __str__(self) -> str:
        return str(
            "\nBlock_Number: %s \nHash: %s \nPrevious_Hash: %s \nData: %s \nNonce: %s" 
            %(self.number, self.hash(), self.get_previous_hash(), self.data, self.nonce)
            )

    def get_previous_hash(self):
        if self.previous is None:
            return genesis_hash
        else:
            return self.previous.hash()
            
    def hash(self):
        return updatehash(
            self.number,
            self.get_previous_hash(), 
            self.data, 
            self.nonce
            ) #pass-in all the infromation to create a unique hash
    
    def get_num(self):
        if self.previous is None:
            return 0 
        return self.previous.get_num() + 1

class Blockchain (object):
    difficulty = 'yO'
    startAmount = 100
    reward = 20

    def __init__(self, chain =[]):
        self.chain = chain
        self.create_genesis()
        self.userDict = {}
        self.moneyDict = {}
        print (type(self.genesis_block))

    def create_genesis(self):
        self.genesis_block = Block(None, "GENESIS")
        self.mine(self.genesis_block)
    
    def addBlock(self, block):
        self.chain.append(block)

    def removeBlock(self, block):
        self.chain.remove(block)

    def mine(self, block, miner = None):
        while block.hash()[:len(self.difficulty)] != self.difficulty:
            block.nonce += 1
        self.addBlock(block)

    def printAll(self):
        for b in self.chain:
            print (b)
        print ('\nThe Block Chain is:\n',self.isValid())
            
    def isValid(self):
        for i in range(1, len(self.chain)):
            if self.chain[i].hash()[:len(self.difficulty)] != self.difficulty:
                return False
        return True

    def saveChain(self, handle = 'yOChain.p'):
            with open(handle, 'wb') as outp:
                pickle.dump(self, outp, pickle.HIGHEST_PROTOCOL)
                print ('Saved As', handle)

    def registerUser(self):

        print ('these will be the only proof of your acoount')
        print ('input your name')
        accountName = str(input())
        key = RSA.generate(2048)

        private_key = key.export_key()
        file_out = open("private.pem", "wb")
        file_out.write(private_key)
        file_out.close()

        public_key = key.publickey().export_key()
        file_out = open("public.pem", "wb")
        file_out.write(public_key)
        file_out.close()

        print(public_key)
        print ("True")
        print ('pem file added to directory')
        self.userDict[accountName] = public_key       #stored as byt type
        self.moneyDict[accountName] = self.startAmount
        print (self.userDict[accountName])
        #self.saveChain()
        print ('chainSaved And User Added')
    
    def transaction(self, sender, amount, reciever, senderpub, senderPriv):                #make a transaction request with signiture
        #message = f'{get_key(sender, self.userDict)}, {amount} ,{get_key(reciever, self.userDict)}'
        self.calcMoney()
        if self.moneyDict[sender] > amount:
            print (f'Sender Have Enough Money For Transition of {amount}\n')
            if self.userDict[sender] == senderpub.export_key():
                message = f'self.moneyDict[\'{sender}\'] -= {amount}\nself.moneyDict[\'{reciever}\'] += {amount}'
                digest = SHA256.new(message.encode('utf-8'))
                privKey = senderPriv
                # print ('please input your private key') 
                # signature = pow(hash, keyPair.d, keyPair.n)
                signature = pkcs1_15.new(privKey).sign(digest)
                transInfo = [senderpub, message, signature]
                return transInfo
            else:
                print('Sender Not Using Sender\'public key')
        else:
            print ('\n!!!not enough in account!!!\n')
            quit()


    def mineTrans(self, translist, miner):                                             #actually mine that transaction
        for info in translist:
            if self.isValid() == True:
                digest = SHA256.new(info[1].encode('utf-8'))
                print ('Transcation On Valid Chain')
                pkcs1_15.new(info[0]).verify(digest, info[2])
                self.mine(Block(self.chain[-1], info[1]+f'\nself.moneyDict[\'{miner}\'] += {self.reward}'))
                print('transaction mined')

    def calcMoney(self):
        for key, val in self.moneyDict.items():
            self.moneyDict[key] = self.startAmount

        for b in self.chain:
            try:
                exec(b.data)
            except: 
                if b.data == 'GENESIS':
                    print ("Start Counting From GENESIS")
                else:
                    print ("Data Error")          
        print (self.moneyDict)

    def transMoney(self):
        pass




if __name__ == '__main__':
        
        # blockchain = Blockchain()
        # database = ['hellowcworld', 'yo','Yoyoy']
        # num = 0

        # for data in database:
        #     blockchain.mine(Block(blockchain.chain[-1], data))

        # blockchain.saveChain()
        
        yc = loadChain()
        #yc = Blockchain()
        #yc.registerUser()
        alicepriv = loginPriKey('aliceprivate.pem')         #stored as RSA object
        alicepub = loginPubKey('alicepublic.pem')
        bobpriv = loginPriKey('bobprivate.pem')
        bobpub = loginPubKey("bobpublic.pem")

        # yc.moneyDict = {}
        # yc.moneyDict['alice'] = 100
        # yc.moneyDict['bob'] = 100
        # yc.saveChain()
        # quit()
        #print(alicepub.export_key())
        transinfo = yc.transaction('alice', 50, 'bob', alicepub, alicepriv)
        transList = []
        transList.append(transinfo)
        yc.mineTrans(transList, 'bob')
        transinfo = yc.transaction('bob', 100, 'alice', bobpub, bobpriv)
        transList = []
        transList.append(transinfo)
        yc.mineTrans(transList, 'bob')
        # transinfo = yc.transaction('bob', 100, 'alice', bobpub, bobpriv)
        # yc.mineTrans([transinfo])
        yc.printAll()

        print ('\nrecounting.....\n')
        yc.calcMoney()


    # blockchain.chain[1].data = "HACKED, I HAVE 1 MILLION DOLLAR"
    # print (blockchain.chain[2])