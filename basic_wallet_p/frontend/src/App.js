import React from 'react';
import './App.css';

import Data from './Data.js';

// this is where I make the visual to the wallet.
//send transactions and then view stuff. maybe look at each persons total.
//doesn't need to be pretty.. just needs to work and display "all the things per the basic_wallet_p README.txt file"
function App() {

  //setup useEffect with hook to pull and setup state for this page to then render below
  // will need a form to input transactions : -sender, -recipient, -amount

  return (
    <div className="App">
      <header className="App-header">
        <p>
          MY ATTEMPT AT THIS FRONTEND WALLET
        </p>
      </header>
      <section>
        <h2>All Transactions</h2>
        <Data />
      </section>
    </div>
  );
}

export default App;
