# Credit for mining

We've forgotten something important!  Miners want credit for the electricity they spend to mine a new block.  Right now, the server is simply recording a `0` as the sender.  We need to fix this to appropriately give credit where credit is due. 


# Task List

*Server*
Modify the server we created to:
X Receive an `id` from a `mine` request.
X Record that ID as the `sender` in the transaction that creates the coin.

*Client*
Modify the client we created to:
X Check for a file called `my_id`, open it if found, and load the ID
X Otherwise, create a UUID ID, removing `-`s and save it to a the file
X When a solution is found, send the ID in the POST as `id`