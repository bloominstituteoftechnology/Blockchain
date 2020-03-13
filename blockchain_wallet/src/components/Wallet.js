import React, { useContext, useState, useEffect} from 'react'
import { UserContext } from '../UserContext'

const Wallet = () => {

    const ctx = useContext(UserContext)

    const [ walletTotal, setWalletTotal ] = useState(0)

    const [ loading, setLoading ] = useState(false)

    useEffect(() => {
        
        setLoading(true)

        if (ctx.user){

            let total = 0

            ctx.chain.forEach((block) => {
    
                block.transactions.forEach( transaction => {

                    if(transaction.recipient === ctx.user){
                        total += transaction.amount

                    }else if (transaction.sender ===  ctx.user){
                        total -= transaction.amount

                    }

                })

            }) 
            setWalletTotal(total)
        }

        setLoading(false)

    }, [ctx.chain, ctx.user])

    return (
        <div>
            {!loading && ctx.user && <h3>Balance for {ctx.user}: {String(walletTotal)} coins</h3>}
        </div>
    )
}

export default Wallet