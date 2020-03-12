import React, {useState, useEffect} from 'react';
import WalletContext from "./contexts/WalletContext"
import './App.css';
import axios from "axios";
import Pusher from "pusher-js";

import Login from "./components/Login"
import Transactions from "./components/Transactions"
import SendForm from "./components/SendForm"

function App() {
  const [user, setUser] = useState("");
  const [txns, setTxns] = useState([]);
  const [balance, setBalance] = useState(0);


  const getTxns = _ => {
    axios.get("http://localhost:5000/chain")
    .then(r => {
      // console.log(r.data)
      setTxns(r.data.chain.map(item => item.transactions.filter(item => item.sender === user || item.recipient === user)))
    })
    .catch(err => console.log(err.response))
  }

  var pusher = new Pusher('48b94c735bb4bae49e16', {
    cluster: 'us2',
    forceTLS: true
  });

  var channel = pusher.subscribe('block');
  channel.bind('new-block', function(data) {
    getTxns();
    console.log(data.message)
  });



  useEffect( _ => {
    getTxns();
    console.log("user changed")
  }, [user])

  useEffect( _ => {
    let newBalance = 0;
    txns.map(item => 
        item.map(txn => {
          if (txn.sender === user) {
            newBalance -= Number(txn.amount);
          } if (txn.recipient === user) {
            newBalance += Number(txn.amount)
          }
        })
      )
      setBalance(newBalance)
  }, [txns])

  return (
    <WalletContext.Provider value={{user, setUser, txns, setTxns, balance, setBalance}}>
      <div className="App">
        <Login />
        <Transactions />
        <SendForm />
      </div>
    </WalletContext.Provider>
  );
}

export default App;
