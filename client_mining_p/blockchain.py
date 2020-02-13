import hashlib
import json
from time import time
from uuid import uuid4

from flask import Flask, jsonify, request


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Create the genesis block
        self.new_block(previous_hash="I'm a teapot.", proof=100)

    def new_block(self, proof, previous_hash=None):
      
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        self.current_transactions = []
        self.chain.append(block)
        return block

    def hash(self, block):
    
        string_object = json.dumps(block, sort_keys=True)
        block_string = string_object.encode()

        raw_hash = hashlib.sha256(block_string)
        hex_hash = raw_hash.hexdigest()

        return hex_hash

    @property
    def last_block(self):
        return self.chain[-1]

    # def proof_of_work(self, block):
        
    #     block_string = json.dumps(block, sort_keys=True)
    #     proof = 0
    #     while self.valid_proof(block_string, proof) is False:
    #         proof += 1

    #     return proof

    @staticmethod
    def valid_proof(block_string, proof):

        guess = f'{block_string}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()

        return guess_hash[:3] == "000"


app = Flask(__name__)

node_identifier = str(uuid4()).replace('-', '')

blockchain = Blockchain()
print(blockchain.chain)
print(blockchain.hash(blockchain.last_block))

@app.route('/mine', methods=['POST'])
def mine():

    data = request.get_json()
    
    proof = data['proof']

    last_block = blockchain.last_block

    last_block_string = json.dumps(last_block, sort_keys =True)

    if blockchain.valid_proof(last_block_string, proof):

        previous_hash = blockchain.hash(blockchain.last_block)
        
        new_block = blockchain.new_block(proof, previous_hash)
    
        response = {
            "block": new_block
        }

        return jsonify(response), 200
    else:
        response = {
            "message": "Bad proof"
        }
    return jsonify(response), 200
    
    

   

    


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        # TODO: Return the chain and its current length
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

@app.route('/last_block', methods=['GET'])
def last_block():
    response = {
        'last_block': blockchain.last_block
    }
    return jsonify(response), 200


# Run the program on port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)