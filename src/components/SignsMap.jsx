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

class Map extends React.PureComponent {
  constructor(props) {
    super(props)

    this.state = {
      infoboxMessage: 'Message',
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
      }],
      signsMissing: [{
        lat: 28.042784,
        lng: -81.957089
      }]
    }
  }

  handleMarkerClick = (message, lat, lng) => {
    this.setState({
      infoboxMessage: message,
      isInfoboxVisible: !this.state.isInfoboxVisible,
      markerLng: lng + 0.006,
      markerLat: lat - 0.0004

    })
    console.log(this.state)
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
          googleMapURL="https://maps.googleapis.com/maps/api/js?v=3.exp&libraries=geometry,drawing,places&key=AIzaSyByBIpxElZbrcCGHnno141apTYc6tbLcoM"
          loadingElement={<div style={{ height: `100%` }} />}
          containerElement={<div style={{ height: `100%` }} />}
          mapElement={<div style={{ height: `100%` }} />}
          isInfoboxVisible={this.state.isInfoboxVisible} // Show/hide info window
          infoboxMessage={this.state.infoboxMessage} // Message shown in info window
          handleInfoboxClick={this.handleInfoboxClick} // Handle closing of the info window
          handleMarkerClick={this.handleMarkerClick} // Handle click on Marker component
          infoboxPosY={this.state.markerLng} // Y coordinate for positioning info window
          infoboxPosX={this.state.markerLat} // X coordinate for positioning info window
          signsCurrent={this.state.signsCurrent}
          signsMissing={this.state.signsMissing}
        />
        <a target="_blank" href="https://icons8.com/icons/set/undefined">Marker icons</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>
      </div>
    );
  }
}

export default Map;