# Communication with other nodes

What about our other nodes?  The underlying principle is that all active nodes should be maintaining the same blockchain.  This means that when when a node adds a block to the chain, it needs to tell the other nodes in the network to do the same.  


# Task List

Note that our colleagues have added some code for us to use.  They haven't used best practice though, so we'll have to paste our code into theirs, instead of using proper source control.

Be sure to review their code!

*Server*
Modify the server we created to:
**** Hard code the genesis block so that all servers using this code can share a chain
* Add a method to `Blockchain` and use it so that when a new block is mined, the server alerts all nodes in its list of registered nodes to add the new block
* Complete the endpoint to receive a new block from one of the nodes in its list of registered nodes, *validate it*, and add it to the chain
* Validate the new block by checking the index, previous hash, and proof
* Check for consensus if the block is invalid
* To support this add a method to `blockchain` that requests the chain from each peer in the network, and replaces the current chain if one is found that is both valid and longer.  
