# Credit for mining

We've forgotten something important!  Miners want credit for the electricity they spend to mine a new block.  Right now, the server is recording itself as the recipient.  We need to fix this to appropriately give credit where credit is due.


# Task List

*Server*
Modify the server we created to:
- ~~Receive an `id` from a `mine` request.~~
- ~~Record that ID as the `recipient` in the transaction that creates the coin.~~

*Client*
Modify the client we created to:
- Check for a file called `my_id`, open it if found, and load the ID
- Otherwise, create a UUID ID, removing `-`s and save it to a the file
- When a solution is found, send the ID in the POST as `id`
- ~~Note: You will have to research how to create, save, and load files in Python!~~
