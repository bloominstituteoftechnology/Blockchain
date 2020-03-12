import hashlib
import requests
import sys
import json



def proof_of_work(block):
    block_string = json.dumps(block, sort_keys=True)
    proof = 0
    while self.valid_proof(block_string, proof): #until num proof is found
        proof += 1
    return proof


def valid_proof(block_string, proof):
    guess = f'{block_string}{proof}'
    guess_hash = hashlib.sha256(guess).hexdigest()

    return guess_hash[:6] =='000000'


if __name__ == '__main__':
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    # Load ID
    f = open("my_id.txt", "r")
    id = f.read()
    print("ID is", id)
    f.close()

    coins_mined = 0
    print('Starting mining.')

    # Run until interrupted, and handle non-json response:
    while True:
        r = requests.get(url=node + "/last_block")
        try:
            data = r.json()
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(r)
            break

        # Get block from `data` to look for new proof:
        block = data['last_block']
        new_proof = proof_of_work(block)
        print(f'Proof found: {new_proof}')

        # When found, POST to server {"proof": new_proof, "id": id}
        post_data = {"proof": new_proof, "id": id}
        r = requests.post(url=node + "/mine", json=post_data)

        try:
            data = r.json()
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(r)
            break

        print(data['message'])
        # If server responds with 'message': 'New Block Forged', add 1 coins mined and print it. 
        # Else print the message from the server.
        if message == 'New Block Forged':
            coins_mined += 1
            response = {'coins_mined': coins_mined}
            print(response)

        else: 
            return jsonify(message)

