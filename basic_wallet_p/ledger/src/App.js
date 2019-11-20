import React, { Component } from 'react';
import Display from './components/Display';
import Form from './components/Form';
import axios from "axios";

class App extends Component {
  state={
    chain: [],
    title: "Whole Chain",
    coins: null,
    filteredChain: [],
    id: null
  }

  componentDidMount() {
    this.getChain()
  }

  getChain = () => {
    axios.get('http://localhost:5000/chain')
    .then(({data}) => this.setState({chain: data.chain}))
    .catch(err => console.error(err))
  }

  filterChain = (id) => {
    console.log("CHAIN: ", this.state.chain, "\n id: ", id)
    const filteredChain = this.state.chain.filter(block => {
      console.log("block: ", block)
      if (!block.transactions.length) {
        return false
      }
      else {
        return block.transactions[0].recipient === id
      } 
    })
    if (!filteredChain.length) {
      this.setState({
        warning: "No user by that id was found",
        title: "Whole Chain",
        filteredChain: [],
        coins: null
      })
      setTimeout(() => {
        this.setState({warning: ''})
      }, 3000);
    }
    else {
      this.setState(
      {
        id,
        title: `${id}'s Transactions`,
        filteredChain,
        warning: null
      }
      )
      setTimeout(() => {
        this.getCoins(id)
      }, 500);
    }
  } 

  getCoins = (id) => {
    let totalCoins = 0;
    this.state.filteredChain.forEach(block => {
      console.log("COINS FOREACH: ", block, id)
      if(block.transactions[0].recipient === id) {
        return totalCoins += block.transactions[0].amount
      }
      if(block.transactions[0].sender === id) {
        return totalCoins -= block.transactions[0].amount
      }
    })
    this.setState({coins: totalCoins})
  }

  render() {
    return (
      <div className="App">
        <Form 
          filterChain={this.filterChain}
        />
        <h2>{this.state.warning}</h2>
        <Display 
          coins={this.state.coins}
          chain={this.state.filteredChain.length ? this.state.filteredChain : this.state.chain}
          title={this.state.title}
          length={this.state.chain.length}
        />
      </div>
    );
  }
}

export default App;