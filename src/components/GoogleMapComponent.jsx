import * as React from 'react';
import {withScriptjs, withGoogleMap, GoogleMap, Marker, InfoWindow} from 'react-google-maps';
import { InputGroup } from 'react-bootstrap';

const style = require('./GoogleMapStyle.json')

const GoogleMapComponent = withScriptjs(
  withGoogleMap(props => (
    <GoogleMap
    defaultZoom = {13}
    defaultCenter = {{
      lat: 28.039465,
      lng: -81.949806
    }}
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
          position = {{lat: marker.lat, lng: marker.lng}}
          key = {marker.id}
          onClick = {(message, lat, lng) =>
            props.handleMarkerClick(
              'Lat/Long',
              28.030431,
              -81.957186
            )
          } 
        />
      ))}
      {/* {props.signsMissing.map(marker => (
        <Marker
          icon = {{
            url: "/icons8-marker-20-red.svg"
          }}
          position = {{lat: marker.lat, lng: marker.lng}}
          key = {marker.id}
          onClick = {(message, lng, lat) =>
              props.handleMarkerClick(
                'Lat/Long',
                28.030431,
                -81.957186
              )
          } 
        />
      ))}
       */}
      {props.isInfoboxVisible && (
        <InfoWindow
          position = {{
            lat: props.infoBoxPosY,
            lng: props.infoBoxPosX
          }}
          onCloseClick = {() => props.handleInfoboxClick()}
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