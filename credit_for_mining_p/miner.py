import hashlib
import requests
import uuid

import sys



def load_id():
    text_file = open('my_id.txt', 'r')
    my_id = text_file.read().split(',')
    text_file.close()
    return my_id


def proof_of_work(last_block_string):
    """
    Simple Proof of Work Algorithm
    Find a number p such that hash(last_block_string, p) contains 6 leading
    zeroes
    """
    proof = 0

    while valid_proof(last_block_string, proof) is False:
        proof += 1
    
    print('Sending to server....')
    return proof

def valid_proof(last_block_string, proof):
    """
    Validates the Proof:  Does hash(block_string, proof) contain 6
    leading zeroes?
    """
    #String to hash
    guess = f'{last_block_string}{proof}'.encode()
    #Hash string
    guess_hash = hashlib.sha256(guess).hexdigest()
    #check for 6 leading 0s
    beg = guess_hash[:6]
    return beg == '000000'




if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    if load_id()[0]:
        userid = load_id()[0]
    else:
        print("Miner ID not found, creating Miner ID ...")
        f = open("my_id.txt", "w")
        userid = str(uuid.uuid1()).replace('-', '')
        print("New Miner ID: " + userid)
        f.write(userid+','+str(0))
        f.close()
        print('Miner ID: ', userid)

    coins_mined = int(load_id()[1])
    # Run forever until interrupted
    while True:
        r = requests.get(url = node +"/last_block_string")
        data = r.json()

        last_block_string = data['last_block_string']['previous_hash']


        new_proof = proof_of_work(last_block_string)

        proof_data = {
            "proof": new_proof,
            "id": userid
        }

        r = requests.post(url=node + "/mine", json=proof_data)
        print(r.json()['message'])

        if r.json()['message'] == 'New Block Forged':
            coins_mined += 1
            print('Coins Mined: ', coins_mined)
            f = open("my_id.txt", "w")
            f.write(userid+','+str(coins_mined))
            f.close()
  
