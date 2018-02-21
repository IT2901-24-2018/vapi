import React from 'react';
import ReactDOM from 'react-dom';

import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import AppBar from 'material-ui/AppBar';

import './sanitize.css';
import './base.css';

import Map from './components/Map/Map';

import registerServiceWorker from './registerServiceWorker';

const App = () => (
  <MuiThemeProvider>
    <AppBar
      title="Orm"
      showMenuIconButton={false}
    />
    <Map isMarkerShown />
  </MuiThemeProvider>
);

ReactDOM.render(<App />, document.getElementById('root'));
registerServiceWorker();
