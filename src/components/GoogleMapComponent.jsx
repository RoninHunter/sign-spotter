import * as React from 'react';
import {withScriptjs, withGoogleMap, GoogleMap, Marker, InfoWindow} from 'react-google-maps';
import { InputGroup } from 'react-bootstrap';

const style = require('./GoogleMapStyle.json')

const GoogleMapComponent = withScriptjs(
  withGoogleMap(props => (
    <GoogleMap
    defaultZoom = {props.mapDefaults.defaultZoom}
    defaultCenter = {props.mapDefaults.defaultCenter}
    defaultOptions = {{
      disableDefaultUI: true,
      draggable: true,
      keyboardShortcuts: false,
      scaleControl: true,
      scrollWheel: true,
      styles: style
    }}
    >
      {props.signsCurrent.map(marker => (
        <Marker
          icon = {{
            url: "/icons8-marker-20-green.svg"
          }}
          position = {{lat: marker.location[0], lng: marker.location[1]}}
          key = {marker.id}
          // {...console.log(marker.location[1])}
          onClick = {(message, lat, lng, id) =>
            props.handleMarkerClick(
              'Lat/Long' + marker.lng,
              marker.location[0],
              marker.location[1],
              marker._id
            )
          } 
        />
      ))}
      {props.signsMissing.map(marker => (
        <Marker
          icon = {{
            url: "/icons8-marker-20-red.svg"
          }}
          position = {{lat: marker.location[0], lng: marker.location[1]}}
          key = {marker.id}
          // {...console.log(marker.location[1])}
          onClick = {(message, lat, lng, id) =>
            props.handleMarkerClick(
              'Lat/Long' + marker.lng,
              marker.location[0],
              marker.location[1],
              marker._id
            )
          } 
        />
      ))}
      {props.isInfoboxVisible && (
        <InfoWindow
          position={{
            lat: props.infoboxPosY,
            lng: props.infoboxPosX
          }}
          onCloseClick={() => props.handleInfoboxClick()}
        >
          <div>
            <h4>{props.infoboxMessage}</h4>
          </div>
        </InfoWindow>
      )}
    </GoogleMap>
  ))
);

export default GoogleMapComponent