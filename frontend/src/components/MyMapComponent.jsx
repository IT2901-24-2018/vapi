import React from 'react';
// import ReactDOM from "react-dom"; //unused reactdom since component are exported
import { compose, withProps } from 'recompose';
import { withScriptjs, withGoogleMap, GoogleMap, Marker } from 'react-google-maps';

// Default map component with marker from library
const MyMapComponent = compose(
  withProps({
    /** API Key
     * AIzaSyBdDmKkxJcu6FlyK0Z9SOEEGEMk9U_Daig
     */
    googleMapURL:
      'https://maps.googleapis.com/maps/api/js?key=AIzaSyBdDmKkxJcu6FlyK0Z9SOEEGEMk9U_Daig&v=3.exp&libraries=geometry,drawing,places',
    loadingElement: <div style={{ height: '100%' }} />,
    containerElement: <div style={{ height: '60vh' }} />,
    mapElement: <div style={{ height: '100%' }} />,
  }),
  withScriptjs,
  withGoogleMap,
)(props => (
  <GoogleMap defaultZoom={14} defaultCenter={{ lat: 63.387075002372903, lng: 10.3277250005425 }}>
    {props.isMarkerShown && (
      <Marker position={{ lat: 63.387075002372903, lng: 10.3277250005425 }} />
    )}
  </GoogleMap>
));

export default MyMapComponent;

/**
 * var startLats = [63.387075002372903, 63.387691997704202, 63.387642998353499, 63.387514999582102
 * , 63.387520001503702, 63.398216997487999, 63.398066997137299, 63.398084999471202];
        var startLongs = [10.3277250005425, 10.3290819995141, 10.3282330021124, 10.328351999716901
          , 10.3280969991206, 10.3594619979811, 10.3578219979658, 10.357628000185899];
        var endLats = [63.387441999029399, 63.387777001722696, 63.387514999582102
          , 63.387471999099603, 63.387520001503702, 63.398066997137299, 63.398084999471202
          , 63.398135001497998];
        var endLongs = [10.3290930003037, 10.328826998917799, 10.328351999716901, 10.3280570009369
          , 10.3283469977953, 10.3578219979658, 10.357628000185899, 10.357228001160401];
        */
