import React from 'react';
import ReactDOM from 'react-dom';

import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import Toggle from 'material-ui/Toggle';

import './base.css';
import './index.css';

import logo from './assets/logo.svg';

import MyMapComponent from './components/MyMapComponent/MyMapComponent';

import registerServiceWorker from './registerServiceWorker';

const App = () => (
  <MuiThemeProvider>
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <h1 className="App-title">Welcome to ORM</h1>
      </header>
      <Toggle
        defaultToggled
      />
      <p className="App-intro"> {" It's got React, and like, Django, and stuff. "}</p>
      <MyMapComponent isMarkerShown />
    </div>
  </MuiThemeProvider>
);

ReactDOM.render(<App />, document.getElementById('root'));
registerServiceWorker();
