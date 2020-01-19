import React, { Component } from 'react';
import Dialog from '@material-ui/core/Dialog';
import AppBar from '@material-ui/core/AppBar';
import MuiThemeProvider from '@material-ui/core/styles/MuiThemeProvider';
import {Redirect} from 'react-router-dom';

export class Success extends Component {
  state = {
    redirect: false
  }

  continue = e => {
    e.preventDefault();
    this.props.nextStep();
  };

  back = e => {
    e.preventDefault();
    this.props.prevStep();
  };

  componentDidMount() {
    setTimeout(() => {
      this.setState({
        redirect: true
      })
    }, 5000);
  }

  render() {
    if(this.state.redirect) {
      return (
        <Redirect to='/home' />
      )
    }
    return (
      <MuiThemeProvider > 
        <React.Fragment>
        <Dialog open="true" fullWidth="true" maxWidth='sm'>
            <AppBar title="Success" />
            <h1> Thank You For Using SignSPOTTER </h1>
            <p> You will receive an email with the status of your sign search </p>
          </Dialog>
        </React.Fragment>
      </MuiThemeProvider>
    );
  }
}

export default Success;