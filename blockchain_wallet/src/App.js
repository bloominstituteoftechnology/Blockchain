import React, { useState, useMemo } from 'react';
import Header from './components/Header'
import RequestData from './components/Request'
import { UserContext } from './UserContext'
import Wallet from './components/Wallet'
import Transaction from './components/Transaction'

function App() {

  const [ user, setUser ] = useState(null)
  const [ chain, setChain ] = useState(null)

  const providerValue = useMemo(() => ({
    user, 
    setUser, 
    chain, 
    setChain
  }), [user, setUser, chain, setChain])

  return (
    <div className="App">
      <Header />
        <UserContext.Provider value = {providerValue}>
          <RequestData />
          <Wallet/>
          <Transaction/>
        </UserContext.Provider>
    </div>
  );
}

export default App;
