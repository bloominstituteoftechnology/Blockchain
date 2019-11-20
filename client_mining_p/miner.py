import hashlib
import requests

import sys
import json
import time

def proof_of_work():
    """
    Simple Proof of Work Algorithm
    Stringify the block and look for a proof.
    Loop through possibilities, checking each one against `valid_proof`
    in an effort to find a number that is a valid proof
    :return: A valid proof for the provided block
    """
    # block_string = json.dumps(block, sort_keys=True)
    last_proof = 28793724
    proof = 28793724
    while valid_proof(last_proof, proof) is False:
        proof += 1
    # guess = f'{block_string}{proof}'.encode()
    # guess_hash = hashlib.sha256(guess).hexdigest()
    # print(guess)
    # print(guess_hash)
    return print(proof)
def valid_proof(last_proof, proof):
    """
    Validates the Proof:  Does hash(block_string, proof) contain 6
    leading zeroes?  Return true if the proof is valid
    :param block_string: <string> The stringified block to use to
    check in combination with `proof`
    :param proof: <int?> The value that when combined with the
    stringified previous block results in a hash that has the
    correct number of leading zeroes.
    :return: True if the resulting hash is a valid proof, False otherwise
    """
    # proof here is like salt, block string is the same salt in this case is changing until we find correct hash
    guess = f'{last_proof}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[:6] == "000000"
while True:
    proof_of_work()



# print(proof_of_work(7590212))


# if __name__ == '__main__':
#     # What is the server address? IE `python3 miner.py https://server.com/api/`
#     if len(sys.argv) > 1:
#         node = sys.argv[1]
#     else:
#         node = "http://localhost:5000"

#     # Load ID
#     f = open("my_id.txt", "r")
#     id = f.read()
#     print("ID is", id)
#     f.close()

#     # Run forever until interrupted
#     coins_mined = 0
#     while True:
#         r = requests.get("https://lambda-treasure-hunt.herokuapp.com/api/bc/last_proof/",
#                          headers={'Authorization': 'Token ef59f33f37d4bf128bd837ff53ea446c66d85281'})
#         # Handle non-json response
#         try:
#             data = r.json()
#             print(data['proof'])
#         except ValueError:
#             print("Error:  Non-json response")
#             print("Response returned:")
#             print(r)
#             break

#         # # TODO: Get the block from `data` and use it to look for a new proof
#         # print('Running proof_of_work')
#         # new_proof = proof_of_work(data['proof'])
        

#         # # When found, POST it to the server {"proof": new_proof, "id": id}
#         # post_data = {'proof': new_proof}

#         # r = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/bc/mine/',  headers={
#         #                   'Authorization': 'Token ef59f33f37d4bf128bd837ff53ea446c66d85281'}, json=post_data)
#         # data = r.json()
#         # print('mine response',data)

#         # if data["message"] == "New Block Forged":
#         #     coins_mined += 1
#         #     print(f"1 coin added, total: {coins_mined}")
#         #     time.sleep(2)
#         #     print('I slept for 2 secs')
            
#         # else:
#         #     print("Error: Nothing added")
#         #     time.sleep(2)
#         #     print('I slept for 2 secs')
            

#         # # TODO: If the server responds with a 'message' 'New Block Forged'
#         # # add 1 to the number of coins mined and print it.  Otherwise,
#         # # print the message from the server.
#         # pass
