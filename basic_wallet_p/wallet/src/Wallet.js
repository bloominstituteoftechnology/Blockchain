import React, {useEffect, useState} from 'react';
import axios from 'axios';

export default function Wallet(){

    const [state, setState] = useState([{}]);
    const [id, setId] = useState();
    const [total, setTotal] = useState()

    const transactions = []
    const list2 = []
    
 

    const changeHandler = e => {
        e.persist();
        setId({
            ...id,
            [e.target.name] : e.target.value
        })
    }

    const grab = () => {
        axios
            .get('http://0.0.0.0:5000/chain')
            .then(res => setState(res.data.chain))
            .catch(err => console.log(err))
            }

    useEffect(()=>{
        grab();
    }, [])

    const sortitout = () => {
        for(let i=0;i<state.length;i++){
            transactions.push(state[i].transactions)
        }
        for(let i=0;i<transactions.length;i++){
            list2.push(transactions[1])
        }
    
    }

    sortitout();

    // console.log(id)
    // console.log(state)
    console.log(transactions)
    console.log(list2)
    
    

    return(
        <div>
            <p>Hey now: {total}</p>
            <input type="text"
            placeholder="ID here"
            name="id"
            onChange={changeHandler}/>
            <button>Submit</button>
            
            
        
        </div>
    )
}