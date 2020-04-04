import React, { Component } from 'react';
import GoogleMapComponent from './GoogleMapComponent'
import axios from 'axios';

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
      mapDefaults: {
        defaultZoom: 13,
        defaultCenter: {
          lat: 28.039465,
          lng: -81.949806
        }
      },
      infoboxMessage: 'Message',
      isInfoboxVisible: false,
      markerLng: 0,
      markerLat: 0,
      signsCurrent: [],
      signsMissing: []
    }
  }

  handleMarkerClick = (message, lat, lng, id) => {
    this.setState({
      infoboxMessage: message,
      markerLng: lng,
      markerLat: lat + 0.004
    })
    this.setState({
      isInfoboxVisible: !this.state.isInfoboxVisible
    })
    // console.log(id)
  }

  handleInfoboxClick = () => {
    console.log(this.state)
    this.setState({
      isInfoboxVisible: false
    })
  }
  
  componentDidMount() {
    axios.get('http://localhost:8080/api/locations/current', {
    }).then((res) => {
      this.setState({
        signsCurrent: res.data
      })
    })

    axios.get('http://localhost:8080/api/locations/missing', {
    }).then((res) => {
      this.setState({
        signsMissing: res.data
      })
    })
  }

  componentDidUpdate() {
    // console.log(this.state.signs)
  }

  render() {
    return (
      <div style = {styles}>
        <GoogleMapComponent
          googleMapURL="https://maps.googleapis.com/maps/api/js?v=3.exp&libraries=geometry,drawing,places&key=AIzaSyByBIpxElZbrcCGHnno141apTYc6tbLcoM"
          loadingElement={<div style={{ height: `100%` }} />}
          containerElement={<div style={{ height: `100%` }} />}
          mapElement={<div style={{ height: `100%` }} />}
          mapDefaults={this.state.mapDefaults}
          isInfoboxVisible={this.state.isInfoboxVisible} // Show/hide info window
          infoboxMessage={this.state.infoboxMessage} // Message shown in info window
          handleInfoboxClick={this.handleInfoboxClick} // Handle closing of the info window
          handleMarkerClick={this.handleMarkerClick} // Handle click on Marker component
          infoboxPosX={this.state.markerLng} // Y coordinate for positioning info window
          infoboxPosY={this.state.markerLat} // X coordinate for positioning info window
          signsCurrent={this.state.signsCurrent}
          signsMissing={this.state.signsMissing}
          // signs={this.state.signs}
        />
        <a target="_blank" href="https://icons8.com/icons/set/undefined">Marker icons</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>
      </div>
    );
  }
}

export default Map;