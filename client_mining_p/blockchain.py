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
        self.new_block(previous_hash=-1, proof=0)

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
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
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
        stringObject = json.dumps(block, sort_keys=True)
        blockString = stringObject.encode()

        rawHash = hashlib.sha256(blockString)
        hexHash = rawHash.hexdigest()
        return hexHash

    @property
    def last_block(self):
        return self.chain[-1]

    # def proof_of_work(self, block):
    #     """
    #     Simple Proof of Work Algorithm
    #     Stringify the block and look for a proof.
    #     Loop through possibilities, checking each one against `valid_proof`
    #     in an effort to find a number that is a valid proof
    #     :return: A valid proof for the provided block
    #     """
    #     blockString = json.dumps(block, sort_keys=True)
    #     proof = 0
    #     while self.valid_proof(blockString, proof) is False:
    #         proof += 1

    #     return proof

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
        guess = f"{block_string}{proof}".encode()
        guessHash = hashlib.sha256(guess).hexdigest()

        return guessHash[:6] == "000000"

    @staticmethod
    def valid_proof_block(block, proof):
        properties = [block.get("index", None), block.get("timestamp", None), block.get("transactions", None), block.get("proof", None), block.get("previous_hash", None)]
        if len([x for x in properties if x is not None]) != 5:
            print("invalid block structure")
            return False
        blockString = json.dumps(block, sort_keys=True)
        return Blockchain.valid_proof(blockString, proof)

# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['POST'])
def mine():
    jsonStr = request.data.decode("utf-8")
    incomingMinedBlock = json.loads(jsonStr)
    newProof = incomingMinedBlock.get("proof", None)
    clientID = incomingMinedBlock.get("id", None)
    if newProof is None or clientID is None:
        return jsonify({"error": "Invalid proof info"}), 400
    newProof = int(newProof)

    if Blockchain.valid_proof_block(blockchain.last_block, newProof):
        # successful = add new block and return message indicating success
        previousHash = blockchain.hash(blockchain.last_block)
        newBlock = blockchain.new_block(newProof, previousHash)
        response = {
            "status": "success",
            "block": newBlock
        }
        return jsonify(response), 200
    else:
        response = {
            "status": "failure",
        }
        return jsonify(response), 401
    


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        # Return the chain and its current length
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


@app.route('/lastblock', methods=['GET'])
def lastBlock():
    return jsonify(blockchain.last_block), 200

# Run the program on port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
