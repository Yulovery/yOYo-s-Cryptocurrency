#yOYo's Crypto 1
#Dec 13 9pm - 11:10pm


from hashlib import sha256
import base64

def updatehash(*args):                  #create and return a ahsh based on the information given
    hashing_text = ""   #instance of the imported hash "class"
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
            "Block_Number: %s \nHash: %s \nPrevious_Hash: %s \nData: %s \nNonce: %s" 
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
    difficulty = 'yOYo'

    def __init__(self, chain =[]):
        self.chain = chain
    
    def addBlock(self, block):
        self.chain.append({
            'hash': block.hash(), 
            "previous": block.prev_hash, 
            'number': block.number, 
            'data': block.data, 
            'nonce': block.nonce
            })

    def mine(self, block):
        try:                            #try/except runs faster than if
            block.prev_hash = self.chain[-1].get('hash')
        except IndexError:
            pass

        while True:
             #the hash's first four letter need to be yOYo
            if block.hash()[:len(self.difficulty)] == self.difficulty:
                self.addBlock(block); break
            else:
                block.nonce += 1


if __name__ == '__main__':
    blockchain = Blockchain()
    database = ['hellowcworld', 'hi']
    num = 0

    for data in database:
        num += 1
        blockchain.mine(Block(data, num))

    for b in blockchain.chain:
        print (b)


