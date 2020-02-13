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
        self.new_block(previous_hash="-1", proof=0)

        self.difficulty = 5

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
            'previousHash': previous_hash or self.hash(self.chain[-1])
        }

        # Reset the current list of transactions
        self.current_transactions = []
        # Append the block to the chain
        self.chain.append(block)
        # Return the new block
        return block

    def newTransaction(self, sender, recipient, amount):
        """
        : param sender: < str > Address of the Recipient
        : param recipient: < str > Address of the Recipient
        : param amount: < int > Amount
        : return: < int > The index of the `block` that will hold this transaction
        """
        transaction = {
            "sender": sender,
            "recipient": recipient,
            "amount": float(amount),
            "timestamp": time(),
            "id": str(uuid4())
        }

        self.current_transactions.append(transaction)

        return self.last_block['index'] + 1

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

    def balanceForUser(self, user):
        balance = 0
        allXtions = [block["transactions"] for block in self.chain]
        allXtions += self.current_transactions
        for blockTransactions in allXtions:
            for transaction in blockTransactions:
                if transaction["sender"] == user:
                    balance -= transaction["amount"]
                if transaction["recipient"] == user:
                    balance += transaction["amount"]

        return balance

    @property
    def last_block(self):
        return self.chain[-1]

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

        return guessHash[:blockchain.difficulty] == "0" * blockchain.difficulty

    @staticmethod
    def valid_proof_block(block, proof):
        properties = [block.get("index", None), block.get("timestamp", None), block.get(
            "transactions", None), block.get("proof", None), block.get("previousHash", None)]
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

        blockIndex = blockchain.newTransaction("0", clientID, 1)

        newBlock = blockchain.new_block(newProof, previousHash)
        response = {
            "status": "success",
            "block": newBlock,
            "reward": f"reward paid in block {blockIndex}"
        }
        return jsonify(response), 200
    else:
        response = {
            "status": "failure",
        }
        return jsonify(response), 200


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        # Return the chain and its current length
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

@app.route("/transaction/new", methods=['POST'])
def receiveNewTransaction():
    jsonStr = request.data.decode("utf-8")
    data = json.loads(jsonStr)
    # data = request.get_json()

    required = ['sender', 'recipient', 'amount']
    if not all(k in data for k in required):
        return jsonify({"error": "Missing Values"}), 400
    sender = data['sender']
    recipient = data['recipient']
    amount = float(data['amount'])

    if blockchain.balanceForUser(sender) < amount:
        response = {
            "message": f"Insuffienct balance"
        }
        return jsonify(response), 200

    index = blockchain.newTransaction(sender, recipient, amount)
    response = {
        "message": f"Transactions will be included in block {index}"
    }
    return jsonify(response), 200

@app.route('/lastblock', methods=['GET'])
def lastBlock():
    return jsonify(blockchain.last_block), 200


@app.route("/difficulty", methods=["GET"])
def difficulty():
    return jsonify(blockchain.difficulty), 200


# Run the program on port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
