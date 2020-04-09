import React, { Component } from 'react';
import Dialog from '@material-ui/core/Dialog';
import AppBar from '@material-ui/core/AppBar';
import MuiThemeProvider from '@material-ui/core/styles/MuiThemeProvider';

import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import Image from 'react-bootstrap/Image'
import NavBar from './NavBar';
import { AlertHeading } from 'react-bootstrap/Alert';


const fontStyling = {
  fontSize: '72px',
  color: 'blue'
}


export class HomePage extends Component {


  render() {
    return (

      <div style={{
           fontFamily: 'Helvetica',
          //display: 'flex', 
          textAlign: 'left',
          textJustify: 'auto',
          padding: '110px',
          lineHeight: '25px'
        }}>

      <h1>signSpotter</h1>

         <p>
           {/* <b>SignSpotter </b>  */}
          A tool that allows its users to upload videos for object detection labeling, 
          specifically traffic signs. Users will receive an email after the video is 
          processed to download the labeled data. The app will also allow the user to 
          export data as a KMZ and allow for asset managment capablilities such as 
          determining if signs are missing from two video files of the same location.
        </p>

      
      </div>
    );
  }
}

export default HomePage;