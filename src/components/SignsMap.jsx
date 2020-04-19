import React, { Component } from 'react';
import DownloadButton from './DownloadButton';
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

  handleMarkerClick = (sign_class, lat, lng, missing, last_sighting, image_id) => {
    let message = [sign_class, lat, lng, String(missing), last_sighting]
    this.setState({
      markerLng: lng,
      markerLat: lat,
      infoboxMessage: message,
      isInfoboxVisible: !this.state.isInfoboxVisible
    })
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

  render() {
    return (
      <div className="map" style = {styles}>


        <LoadingButton />

        <GoogleMapComponent
          googleMapURL="https://maps.googleapis.com/maps/api/js?v=3.exp&libraries=geometry,drawing,places&key=AIzaSyByBIpxElZbrcCGHnno141apTYc6tbLcoM"
          loadingElement={<div style={{ height: `100%` }} />}
          containerElement={<div style={{ height: `100%` }} />}
          mapElement={<div style={{ height: `100%` }} />}
          
          mapDefaults={this.state.mapDefaults}
          isInfoboxVisible={this.state.isInfoboxVisible}
          infoboxMessage={this.state.infoboxMessage}
          handleInfoboxClick={this.handleInfoboxClick}
          handleMarkerClick={this.handleMarkerClick}
          infoboxPosX={this.state.markerLng}
          infoboxPosY={this.state.markerLat}
          signsCurrent={this.state.signsCurrent}
          signsMissing={this.state.signsMissing}
        />
        <a target="_blank" href="https://icons8.com/icon/8818/facebook-old">Marker icons by Icons8</a>
      </div>
    );
  }
}

export default Map;