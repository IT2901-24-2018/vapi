import React from 'react';
import ReactDOM from 'react-dom';
import MyMapComponent from '../MyMapComponent';

it('renders without crashing', () => {
  const div = document.createElement('div');
  ReactDOM.render(<MyMapComponent />, div);
  ReactDOM.unmountComponentAtNode(div);
});
