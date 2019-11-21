# Blockchain FAQ
## Contents
### General

#### Help!  I'm on Windows and pipenv doesn't work!
If you've already done the setup for BW1, you should be set.  Don't forget that you need to change the `pipfile` to use Python version "3" and create your virtual environment with _pipenv --three --python=\`which python3\`_  *NOTE* that there are backticks (\`) around *which python3*

If not, follow [these steps](https://github.com/LambdaSchool/CS-Build-Week-1/blob/master/WindowsSetup.md) up to and including number 7

#### Help!  I'm on Windows, I've done the above, and the console says the server is running on http://0.0.0.0:5000, but when I try to load that I get an error that the site cannot be reached.

This is a great learning example of why you should _never_ hardcode values.  On a Mac, this will work.  On Windows, the server can be found on http://localhost:5000 or http://127.0.0.1:5000.

#### What's the difference between block chain and crypto currency?
A block chain is a ledger that securely records transactions or other data with a timestamp in a public form that cannot be altered or manipulated after it is recorded.  Crypto currency is made up currency with transactions that are recorded within the block chain.  Most systems introduce money into the system by paying it as a set reward for mining a block.

#### What is mining?
Mining is the act of adding a block to a blockchain.  This is done by solving or winning consensus system, usually Proof of Work or Proof of Stake.  

#### What is Proof of Work?
Proof of work is an arbitrarily difficult computing problem.  Each problem is directly related to the current block, so it is not possible to re-use or pre-calculate work.

#### What is proof of Stake?
Proof of Stake is a system that rewards coins semi-randomly, with better chances for winning based on either the amount or age of coins someone holds.  The advantage is that it doesn't consume electricity to mine, however it creates an incentive to _not_ spend currency.

#### What is Bitcoin?
[Bitcoin](https://en.wikipedia.org/wiki/Bitcoin) is the first major cryptocurrency, although it is not the first attempt to create an e-currency.  It uses proof of work for consensus.

#### What is Ethereum?
[Ethereum](https://en.wikipedia.org/wiki/Ethereum) is another popular cryptocurrency.  It uses Proof of Work for consensus but is in the process of switching to Proof of Stake.

#### What are some factors that might prevent Bitcoin from becoming a mainstream currency in the future?

#### What are the environmental and energy implications if BitCoin becomes a mainstream currency in the future?
Bitcoin/crypto mining currently consumes enough energy to power a small country.  This is likely to grow if they become mainstream.  However, engineers hate waste.  Two possibilities for mitigation are the use of the heat from mining to recover some lost energy, and the switch to less energy consuming methods of consensus.

#### What about quantum computing? Will that make it exponentially easier to mine coins? Or inject invalid blocks into the chain?
Quantum computing will be an epochal change that alters the fundamental landscape of how computing works.   The risk is that it could break the system because it could calculate hashes so quickly that a single quantum computer could mine faster than all regular computers.  However, when they become availible, many people are likely to have them, so I think it will balance out.

The other risk, however, is that it will break the current system of encryption of transactions.  Luckily, it's likely that there will be plenty of warning for this shift, and new systems of cryptography can be devised.

#### What is `hashlib`?
`Hashlib` is a Python library that can produce a number of hashing algorithms.  We use it for the `SHA-256` hash function.

#### What exactly are we using the hash function to do?
We're using the hash function to standardize a set of data for comparison in a way that is unpredictable and can't be gamed or pre-calculated.

#### What is the `uuid`?
UUID stand for `Universally Unique Identifier`.  It's a string of random characters with enough entropy (possibilities) that it is very unlikely that the same sequence will come up twice.

#### What is Flask & how does it work?
Flask is a lightweight package that lets you create servers and endpoints in Python.  Each endpoint calls exactly one function one time when accessed.

#### I suddenly started getting a bunch of crazy errors, no module named 'request', etc. what's happening?
Did you use `pipenv install` and `pipenv shell`?  Make sure you are still in your shell.  It can close sometimes without you realizing it.

#### How long should it take to mine a coin and/or why isn't my miner getting me a coin?
With most of the example `Proof of Work` algorithms, it should take a simple miner 1 to 3 minutes to find a solution.  The age of the computer shouldn't matter very much.

Remember that it is a competition.  At best, you will usually lose against the 30 to 60 other students who are competing for the same coin.  At worse, think about what happens if you and another student are both using the exact same mining algorithm, but they started first.  What will happen?  What can you do to mitigate this problem?

#### What is the rule of the longest chain?
The longest chain states that the valid chain with the most blocks has the most work in it, and is therefore the valid chain.  All other branches are discarded and a complicated process involving the mempool (in Bitcoin) recovers lost transactions.



