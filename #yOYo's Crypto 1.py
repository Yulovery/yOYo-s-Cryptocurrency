#yOYo's Crypto 1
#Dec 14 2pm - 3pm

from hashlib import sha256
import base64

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
    
# print (updatehash('yoyo', "ssad"))
# quit()

class Block (object):
    data=None 
    hash = None
    nonce = 0
    prev_hash = 'yoyo' + "0" * 42

    def __init__(self, data, number = 0):
        self.data = data
        self.number = number

    def __str__(self) -> str:
        return str(
            "\nBlock_Number: %s \nHash: %s \nPrevious_Hash: %s \nData: %s \nNonce: %s" 
            %(self.number, self.hash(), self.prev_hash, self.data, self.nonce)
            )

    def hash(self):
        return updatehash(
            self.prev_hash, 
            self.number, 
            self.data, 
            self.nonce
            ) #pass-in all the infromation to create a unique hash


class Blockchain (object):
    difficulty = 'yO'

    def __init__(self, chain =[]):
        self.chain = chain
    
    def addBlock(self, block):
        self.chain.append(block)

    def removeBlock(self, block):
        self.chain.remove(block)

    def mine(self, block):
        try:                            #try/except runs faster than if
            block.prev_hash = self.chain[-1].hash()
        except IndexError:
            pass

        while True:
             #the hash's first four letter need to be yOYo
            if block.hash()[:len(self.difficulty)] == self.difficulty:
                self.addBlock(block); break
            else:
                block.nonce += 1

    def isValid(self):
        for i in range(1, len(self.chain)):
            stored_previous = self.chain[i].prev_hash
            previous = self.chain[i-1].hash()
            if stored_previous != previous or previous[:len(self.difficulty)] != self.difficulty:
                return False
        return True
            




if __name__ == '__main__':
    blockchain = Blockchain()
    database = ['hellowcworld', 'hi', 'fghj']
    num = 0

    for data in database:
        num += 1
        blockchain.mine(Block(data, num))

    for b in blockchain.chain:
        print (b)

    print ('\nThe Block Chain is Valid:\n',blockchain.isValid())


