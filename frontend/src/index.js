import React from 'react';
import ReactDOM from 'react-dom';

import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import getMuiTheme from 'material-ui/styles/getMuiTheme';

import AppBar from 'material-ui/AppBar';

import './sanitize.css';
import './base.css';

import Map from './components/Map/Map';

import registerServiceWorker from './registerServiceWorker';

const COLOR_SCHEME = {
  orange: '#ff9600',
  grayDark: '#444f55',
  grayMid: '#dadada',
  blue: '#008ec2',
  green: '#5db82e',
  grayLight: '#f5f5f5',
};

const THEME = getMuiTheme({
  palette: {
    primary1Color: COLOR_SCHEME.grayDark,
    primary2Color: COLOR_SCHEME.orange,
    accent1Color: COLOR_SCHEME.orange,
    pickerHeaderColor: COLOR_SCHEME.grayDark,
  },
});

const App = () => (
  <MuiThemeProvider muiTheme={THEME}>
    <AppBar
      title="Orm"
      showMenuIconButton={false}
    />
    <Map isMarkerShown />
  </MuiThemeProvider>
);

ReactDOM.render(<App />, document.getElementById('root'));
registerServiceWorker();
