import React from 'react';
// import ReactDOM from "react-dom"; //unused reactdom since component are exported
import { compose, withProps } from 'recompose';
import { withScriptjs, withGoogleMap, GoogleMap, Marker } from 'react-google-maps';

const styles = {
  mapHeight: {
    height: '100%',
  },
  mapContainerHeight: {
    height: 'calc(100% - 64px)',
  },
};

// Default map component with marker from library
const Map = compose(
  withProps({
    /** API Key
     * AIzaSyBdDmKkxJcu6FlyK0Z9SOEEGEMk9U_Daig
     */
    googleMapURL:
      'https://maps.googleapis.com/maps/api/js?key=AIzaSyBdDmKkxJcu6FlyK0Z9SOEEGEMk9U_Daig&v=3.exp&libraries=geometry,drawing,places',
    loadingElement: <div style={styles.mapHeight} />,
    containerElement: <div style={styles.mapContainerHeight} />,
    mapElement: <div style={styles.mapHeight} />,
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

export default Map;
