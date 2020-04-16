import React, { useEffect, useState } from 'react';
import axios from 'axios';


export default function Data() {
    const [data, setData] = useState([])
    const [transactions, setTransactions] = useState([])

    useEffect(() => {
        const getData = () => {
            console.log('just before the axios call')
            axios.get('http://localhost:5000/chain')
                .then(response => {
                    setData(response.data.chain)
                    console.log('in state', response.data.chain)
                    // setTransactions(response.data.chain.transactions)
                    // console.log('in transactions', response.data.chain.transactions)
                })
                .catch(error => {
                    console.log('server error dude!', error);
                });
        }
        getData();
    }, []);
    const getTransactions = () => {
        tList = []

    }

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
    return (
        <div>
            <h1> WALLET DATA </h1>
            <p>we are getting data from the server now</p>
            {data.map(thedata => (
                <section>
                    <p>Block: {thedata.index}</p>
                    <p>proof: {thedata.proof}</p>
                </section>
            ))}
        </div>
    )
}

