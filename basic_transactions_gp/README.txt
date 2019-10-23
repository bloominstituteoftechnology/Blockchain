Create a method in the `Blockchain` class called `new_transaction` 
that adds a new transaction to the list of transactions:

    :param sender: <str> Address of the Recipient
    :param recipient: <str> Address of the Recipient
    :param amount: <int> Amount
    :return: <int> The index of the `block` that will hold this transaction

Modify the `mine` endpoint to create a reward via a `new_transaction`
for mining a block:

    * The sender is "0" to signify that this node created a new coin
    * The recipient is the id of the miner
    * The amount is 1 coin as a reward for mining the next block

Create an endpoint at `/transactions/new` that accepts a json `POST`:

    * use `request.get_json()` to pull the data out of the POST
    * check that 'sender', 'recipient', and 'amount' are present
        * return a 400 error using `jsonify(response)` with a 'message'
    * upon success, return a 'message' indicating index of the block
      containing the transaction

