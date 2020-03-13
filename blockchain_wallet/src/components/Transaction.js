import React, { useContext, useState, useEffect } from 'react'
import { UserContext } from '../UserContext'

const Transaction = () => {

    const ctx = useContext(UserContext)
    const [userTransactions, setUserTransactions] = useState(null)


    useEffect(() => {
        
        if (ctx.user){

            let total = []

            ctx.chain.forEach((block) => {
    
                block.transactions.forEach( transaction => {

                    if(transaction.recipient === ctx.user || transaction.sender ===  ctx.user){
                        total.push(transaction)
                    }

                })

            }) 

            setUserTransactions(total)
        }


    }, [ctx.chain, ctx.user])

    return (
        <div>
            <h3>Transactions</h3>
            { userTransactions && 
            userTransactions.map(transaction => {
                return (
                    <div key = {transaction.timestamp}>
                        <p>Transaction Amount: {transaction.amount}</p>
                        <p>Recipient: {transaction.recipient}</p>
                        <p>Sender: {transaction.sender}</p>
                    </div>
                )
            })}
        </div>    
    )
}

export default Transaction