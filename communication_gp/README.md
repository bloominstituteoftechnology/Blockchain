# Communication with other nodes

What about our other nodes?  The underlying principle is that all active nodes should be maintaining the same blockchain.  This means that when when a node adds a block to the chain, it needs to tell the other nodes in the network to do the same.  


# Task List

*Server*
Modify the server we created to:
* Hard code the genesis block so that all servers using this code can share a chain
* When a new block is mined, alert all nodes in its list of registered nodes to add the new block
* Receive a new block from one of the nodes in its list of registered nodes, *validate it*, and add it to the chain, or, if necessary, query for the entire chain
* Validate the new block by checking the index, previous hash, and proof