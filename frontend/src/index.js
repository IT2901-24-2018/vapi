import React from 'react';
import ReactDOM from 'react-dom';

import 'leaflet/dist/leaflet.css';

import { Map, TileLayer } from 'react-leaflet';

import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import getMuiTheme from 'material-ui/styles/getMuiTheme';

import AppBar from 'material-ui/AppBar';
import Paper from 'material-ui/Paper';
import FlatButton from 'material-ui/FlatButton';
import RaisedButton from 'material-ui/RaisedButton';
import Divider from 'material-ui/Divider';
import Toggle from 'material-ui/Toggle';
import DatePicker from 'material-ui/DatePicker';
import * as _colorManipulator from 'material-ui/utils/colorManipulator';

import './sanitize.css';
import './base.css';

import registerServiceWorker from './registerServiceWorker';

const styles = {
  paper: {
    width: 512,
    padding: 32,
    margin: '32px auto',
    textAlign: 'center',
  },
  divider: {
    marginTop: 16,
    marginBottom: 16,
  },
};

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

const stamenTonerTiles = 'http://stamen-tiles-{s}.a.ssl.fastly.net/toner-background/{z}/{x}/{y}.png';
const stamenTonerAttr = 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>';
const mapCenter = [39.9528, -75.1638];
const zoomLevel = 12;

const App = () => (
  <MuiThemeProvider muiTheme={THEME}>
    <div>
      <AppBar
        title="Orm"
        showMenuIconButton={false}
      />
      <Paper style={styles.paper} zDepth={1}>
        <FlatButton label="Primary" primary />
        <FlatButton label="Secondary" secondary />
        <Divider style={styles.divider} />
        <RaisedButton label="Primary" primary />
        <RaisedButton label="Secondary" secondary />
        <Divider style={styles.divider} />
        <Toggle
          defaultToggled
        />
        <Toggle
          thumbSwitchedStyle={{
            backgroundColor: COLOR_SCHEME.orange,
          }}
          trackSwitchedStyle={{
            backgroundColor: _colorManipulator.fade(COLOR_SCHEME.orange, 0.5),
          }}
          defaultToggled
        />
        <Divider style={styles.divider} />
        <DatePicker hintText="Portrait Dialog" />
        <p>hey ha</p>
      </Paper>
      <Map
        center={mapCenter}
        zoom={zoomLevel}
      >
        <TileLayer
          attribution={stamenTonerAttr}
          url={stamenTonerTiles}
        />
      </Map>
    </div>
  </MuiThemeProvider>
);

ReactDOM.render(<App />, document.getElementById('root'));
registerServiceWorker();
