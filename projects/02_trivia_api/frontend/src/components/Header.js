import React, { Component } from 'react';
import '../stylesheets/Header.css';

class Header extends Component {

  navTo(uri){
    window.location.href = window.location.origin + uri;
  }

  render() {
    return (
      <div className="App-header">
        <h2 onClick={() => {this.navTo('')}}>Review</h2>
        <h2 onClick={() => {this.navTo('/add')}}>Add</h2>
        <h2 onClick={() => {this.navTo('/play')}}>Quiz</h2>
      </div>
    );
  }
}

export default Header;
