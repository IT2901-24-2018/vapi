import React from 'react';
import ReactDOM from 'react-dom';

import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import Toggle from 'material-ui/Toggle';

import './base.css';

import MyMapComponent from './components/MyMapComponent/MyMapComponent';

import registerServiceWorker from './registerServiceWorker';

const App = () => (
  <MuiThemeProvider>
    <div className="App">
      <Toggle
        defaultToggled
      />
      <MyMapComponent isMarkerShown />
    </div>
  </MuiThemeProvider>
);

ReactDOM.render(<App />, document.getElementById('root'));
registerServiceWorker();
