import hashlib
import requests
import sys


# TODO: Implement functionality to search for a proof 
# both functions moved from server code in blockchain.py
def proof_of_work(last_block_string):
    """
    Simple Proof of Work Algorithm
    Find a number p such that hash(last_block_string, p) contains 6 leading
    zeroes

    hash of the string should have 6 leading 0's
    """
    print("Starting work on a new proof....")
    proof = 0
    #for block 1, hash(1, p) = 000000x
    while not valid_proof(last_block_string, proof):
        proof += 1
    print("Attempting to mine...")
    return proof

def valid_proof(last_block_string, proof):
    """
    Validates the Proof:  Does hash(block_string, proof) contain 6
    leading zeroes?
    """
    # TODO
    #generate hash
    guess = f"{last_block_string}{proof}".encode()
    guess_hash = hashlib.sha256(guess).hexdigest()

    #check if 6 leading 0's
    beg = guess_hash[:6]

    if beg == "000000":
        return True
    else:
        return False


if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    coins_mined = 0 #for this client

    # Run forever until interrupted
    while True:
        # TODO: Get the last proof from the server and look for a new one

        r = requests.get(url = node + "/last_block_string")
        data = r.json()
        last_block_string = data["last_block_string"]["previous_hash"]

        new_proof = proof_of_work(last_block_string)

        # TODO: When found, POST it to the server {"proof": new_proof}
        # TODO: We're going to have to research how to do a POST in Python
        # HINT: Research `requests` and remember we're sending our data as JSON
        proof_data = {"proof": new_proof}
        r = requests.post(url = node + "/mine", json = proof_data)
        data = r.json()

        # TODO: If the server responds with 'New Block Forged'
        # add 1 to the number of coins mined and print it.  Otherwise,
        # print the message from the server.
        if data.get("message") == "New Block Forged":
            coins_mined += 1
            print(f"You have: {coins_mined} coins")
        print(data.get("message"))