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

import 'proj4leaflet';
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

const mapCenter = [63.417400, 10.397518];
const zoomLevel = 14;

const crs = new window.L.Proj.CRS(
  'EPSG:25833',
  '+proj=utm +zone=33 +ellps=GRS80 +units=m +no_defs ',
  {
    resolutions: [
      21674.7100160867,
      10837.35500804335,
      5418.677504021675,
      2709.3387520108377,
      1354.6693760054188,
      677.3346880027094,
      338.6673440013547,
      169.33367200067735,
      84.66683600033868,
      42.33341800016934,
      21.16670900008467,
      10.583354500042335,
      5.291677250021167,
      2.6458386250105836,
      1.3229193125052918,
      0.6614596562526459,
      0.33072982812632296,
      0.16536491406316148,
    ],
    origin: [-2500000.0, 9045984.0],
    // transformation: Leaflet.Transformation(1, 0, -1, 0)
  },

);


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
        crs={crs}
      >
        <TileLayer
          url="http://nvdbcache.geodataonline.no/arcgis/rest/services/Trafikkportalen/GeocacheTrafikkJPG/MapServer/tile/{z}/{y}/{x}"
        />
      </Map>
    </div>
  </MuiThemeProvider>
);

ReactDOM.render(<App />, document.getElementById('root'));
registerServiceWorker();
