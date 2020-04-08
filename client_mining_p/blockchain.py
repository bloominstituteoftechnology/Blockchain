import hashlib
import json
from time import time
from uuid import uuid4
import random
from flask import Flask, jsonify, request

from math import exp


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.max_award = 1
        self.difficulty = 5

        # Create the genesis block
        self.new_block(proof=100)

    def new_block(self, proof):
        """
        Create a new Block in the Blockchain

        A block should have:
        * Index
        * Timestamp
        * List of current transactions
        * The proof used to mine this block
        * The hash of the previous block

        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous Block
        :return: <dict> New Block
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'prev_hash': block_hash(self.last_block),
            'difficulty': self.difficulty,
        }

        # Reset the current list of transactions
        # Append the chain to the block
        # Return the new block]
        self.current_transactions = []
        self.chain.append(block)
                    
    @property
    def last_block(self):
        if len(self.chain) > 0:
            return self.chain[-1]
        return 1

    @property
    def award(self): 
        return 1 / (1 - abs(self.max_award / (5 - exp(-.05*(self.last_block['index']-0)))))  # 1 - logistic

    def add_transaction(self, transaction):
        self.current_transactions.append(transaction)

    def proof_of_work(self):
        """
        Simple Proof of Work Algorithm
        Stringify the block and look for a proof.
        Loop through possibilities, checking each one against `valid_proof`
        in an effort to find a number that is a valid proof
        :return: A valid proof for the provided block
        """
        
        valid_proof = False
        guess = 0

        while valid_proof == False:
            valid_proof = self.validate_proof(self.last_block, guess, difficulty=self.difficulty)
            guess += 1

        if valid_proof:
            return guess
        else:
            return None

    @staticmethod
    def validate_proof(block, proof, difficulty):
        """
        Validates the Proof:  Does hash(block_string, proof) contain 3
        leading zeroes?  Return true if the proof is valid
        :param block_string: <string> The stringified block to use to
        check in combination with `proof`
        :param proof: <int?> The value that when combined with the
        stringified previous block results in a hash that has the
        correct number of leading zeroes.
        :return: True if the resulting hash is a valid proof, False otherwise
        """
        
        block_string = json.dumps(block, sort_keys=True)

        guess_hash = str(block_hash(
            f'{block_string}{proof}'
        ))
        return '0'*difficulty == guess_hash[0:difficulty]



def block_hash(block: dict):
    """
    Creates a SHA-256 hash of a Block

    :param block": <dict> Block
    "return": <str>
    """

    # Use json.dumps to convert json into a string
    # Use hashlib.sha256 to create a hash
    # It requires a `bytes-like` object, which is what
    # .encode() does.
    # It converts the Python string into a byte string.
    # We must make sure that the Dictionary is Ordered,
    # or we'll have inconsistent hashes

    new_hash = hashlib.sha256(
            json.dumps(block, sort_keys=True).encode()).hexdigest()
    # print(len(new_hash), new_hash)
    return new_hash



# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()



## Routes

@app.route('/', methods=['GET'])
def home():
    response = 'Home Page - Blockchain practice'
    return response


@app.route('/mine', methods=['GET'])
def mine():
    # Run the proof of work algorithm to get the next proof

    print('Begin Mining New Block')
    proof = blockchain.proof_of_work()
    
    blockchain.new_block(
        proof = proof
    )

    response = {
        'message': 'New Block Found',
        'index': blockchain.last_block['index'],
        'transactions': blockchain.last_block['transactions'],
        'proof': blockchain.last_block['proof'],
    }

    return jsonify(response), 200


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'block': blockchain.chain,
        'len': len(blockchain.chain)
    }
    return jsonify(response), 200


@app.route('/last_block', methods=['GET'])
def last_block():
    response = {
        'last_block': blockchain.last_block,
        'difficulty': blockchain.last_block['difficulty'],
    }
    return jsonify(response), 200


@app.route('/verify', methods=['POST'])
def verify():
    miner_id = request.json['miner_id']
    proof = request.json['proof']
    difficulty = blockchain.last_block['difficulty']

    # Check proof
    check = Blockchain.validate_proof(
        block = blockchain.last_block,
        proof = proof,
        difficulty=difficulty,
     )

    # Build transaction if pass
    if check:
        print(f'Valid proof found! Building Transaction for {miner_id}')
        new_transaction = {
            'sender': 0,
            'receiver': miner_id,
            'amount': blockchain.award,
            'message': f"Valid proof <block {blockchain.last_block['index']}><proof {proof}><difficulty {difficulty}>",
        }
        blockchain.add_transaction(new_transaction)
        blockchain.new_block(proof=proof)
    else:
        new_transaction = {'amount': 0}

    response = {
        'miner_id': miner_id,
        'result': check,
        'transaction': new_transaction
    }
    return jsonify(response)



# Run the program on port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
