import React, {useState, useContext} from "react";
import WalletContext from "../contexts/WalletContext"
import axios from "axios";

export default function SendForm() {

    const INITIAL_TXN = {
        
        recipient: "",
        amount: ""
    }

    const {user, txns, setTxns} = useContext(WalletContext)
    const [newTxn, setNewTxn] = useState(INITIAL_TXN)

    const handleChange = e => {
        setNewTxn({...newTxn, [e.target.name]: e.target.value})
    }
    const handleSubmit = e => {
        e.preventDefault()
        axios.post("http://localhost:5000/transactions/new", {...newTxn, sender: user})
            .then(r => {
                console.log(r);
                setTxns([...txns, [{...newTxn, sender: user, pending: true}] ])
                setNewTxn(INITIAL_TXN);

            })
            .catch(err => console.log(err.response))
    }

    return(
        <>
        { user ? 
        <form className="send-form" onSubmit={handleSubmit}>
            <h3>Send from {user}</h3>
            <label>Send to:
            <input
            name="recipient"
            value={newTxn.recipient}
            onChange={handleChange} /></label>
            <label>Amount
            <input
            name="amount"
            value={newTxn.amount}
            onChange={handleChange} /></label>

            <button type="submit">Send</button>
        </form>
        : null}
        </>
    )
}