import hashlib
import json
import string
from time import time
import __future__

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.nodes = set()
        self.new_block(previous_hash=1, proof=100)
            
    def new_block(self, proof, previous_hash=None):
        """
        Create a new Block in the Blockchain
        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous Block
        :return: <dict> New Block
        """
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.pending_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        self.pending_transactions = []
        self.chain.append(block)
        
        return 
    
    def last_block(self):
        return self.chain[-1]
    
    def new_transaction(self, sender, receiver, amount):
        transaction = {
            'snd': sender,
            'rec': receiver,
            'amt': amount
        }
        self.pending_transactions.append(transaction)
        return self.last_block()['index'] + 1
    
    def hash(self, block):
        # Generate an immutable hashed block
        
        string_object = json.dumps(block, sort_keys=True)
        block_str = string_object.encode()
        raw_hash = hashlib.sha256(block_str)
        hex_hash = raw_hash.hexdigest()
        
        return hex_hash
    
    def display_chain(self):
        for i in range(len(self.chain)):
            print(i + ": " + str(self.chain[i]))

class Proof_of_Work(object):
    def __init__(self, blockchain: Blockchain):
        self.blockchain = blockchain
    
    def run(self):
        last_block = self.blockchain.last_block()
        last_proof = last_block['proof']
        proof = proof_of_work(self.blockchain, last_proof)
        
        return proof
    
    def valid_proof(self, last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

def proof_of_work(blockchain: Blockchain, last_proof: Proof_of_Work):
    """
    Simple Proof of Work Algorithm:
    - Find a number p' such that hash(pp') contains leading 4 zeroes, where p is the previous p'
    - p is the previous proof, and p' is the new proof
    :param last_proof: <int>
    :return: <int>
    """
    proof = 0
    while not last_proof.valid_proof(last_proof, proof):
        proof += 1
    
    return proof

def test_blockchain():
    blockchain = Blockchain()
    t1 = blockchain.new_transaction('sender1', 'receiver1', 100)
    t2 = blockchain.new_transaction('sender2', 'receiver2', 200)
    t3 = blockchain.new_transaction('sender2', 'receiver1', 50)
    
    blockchain.new_block(12345)
    
    t4 = blockchain.new_transaction('sender3', 'receiver3', 300)
    t5 = blockchain.new_transaction('sender4', 'receiver3', 1400)
    t6 = blockchain.new_transaction('sender4', 'receiver4', 500)
    
    blockchain.new_block(54321)
    
    print(blockchain.chain)