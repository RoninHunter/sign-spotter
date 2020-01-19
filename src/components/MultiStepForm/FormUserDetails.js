import React, { Component } from 'react';
import Dialog from '@material-ui/core/Dialog';
import Typography from '@material-ui/core/Typography';
import AppBar from '@material-ui/core/AppBar';
import MuiThemeProvider from '@material-ui/core/styles/MuiThemeProvider';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import VideoUploadForm from './VideoUploadForm';
import { Card } from 'react-bootstrap';
import { Paper } from '@material-ui/core';
//import MainComp from '../components/MainComp';
//import DescriptionComp from './DescriptionComp';


const style = {
  height: 75,
  width: 320,
  margin: "1em",
  textAlign: 'center',
  display: 'inline-block',
  justify: 'center',
};



export class FormUserDetails extends Component {
  continue = e => {
    e.preventDefault();
    this.props.nextStep();
  };

  
  render() {
    const { values, handleChange } = this.props;
    return (
        <MuiThemeProvider >
        
          <React.Fragment>
            
            <Dialog 
              open="true"
              fullWidth="true"
              maxWidth='sm'
            >



              <Paper 
                style = {style}  
                elevation = {0}
              >
                <Typography variant = "h5" component = "h3"> 
                  Video Upload 
                </Typography>
              </Paper>

              <VideoUploadForm uploadVideo={this.props.uploadVideo} />


              <AppBar title="Enter User Details" />
              <TextField
                placeholder="Enter Your First Name"
                label="First Name"
                onChange={handleChange('firstName')}
                defaultValue={values.firstName}
                margin="normal"
                fullWidth="true"
              />
              <br />
              <TextField
                placeholder="Enter Your Last Name"
                label="Last Name"
                onChange={handleChange('lastName')}
                defaultValue={values.lastName}
                margin="normal"
                fullWidth="true"
              />
              <br />
              <TextField
                placeholder="Enter Your Email"
                label="Email"
                onChange={handleChange('email')}
                defaultValue={values.email}
                margin="normal"
                fullWidth="true"
              />
              <br />
              <Button
                color="primary"
                variant="contained"
                onClick={this.continue}
              >Continue</Button>
            </Dialog>
          </React.Fragment>
        </MuiThemeProvider>
    );
  }
}

export default FormUserDetails;