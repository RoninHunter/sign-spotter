import React, { Component } from 'react';
import Dialog from '@material-ui/core/Dialog';
import AppBar from '@material-ui/core/AppBar';
import MuiThemeProvider from '@material-ui/core/styles/MuiThemeProvider';

import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import Image from 'react-bootstrap/Image'
import NavBar from './NavBar';




export class HomePage extends Component {
  // continue = e => {
  //   e.preventDefault();
  //   // PROCESS FORM //
  //   this.props.nextStep();
  // };

  // back = e => {
  //   e.preventDefault();
  //   this.props.prevStep();
  // };

  render() {
    return (
      <MuiThemeProvider > 
        <React.Fragment>
        <Dialog 
            open="true"
            fullWidth="true"
            maxWidth='sm'
          >
             <NavBar />
            <AppBar title="HomePage" />
            <h1> SignSPOTTER </h1>
            <p> Sign spotting for life </p>
          </Dialog>
        </React.Fragment>
      </MuiThemeProvider>
    );
  }
}

export default HomePage;