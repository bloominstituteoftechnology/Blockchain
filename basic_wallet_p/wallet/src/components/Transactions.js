import React, {useState, useEffect, useContext} from "react";
import WalletContext from "../contexts/WalletContext"

export default function Transactions () {
    const { txns, balance } = useContext(WalletContext)
    
    return(
        <div className="txn-list">
            {txns.map(item => 
                item.length > 0 
                    ?
                    <>
                    {item.map(txn =>
                        <div className={txn.pending ? "txn-log pending" : "txn-log"}>
                            <span>Sender: {txn.sender}</span>
                            <span>Receiver: {txn.recipient}</span>
                            <span>Amount: {txn.amount}</span>
                        </div>
                    )}
                    
                    </>
                    : null
                
            )}
            <h2>Balance: {balance}</h2>

        </div>
    )
}