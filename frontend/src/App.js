import React from 'react';
import logo from './media/logo.svg';
import './App.css';
import MyMapComponent from './components/MyMapComponent/MyMapComponent';

const App = () => (
  <div className="App">
    <header className="App-header">
      <img src={logo} className="App-logo" alt="logo" />
      <h1 className="App-title">Welcome to BIT24</h1>
    </header>
    <p className="App-intro"> {" It's got React, and like, Django, and stuff. "}</p>
    <MyMapComponent isMarkerShown />
  </div>
);

export default App;
