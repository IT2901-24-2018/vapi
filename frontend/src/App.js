import React, { Component } from "react";
import logo from "./logo.svg";
import "./App.css";
import MyMapComponent from "./components/MyMapComponent.js";

class App extends Component {
  render() {
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h1 className="App-title">Welcome to BIT24</h1>
        </header>
        <p className="App-intro">
          It's got React, and like, Django, and stuff.
        </p>
        <MyMapComponent isMarkerShown />
      </div>
    );
  }
}

export default App;
