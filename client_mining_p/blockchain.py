import hashlib  #sha-256 for this project
import json  
from time import time
from uuid import uuid4  # for unique user id  -  very difficult to replicate

from flask import Flask, jsonify, request  # gotta learn about flask

LOTSOFZEROS = 6


PURPLE = "\033[95m"
CYAN ="\033[96m"
DARKCYAN = "\033[36m"
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"
END = "\033[0m"


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Create the genesis block
        self.new_block(previous_hash="I'm a teapot.", proof=100)

    def new_block(self, proof, previous_hash=None):
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
        # a dictionary
        block = {
            # TODO
            'index': len(self.chain) + 1, # index of the first block is 1
            # for index here in a block, we get to count normally
            'time_stamp':time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash # or self.hash(self.chain[-1]) hashing the last block
        }

        # Reset the current list of transactions
        self.current_transactions = []
        # Append the block to the chain
        self.chain.append(block)
        # Return the new block
        return block

    def hash(self, block):
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

        # TODO: Create the block_string
        string_object = json.dumps(block, sort_keys=True)
        block_string = string_object.encode()

        '''
        # json.dumps ( stringifys json ) 
        # turn block into a string
        #sort_key = True = makes sure keys are done in the same order
            # otherwise they will all be different

        problem with python string = they are actually objects so have to encode

        .encode()
        a string in python is an object with meta data and functions 
        cannot be encoded into an sha-256
        .encode() turns into bit string

        has same effect b " " will have
        gives us a RAW string

        '''
        # TODO: Hash this string using sha256
        raw_hash = hashlib.sha256(block_string)
        hex_hash = raw_hash.hexdigest()

        '''

        look up hexdigest()

        '''

        # By itself, the sha256 function returns the hash in a raw string
        # that will likely include escaped characters.
        # This can be hard to read, but .hexdigest() converts the
        # hash to a string of hexadecimal characters, which is
        # easier to work with and understand

        # TODO: Return the hashed block string in hexadecimal format
        return hex_hash

    @property # decorator~ the preamble for a function
    # makes the return from the function a property of the chain
    def last_block(self):
        return self.chain[-1]

    @staticmethod # decorator
    # can run it without an instance
    def valid_proof(block_string, proof):
        #  hash(block_string, proof) = proof of work
        """
        Validates the Proof:  Does self.hash(block_string, proof) contain 3
        leading zeroes?  Return true if the proof is valid
        :param block_string: <string> The stringified block to use to
        check in combination with `proof`
        :param proof: <int?> The value that when combined with the
        stringified previous block results in a hash that has the
        correct number of leading zeroes.
        :return: True if the resulting hash is a valid proof, False otherwise
        """

        '''
        hash() only takes one param while our self.hash() takes two

        using sha-256 hash to:
            1) validating the chain
            2) proof of work
        '''
        # TODO
        guess = f"{block_string}{proof}".encode()
        '''
        becomes bit string so we can hash it
        '''

        guess_hash = hashlib.sha256(guess).hexdigest()
        '''
        hexdigest converts into a readable format so we can compare
        '''

        return guess_hash[:LOTSOFZEROS] == '0' * LOTSOFZEROS
        '''
        return if guess_hash  first 3 characters == '000'
        '''
        # return True or False


# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()

@app.route('/mine', methods=['POST']) # It should accept a POST

def mine():
    #instead receive and validate or reject a new proof sent by a client

    '''
    * Note that `request` and `requests` both exist in this project
      Remember, a valid proof should fail for all senders except the first.
    '''
    # Use `data = request.get_json()` to pull the data out of the POST
    try:
        data = request.get_json()
    # non json response
    except ValueError:
        print('Error: non json response')
        print(request)
        return

    # Check that 'proof', and 'id' are present
    required_keys = ['proof', 'id']

    #loop through req_keys
    for key in required_keys:

        # if proof and id not in the data received
        if key not in data:

            #return a 400 error using `jsonify(response)` with a 'message'
            response = {
                'error': 'Invalid proof format'
            }
            code = 400
        else:

            # performing what was proof part of proof_of_work on the post request
            block_string = json.dumps(blockchain.last_block, sort_keys=True)
            miner_proof = data['proof']
            print(CYAN + f"{miner_proof}, miner proof is this")
            #minor proof is the  like striking gold but a proof
            # will reflect in a print() i have set up on miner.py

            # as long as the proof checks out and has the 6 preceeding 0s
            if blockchain.valid_proof(block_string, miner_proof):
                previous_hash = blockchain.hash(blockchain.last_block)

                # a new_block will be created that will hold on to the prev hash of the block before it.
                new_block = blockchain.new_block(miner_proof, previous_hash)
                
                # success
                response = {
                    'message': 'New Block Forged',
                    'block': new_block
                }
                code = 200
            else:

                # failure
                response = {
                    'message': 'Proof is not valid or already submitted'
                }
                code = 400
        # Return a message indicating success or failure.
        return jsonify(response), code


@app.route('/chain', methods=['GET']) # get request
def full_chain():
    response = {
        # TODO: Return the chain and its current length
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200

@app.route('/last_block', methods=['GET']) # get request
def last_block():
   
    # returns the last block in the chain
    last_block_in_chain = blockchain.last_block
    
    response = {
        # TODO: Send a JSON response with the last block
        'last_block': last_block_in_chain
    }

    return jsonify(response), 200


# Run the program on port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
