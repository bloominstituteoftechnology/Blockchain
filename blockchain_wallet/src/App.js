import React, { useState, useMemo } from 'react';
import Header from './components/Header'
import RequestData from './components/Request'
import { UserContext } from './UserContext'

function App() {

  const [ user, setUser ] = useState(null)

  const providerValue = useMemo(() => ({user, setUser}), [user, setUser])

  return (
    <div className="App">
      <Header />
        <UserContext.Provider value = {providerValue}>
          <RequestData />
        </UserContext.Provider>
    </div>
  );
}

export default App;
