import React, { useState, useEffect, useContext } from 'react'
import { UserContext } from '../UserContext'
import axios from 'axios'

const RequestData = (props) => {

    const ctx = useContext(UserContext)

    const [ value, setValue ] =  useState("")

    const handleSubmit = (e) => {

        e.preventDefault()

        if (value != ''){
            axios
            .get('http://localhost:5000/chain')
            .then(res => console.log(res))
            .catch(err => console.log(err))
        }

    }

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
            <button type = 'submit' onClick = {(e) => handleSubmit(e)}>GET WALLET</button>
        </div>
    )
}

export default RequestData