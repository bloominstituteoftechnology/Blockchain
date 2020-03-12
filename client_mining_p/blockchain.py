import hashlib
import json
from time import time
from uuid import uuid4
from flask import Flask, jsonify, request

import random
import string


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Create the genesis block
        self.new_block(previous_hash=1, proof=100)

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

        block = {
            "index": len(self.chain) + 1,
            "timestamp":time(),
            "transactions":self.current_transactions,
            "proof":proof,
            "previous_hash": previous_hash or self.hash(self.chain[-1]) #or self.lastblock
        }

        # Reset the current list of transactions
        current_transactions = []
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
        string_block = json.dumps(block, sort_keys=True)#if orders change, the hash would be different
        # Use hashlib.sha256 to create a hash
        # It requires a `bytes-like` object, which is what
        # .encode() does.
        raw_hash = hashlib.sha256(string_block.encode())
        # It converts the Python string into a byte string.
        # We must make sure that the Dictionary is Ordered,
        # or we'll have inconsistent hashes
        hex_hash = raw_hash.hexdigest()

        # TODO: Create the block_string
        return hex_hash

        # TODO: Hash this string using sha256

        # By itself, the sha256 function returns the hash in a raw string
        # that will likely include escaped characters.
        # This can be hard to read, but .hexdigest() converts the
        # hash to a string of hexadecimal characters, which is
        # easier to work with and understand

        # TODO: Return the hashed block string in hexadecimal format
        pass

    @property #property decorator, don't need to use 
    #parenthesis when you use this, acts like a property not a method, 
    # gives you the last block
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, block):
        """
        Simple Proof of Work Algorithm
        Stringify the block and look for a proof.
        Loop through possibilities, checking each one against `valid_proof`
        in an effort to find a number that is a valid proof
        :return: A valid proof for the provided block
        """
        # TODO
        block_string = json.dumps(block, sort_keys=True)
        proof = 0
        while self.valid_proof(block_string, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(block_string, proof):
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
        # TODO

        guess = f'{block_string}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest() # turn into a hexadecimal string

        return guess_hash[:3] == '000'#slice off last 6, see if it equals all zeros
        # we compare hexidecimal strings


# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    # Run the proof of work algorithm to get the next proof
    proof = blockchain.proof_of_work(blockchain.last_block)
    # Forge the new Block by adding it to the chain with the proof
    previous_hash = blockchain.hash(blockchain.last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'new_block': block
    }
    return jsonify(response), 200

@app.route('/check', methods=['POST'])
 # if the incoming proof sent by the client is valid, and if so add the block
def check():
# Modify the mine endpoint to instead receive and validate or reject a new proof sent by a client.

# Use data = request.get_json() to pull the data out of the POST
    data = request.get_json()
# Note that request and requests both exist in this project
# Check that 'proof', and 'id' are present
    if data and ("proof" in data) and ("id" in data):
        id = data["id"]    
        proof = data["proof"]

        # get back in json the last block in the last_block route
        # convert to string
        # tack on extra info 
        # hash 
        # check if the hash has "000000" at the start, and then send proof (the thing you added to string before hashing) to /mine
        # if it matches proof
        # print something

        response = {
        # return a 400 error using jsonify(response) with a 'message'
        'match': 'It is a match',
    }
        return jsonify(response)
    else: 
        response = {
        # return a 400 error using jsonify(response) with a 'message'
        'ERROR 400': '400 Error, proof and id are not present',
    }
        return jsonify(response)
# Return a message indicating success or failure. Remember, a valid proof should fail for all senders except the first.




# # Get the last block from the server
# # Run the proof_of_work function until a valid proof is found, validating or rejecting each attempt. Use a copy of valid_proof to assist.
#     proof = blockchain.proof_of_work(blockchain.last_block)
# # Print messages indicating that this has started and finished.
# # Modify it to generate proofs with 6 leading zeroes.
# # Print a message indicating the success or failure response from the server
# # Add any coins granted to a simple integer total, and print the amount of coins the client has earned
# # Continue mining until the app is interrupted.



#     # Run the proof of work algorithm to get the next proof
#     proof = blockchain.proof_of_work(blockchain.last_block)
#     # Forge the new Block by adding it to the chain with the proof
#     previous_hash = blockchain.hash(blockchain.last_block)
#     block = blockchain.new_block(proof, previous_hash)

#     response = {
#         'new_block': block
#     }
#     # return a 400 error using jsonify(response) with a 'message'
#     data = request.get_json()

#     return jsonify(response), 200


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        # TODO: Send a JSON response with the new block
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }

    return jsonify(response), 200


@app.route('/last_block', methods=['GET'])
def get_last_block():
        # get back in json the last block in the last_block route
        # convert to string
        # tack on extra info 
        # hash 
        # check if the hash has "000000" at the start, and then send proof (the thing you added to string before hashing) to /mine
    # get back in json the last block in the last_block route
    last_block = blockchain.last_block
    if last_block and ("previous_hash" in last_block):
        last_block = last_block["previous_hash"] 
        # convert to string
        convert_to_string = json.dumps(last_block) #str() worked before
        string.ascii_letters
        # tack on extra info
        newly_generated_alphanumeric_char = random.choice(string.ascii_letters)
        newly_generated_alphanumeric_char = newly_generated_alphanumeric_char.lower()
        hash_with_added_str = convert_to_string + newly_generated_alphanumeric_char + newly_generated_alphanumeric_char

        hashed_last_block = blockchain.hash(hash_with_added_str)

        response = {
            "last_block":hashed_last_block
        }

        return jsonify(response), 200


# Run the program on port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


#take hash function, take the item at the end of it 

#take information in latest block
# take from last block
#run through hash function, see if it checks out
#see if you hav eenough leading zeros to match

#a hash of the previous block for guesses


#condition to make new block
#someone makes a proof that works

#take hash of previous block tack characters to end
#find hash to get condition = 3 zeros in front
#if you find, submit the proof
#server check it, yes it is true when i hash with this block, this is what satisfies requirements
#if block gets added you get a lambda coin


#check if proof and id are present, use jsonfiy response if not 400
#id is when you get paid