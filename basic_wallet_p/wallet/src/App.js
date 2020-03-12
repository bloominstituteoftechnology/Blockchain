import React, {useEffect} from 'react';
import WalletContext from "./contexts/WalletContext"
import './App.css';
import axios from "axios";

import Login from "./components/Login"
import Transactions from "./components/Transactions"
import SendForm from "./components/SendForm"

function App() {
  const [user, setUser] = useState("")
  const [txns, setTxns] = useState([])

  useEffect( _ => {
    axios.get("localhost:5000/chain")
    .then(r => console.log(r))
    .catch(err => console.log(error.response))
  }, user)

  return (
    <div className="App">
      <Login />
      <Transactions />
      <SendForm />
    </div>
  );
}

export default App;
