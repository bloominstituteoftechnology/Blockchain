import React, {useEffect, useState} from 'react';
import axios from 'axios';

export default function Wallet(){

    const [state, setState] = useState([]);
    const [id, setId] = useState();
    const [total, setTotal] = useState()

    const transactions = []
    const trans2 = []
    const trans3 = []
    const trans4 = []
    const trans5 = []

    const changeHandler = e => {
        e.persist();
        setId({
            ...id,
            [e.target.name] : e.target.value
        })
    }

    const separate = () =>{
        for (let i = 0; i < state.length; i++){
            transactions.push(state[i].transactions);
        };
    }

    const formulate = () =>{
        for (let i = 0; i < transactions.length; i++){
            trans2.push(transactions[i])
        }
    }

    const granulate = () =>{
        for (let i = 0; i < trans2.length; i++){
            trans3.push(trans2[i])
        }
    }

    const infuriate = () =>{
        for (let i = 0; i < trans3.length; i++){
            trans4.push(trans3[i])
        }
    }

    const finalize = () =>{
        for (let i = 0; i < trans4.length; i++){
            trans5.push(trans4[i])
        }
    }

    const tabulate = () =>{
        let pretotal = 0
        for(let i = 0; i < trans5.length; i++){
            if(trans5[i].recipient === id){
                setTotal(pretotal + trans5[i].amount)
            }
        }
        console.log(pretotal)
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

    separate();
    formulate();
    granulate();
    infuriate();
    finalize();
    tabulate();

    console.log(id)
    console.log(state)
    console.log(trans5)
    

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