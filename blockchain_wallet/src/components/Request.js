import React, { useState, useEffect, useContext } from 'react'
import { UserContext } from '../UserContext'
import axios from 'axios'

const RequestData = (props) => {

    const ctx = useContext(UserContext)

    const [ value, setValue ] =  useState("")

    useEffect(() => {

        axios
            .get('http://localhost:5000/chain')
            .then(res => {
                ctx.setChain(res.data.chain)
            })
            .catch(err => console.log(err))

    },[]) 


    return(
        <div>
            <label>Lambda Wallet Name</label>
            <input 
            value = {value} 
            type = 'text' 
            name = 'username' 
            placeholder = 'Enter Your Crypto Name'
            onChange = {(e) => {
                setValue(e.target.value)
            }}
            ></input>
            <button type = 'submit' onClick = {() => ctx.setUser(value)}>GET WALLET</button>
        </div>
    )
}

export default RequestData