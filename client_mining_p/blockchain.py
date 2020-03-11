import hashlib
import json
from time import time
from uuid import uuid4 #universally unique identifier

from flask import Flask, jsonify, request

"""
The blockchain is a new way of storing and moving data securely. The data mostly consists of transactions 
or blocks which include messages exchanged between two parties. 
"""
class Blockchain(object):
    def __init__(self):
        self.chain = [] #list that holds all the blocks inside the chain
        self.current_transactions = [] #list of current transactions in each block

        # Create the genesis block - block automatically generated when the blockchain is initialized
        # initialize the previous_hash for the genesis block to an invalid hash to indicate that it doesn't 
        # have a previous block (I'm a teapot is not valid)
        self.new_block(previous_hash = "I'm a teapot.", proof = 100)

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

        #blockchains are made up of blocks
        #each block is best represented in the form of a Python dictionary, with keys for the required 
        #fields and values specific to the transaction.
        block = {
            # TODO
            #index starts at 1 and not 0 - length will start out at 0 and then we add 1 to it
            'index': len(self.chain) + 1, 
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            #generate a previous hash if we did not provide a hash like we did for the genesis hash
            'previous_hash': previous_hash or self.hash(self.chain[-1]),#previous block's hash
        }

        # Reset the current list of transactions        
        self.current_transactions = []

        # Append the block to the chain
        self.chain.append(block)

        # Return the new block
        return block

    #hash the previous block
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

        # The SHA-256 algorithm is used to generate the hash of the block using all the information in the block
        # The block is passed to json.dumps to be converted into a string before being encoded and
        # passed to hashlib.sha256
        # sort_keys = True => We must make sure that the Dictionary is ordered or the hash will all be different
        # if the keys are not in the same order
        string_object = json.dumps(block, sort_keys = True)

        #To properly use this function in Python 3, our string must be encoded before being passed as 
        # an argument. To encode the string, we use the .encode() method.
        #python strings are not really strings they are metadata so we need to encode it
        block_string = string_object.encode()

        # Use hashlib.sha256 to create a hash
        raw_hash = hashlib.sha256(block_string)

        #hexdigest returns the hashed block string in hexadecimal format
        hex_hash = raw_hash.hexdigest()

        # By itself, the sha256 function returns the hash in a raw string
        # that will likely include escaped characters.
        # This can be hard to read, but .hexdigest() converts the
        # hash to a string of hexadecimal characters, which is
        # easier to work with and understand

        # TODO: Return the hashed block string in hexadecimal format
        return hex_hash

    @property
    def last_block(self):
        #returns the last block in the chain list
        #self.chain is the list that holds all the blocks inside the chain
        return self.chain[-1]

    """
    proof_of_work method is called from the mine() endpoint  ~ line 191. block is passed to json.dumps to be 
    converted into a string before being passed to the valid_proof method where the SHA-256 algorithm is used to 
    generate or guess the hash with a specific amount of leading zeros. 
    """

    """
    The hash function that’s most commonly used to create the hash for the block is the SHA-256. 
    Miners first guess a nonce value, which is then combined with the contents of the block 
    (i.e transactions, timestamp, hash, and previous hash). They repeat this process until the 
    desired hash is generated.
    """
    #remove proof of work function from the server
    #this is now in the miner.py file
    """
    def proof_of_work(self, block):
        
        Simple Proof of Work Algorithm
        Stringify the block and look for a proof.
        Loop through possibilities, checking each one against `valid_proof`
        in an effort to find a number that is a valid proof
        :return: A valid proof for the provided block
        
        #block is passed to json.dumps to be converted into a string before being encoded and
        #passed to hashlib.sha256
        block_string = json.dumps(block, sort_keys=True)
        #nonce value combined with the contents of the block in valid_proof to generate the guess hash
        #we don't have to encode the proof since we are combining it with another string
        #a way to do this is to guess, start at 0 and start guessing numbers
        proof = 0
        #this will run until it finds one that works
        while self.valid_proof(block_string, proof) is False:
            #increments the proof value until the hash with the required difficulty has been generated.
            proof += 1
        #after we find one that works, we return proof
        return proof
    """


    @staticmethod #static methods can be run without an instance of the class
    #helps protect the blockchain from potential attackers.
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
        #encode the block_string and proof (nonce value) passed in from proof_of_work
        guess = f'{block_string}{proof}'.encode()

        #hashes and converts guess to hexadecimal format (readable format that we can compare)
        guess_hash = hashlib.sha256(guess).hexdigest()

        #return guess_hash if it contains 6 leading zeros
        return guess_hash[:6] == "000000"


# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()
print(blockchain.chain)
print(blockchain.hash(blockchain.last_block))

#Modify the `mine` endpoint to instead receive and validate or reject a new proof sent by a client.
# It should accept a POST
@app.route('/mine', methods=['POST'])
def mine():

    #Use `data = request.get_json()` to pull the data out of the POST
    data = request.get_json()

    if 'proof' not in data or 'id' not in data: 
        response = {"message": "proof and/or id are not present"}
        return jsonify(response), 400

    #if proof and id exists, store them in proof and minder_id
    proof = data['proof']
    miner_id = data['id']    

    #convert last_block to a string
    last_block = blockchain.last_block
    last_block_string = json.dumps(blockchain.last_block, sort_keys=True)

    #and check if the last_block and the proof recieved in the POST was valid
    if blockchain.valid_proof(last_block_string, proof):

        #hash the last_block to get the previous hash
        #then forge the new block by passing the proof and the previous_hash to new_block
        previous_hash = blockchain.hash(blockchain.last_block)
        new_block = blockchain.new_block(proof, previous_hash)    

        #send a JSON response with the new_block and a success message
        response = {
            # TODO: Send a JSON response with the new_block
            "block": new_block,
            "message": "New Block Forged"
        }

        return jsonify(response), 200
    else:
        #if the last_block and the proof recieved in the POST was not valid
        #send an error message
        response = {"message": "Invalid or already submitted proof"}
        return jsonify(response), 200


#endpoint that returns the chain and it's current length
@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        # TODO: Return the chain and its current length
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200

#endpoint that returns the last_block in the chain
@app.route('/last_block', methods=['GET'])
def last_block():       

    response = {
        # TODO: Send a JSON response with the new block
       "last_block": blockchain.last_block
    }

    return jsonify(response), 200


# Run the program on port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)