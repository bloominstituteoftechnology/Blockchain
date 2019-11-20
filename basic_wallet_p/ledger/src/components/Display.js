import React from 'react';
import Moment from 'react-moment';

export default function Display({chain, title, length, coins}) {


    if(chain.length) {

      return (
        <div className="list">
          <h3>Total Blocks: {length}</h3>
          <h3>{title}</h3>
          {coins && <h3>Coins: {coins}</h3>}
          {chain.map(block => {
            if (block.transactions[0]) {
                return (
                <div className="blockWrapper" key={block.previous_hash}>
                  <h4>Amount: {block.transactions[0].amount}</h4>
                  <h4>Sender: {block.transactions[0].sender}</h4>
                  <h4>Recipient: {block.transactions[0].recipient}</h4>
                  <h6><Moment unix format="MM/DD/YYYY HH:mm">{block.timestamp}</Moment></h6>
                </div>
              )
            }
          })}
          <code>{JSON.stringify(chain)}</code>
        </div>
      )
    } else {
      return (
      <div>
        <h3>Total: Loading...</h3>
        <p>Loading...</p>
        </div>
      )
    }
}