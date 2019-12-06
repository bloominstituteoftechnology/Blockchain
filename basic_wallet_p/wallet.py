import requests
from argparse import ArgumentParser

def make_argparser() -> ArgumentParser:
  """
  Parse command line arguments.
  """
  parser = ArgumentParser(description='Find All Blockchain Transactions by ID')
  parser.add_argument('id', type=str, help='Please enter a blockchain ID.')
#   parser.add_argument('node', type=int, help='Please enter node address or press ENTER for default address of localhost:5000.')

  return parser

def search_blockchain(id, chain) -> dict():
    """
    Search the blockchain for an id and return all matching ids
    """
    
    
    key_list = ['sent', 'received', 'all']
    txt = {key : [] for key in key_list}

    for block in chain:
        transactions = block['transactions']

        for trans in transactions:
            
            # print(trans)
            
            flag = False
            
            if trans['sender'] == id:
                txt['sent'].append(trans)
                flag = True    
        
            if trans['recipient'] == id:
                txt['received'].append(trans)
                flag = True
        
            if flag == True:
                txt['all'].append(trans)
            
    
    return txt




host = 'localhost:5000'

if __name__ == "__main__":
    args = make_argparser().parse_args()
  


    node = "http://localhost:5000"

    
    r = requests.get(url=node + "/chain")
    # Handle non-json response
    try:
        data = r.json()
    except ValueError:
        print("Error:  Non-json response")
        print("Response returned:")
        print(r)
    
    blockchain = data['chain']

    txts = search_blockchain(args.id, blockchain)

    sent = txts['sent']
    received = txts['received']
    all_txts = txts['all']

    print(f'''{args.id} has {len(all_txts)} total transactions on the blockchain. 
    {len(sent)} are send transactions and {len(received)} are recieve transactions.''')
    

