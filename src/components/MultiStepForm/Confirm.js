import React, { Component } from 'react';
import Dialog from '@material-ui/core/Dialog';
import AppBar from '@material-ui/core/AppBar';
import MuiThemeProvider from '@material-ui/core/styles/MuiThemeProvider';
import { List, ListItem, ListItemText } from '@material-ui/core/';
import Button from '@material-ui/core/Button';

export class Confirm extends Component {
  continue = e => {
    this.props.submitForm();
    this.props.nextStep();
  };

  back = e => {
    e.preventDefault();
    this.props.prevStep();
  };

  fileList() {
    if(this.props.values.files) {
      const fileList = this.props.values.files.map(file => (
        <li key={file.path}>
          {file.path} - {file.size} bytes
        </li>
      ));
      return(
        <div>
          {fileList}
        </div>
      )
    }
  }


  render() {
    const {
      values: { firstName, lastName, email, files}
    } = this.props;
    return (
      <MuiThemeProvider >
        <React.Fragment>
          <Dialog
            open="true"
            fullWidth="true"
            maxWidth='sm'
          >
          <AppBar title="Confirm User Data" />
          <List>
            <ListItem>
              <ListItemText primary="Files" secondary={this.fileList()} />
            </ListItem>
            <ListItem>
              <ListItemText primary="First Name" secondary={firstName} /> 
            </ListItem>
            <ListItem>
              <ListItemText primary="Last Name" secondary={lastName} /> 
            </ListItem>
            <ListItem>
              <ListItemText primary="Email" secondary={email} /> 
            </ListItem>
          </List>
          <br />
        
          <Button
            color="secondary"
            variant="contained"
            onClick={this.back}
          >Back</Button>

          <Button
            color="primary"
            variant="contained"
            onClick={this.continue}
          >Confirm & Continue</Button>
          </Dialog>
        </React.Fragment>
      </MuiThemeProvider>
    );
  }
}

export default Confirm;