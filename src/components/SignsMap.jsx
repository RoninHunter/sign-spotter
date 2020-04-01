import React, { Component } from 'react';
import GoogleMapComponent from './GoogleMapComponent'

const styles = {
  width: '100%',
  height: '94%',
  padding: '2%',
  margin: '0'
}

// Icons from Icons8 https://icons8.com/icons/set/marker
const iconCredit = {
  fontSize: '10px',
  color: 'white'
}

class Map extends Component {
  constructor(props) {
    super(props)

    this.state = {
      infoboxMessage: '',
      isInfoboxVisible: false,
      markerLng: 0,
      markerLat: 0,
      signsCurrent: [{
        lat: 28.030431,
        lng: -81.957186
      },
      {
        lat: 28.054223,
        lng: -81.957218
      }]
    }
  }

  handleMarkerClick = (message, lng, lat) => {
    this.setState({
      infoMessage: message,
      isInfoboxVisible: !this.state.isInfoboxVisible,
      markerLng: lng + 0.006,
      markerLat: lat - 0.0004
    })
  }

  handleInfoboxClick = () => {
    this.setState({
      isInfoboxVisible: false
    })
  }
  
  render() {
    return (
      <div style = {styles}>
        <GoogleMapComponent
          googleMapURL="https://maps.googleapis.com/maps/api/js?v=3.exp&libraries=geometry,drawing,places&key="
          loadingElement={<div style={{ height: `100%` }} />}
          containerElement={<div style={{ height: `100%` }} />}
          mapElement={<div style={{ height: `100%` }} />}
          isInfoboxVisible={this.state.isInfoboxVisible} // Show/hide info window
          infoboxMessage={this.state.infoboxMessage} // Message shown in info window
          handleInfoboxClick={this.handleInfoboxClick} // Handle closing of the info window
          handleMarkerClick={this.handleMarkerClick} // Handle click on Marker component
          infoboxPosY={this.state.markerLang} // Y coordinate for positioning info window
          infoboxPosX={this.state.markerLat} // X coordinate for positioning info window
          markers={this.state.signsCurrent}
        />
        <a style = {iconCredit} href="https://icons8.com/icon/BE8zKVHfRaQj/marker">Marker icon by Icons8</a>
      </div>
    );
  }
}

export default Map;