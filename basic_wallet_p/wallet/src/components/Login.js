import React, {useState, useContext} from "react";
import WalletContext from "../contexts/WalletContext"


export default function Login() {
    const {user, setUser} = useContext(WalletContext)
    const [newUser, setNewUser] = useState("")

    const handleChange = e => {
        setNewUser(e.target.value)
    }
    const handleSubmit = e => {
        e.preventDefault();
        setUser(newUser);
    }

    return(
        <form onSubmit={handleSubmit}>
            <input
            name="newUser"
            value={newUser}
            onChange={handleChange} />
            <button type="submit">{user ? "Change User" : "Open Wallet"}</button>
        </form>
    )
}