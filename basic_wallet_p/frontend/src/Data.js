import React, { useEffect, useState } from 'react';
import axios from 'axios';


export default function Data() {
    const [data, setData] = useState([])

    useEffect(() => {
        const getData = () => {
            console.log('just before the axios call')
            axios.get('http://localhost:5000/chain')
                .then(response => {
                    setData(response.data.chain)
                    console.log('in state', response.data.chain)
                })
                .catch(error => {
                    console.log('server error dude!', error);
                });
        }
        getData();
    }, []);


    let theList = []
    const getTransactions = () => {
        //<p>{thedata.transactions.length > 0 ? thedata.transactions.map(trans => <p>transactions: {trans.recipient}, sender: {trans.sender}, amount: {trans.amount}</p>) : ''}</p>
        theList = data.map(thedata => (
            thedata.transactions.length > 0 ? thedata.transactions.map(trans => (
                {
                    'recipient': trans.recipient,
                    'sender': trans.sender,
                    'amount': trans.amount,
                }
            ))
                : []))
        console.log(theList)
        return theList
    }
    getTransactions();
    // this below now makes it so i have access to just a list of all transactions
    theList = getTransactions();
    console.log("after getTransactions fn:", theList)

    //trying to set this up to conditional render if no data stored
    if (!data) {
        return (
            <div>
                <h1> WALLET DATA </h1>

                <h2> SORRY... EITHER THE BLOCKCHAIN IS CURRENTLY DOWN OR BC SERVER ISNT RUNNING</h2>
                <p>AINT NOTHING YET TO SHOW... LOADING...</p>

            </div>
        )
    }

    ///need to map over the list of transactions for each one
    //{thedata.transactions.length ? thedata.transactions[0].recipient : ''}</p>
    // the above states that if the transactions has a length then if true show 
    return (
        <div>
            <h1> All Blocks DATA </h1>
            <p>we are getting data from the server now</p>
            {data.map(thedata => (
                <section>
                    <p>Block: {thedata.index}</p>
                    <p>proof: {thedata.proof}</p>
                    {/* <p>transactions: {thedata.transactions.length ? thedata.transactions[0].recipient : ''}</p> */}
                    {/* can look at one like above or map through like below for each one */}
                    <p>{thedata.transactions.length > 0 ? thedata.transactions.map(trans => <p>transactions: {trans.recipient}, sender: {trans.sender}, amount: {trans.amount}</p>) : ''}</p>
                </section>
            ))}
        </div>
    )
}

