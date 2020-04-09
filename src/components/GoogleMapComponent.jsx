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
          onClick = {(sign_class, lat, lng, missing, last_sighting, image_id) =>
            props.handleMarkerClick(
              marker.class,
              marker.location[0],
              marker.location[1],
              marker.missing,
              marker.last_sighting,
              marker.image_id
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
          onClick = {(sign_class, lat, lng, missing, last_sighting, image_id) =>
            props.handleMarkerClick(
              marker.class,
              marker.location[0],
              marker.location[1],
              marker.missing,
              marker.last_sighting,
              marker.image_id
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
            <h4>Sign: {props.infoboxMessage[0]}</h4>
            <h4>Latitude: {props.infoboxMessage[1]}</h4>
            <h4>Longitude: {props.infoboxMessage[2]}</h4>
            <h4>Missing: {props.infoboxMessage[3]}</h4>
            <h4>Last Sighting: {props.infoboxMessage[4]}</h4>
          </div>
        </InfoWindow>
      )}
    </GoogleMap>
  ))
);

export default GoogleMapComponent