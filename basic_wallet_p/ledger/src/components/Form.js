
import React, { Component } from 'react'
import axios from 'axios';

export default class Form extends Component {
  state = {
    id: ""
  }

  handleChange = ({target: {name, value}}) => this.setState({[name]: value})

  handleSubmit = e => {
    e.preventDefault()
    if(this.state.id.trim() === "") {
      alert("Must provide an ID to filter by")
    } else {
      this.props.filterChain(this.state.id)
    }
  }

  render() {
    return (
      <form onSubmit={this.handleSubmit}>
        <h2>Enter the id of the recipient to track</h2>
        <label htmlFor="id">Id:</label>
        <input type="text" value={this.state.id} onChange={this.handleChange} name="id" />
        <input type="submit" value="Filter By Id"/>
      </form>
    )
  }
}