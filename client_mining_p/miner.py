import hashlib
import requests

import sys
import json

from multiprocessing import Process, Queue, Event


### Threading Setup ###
q = Queue()
processes = []
num_workers = 8


### Local Results Store ###
class NodeInfo():
    def __init__(self, miner_id=None, server_url=None):
        self.miner_id = miner_id
        self.server_url = server_url

    @property
    def verification_url(self):
        if self.server_url is not None:
            return self.server_url + '/verify'    

class Results():
    def __init__(self, results=[]):
        self.proof = Queue()

    def add_result(self, result):
        if result:
            self.proof.put(result)

    @property
    def success(self):
        return not self.proof.empty()
        
node_info = NodeInfo()
results = Results()


def block_hash(block: dict):
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

    new_hash = hashlib.sha256(
            json.dumps(block, sort_keys=True).encode()).hexdigest()
    # print(len(new_hash), new_hash)
    return new_hash


def validate_proof(block, proof, difficulty):
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
    
    block_string = json.dumps(block, sort_keys=True)

    guess_hash = str(block_hash(
        f'{block_string}{proof}'
    ))
    return '0'*difficulty == guess_hash[0:difficulty]



def proof_of_work(block, search_space:list, difficulty: int):
    """
    Modified Proof of Work Algorithm
    Stringify the block and look for a proof.
    Loop through defined search_space of possibilities, checking each one against `valid_proof`
    in an effort to find a number that is a valid proof
    :return: A valid proof for the provided block
    """
    
    # Validate search_space
    assert len(search_space) == 2, 'Search space only accepts [start_int, end_int]'
    assert type(search_space[0]) == int, 'Must provide integer start' 
    assert type(search_space[1]) == int, 'Must provide integer end'

    valid_proof = False
    guess = search_space[0]

    while guess < search_space[1]:
        valid_proof = validate_proof(
            block=block, 
            proof=guess, 
            difficulty=difficulty
            )
        if valid_proof:
            return guess
        guess += 1

    return None


def request_block(url):
    """ Request last block from server with given URL """
    r = requests.get(url = url)
    try:
        data = r.json()
    except:
        raise

    return(data)


def check_proof():
    if results.success:
        print('Validating \n')
        check = requests.post(url=node_info.verification_url, json = {
            'miner_id': node_info.miner_id,
            'proof': results.proof.get(),
        })
        return check


def mine(job):
    print(f"Starting to mine{job['search_space']}")
    proof = proof_of_work(
        block=job['block'],
        search_space=job['search_space'],
        difficulty=job['difficulty']
    )
    if proof is not None:
        results.add_result(proof)
        return True
    return False


def miner(pquit, foundit):
    while not pquit.is_set():
        if q.empty():
            break
        job = q.get()
        if job is None:
            break
        if mine(job):
            print('Found proof!')
            check = check_proof()
            print(check.json())
            foundit.set()
            break
        

def create_jobs(block_info, max_search = 2**24, num_jobs=0):
    segment = max_search/num_workers
    jobs = []

    # Dynamically size number of jobs based on max_search
    if num_jobs == 0:
        num_jobs = int(max_search/10000)

    for i in range(num_jobs):
        search_space = [
            int(i*segment), int((i+1)*segment)
        ]
        job = {
            'block': block_info['last_block'],
            'search_space': search_space,
            'difficulty': block_info['difficulty'],
        }
        jobs.append(job)

    return jobs



if __name__ == '__main__':
    # What is the server address? IE `python3 miner.py https://server.com/api/`
    if len(sys.argv) > 1:
        node_info.server_url = sys.argv[1]
    else:
        node_info.server_url = "http://localhost:5000"

    # Load ID
    f = open("my_id.txt", "r")
    node_info.miner_id = f.read()
    print("ID is", node_info.miner_id)
    f.close()

    # Get last block
    block_info = request_block(url=node_info.server_url + '/last_block')

    # # Search for proof (single-threaded)
    # proof = proof_of_work(block=block_info['last_block'], search_space=[0, 2**256], difficulty=block_info['difficulty'])
    # print('Proof:', proof)

    # Search for proof (multi-threaded)
    jobs = create_jobs(block_info=block_info)
    print(jobs[0], jobs[-1])

    # Load queue
    for job in jobs:
        q.put(job)

    # Start multiple processes
    pquit = Event()
    foundit = Event()
    for i in range(num_workers):
        p = Process(target=miner, args=(pquit, foundit))
        p.start()
        processes.append(p)

    foundit.wait()
    pquit.set()

    for p in processes:
        p.terminate()
        p.join()
    print('All Done')

