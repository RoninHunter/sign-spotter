import React, { Component } from 'react';
import FormUserDetails from './FormUserDetails';
import FormPersonalDetails from './FormPersonalDetails';
import Confirm from './Confirm';
import Success from './Success';
// import { HomePage } from '../HomePage';
import axios from 'axios';

export class UserForm extends Component {
  constructor(props) {
    super(props)

    this.state = {
      step: 1,
      firstName: null,
      lastName: null,
      email: null,
      files: null
    }
  }

  // Proceed to next step
  nextStep = () => {
    const { step } = this.state;
    this.setState({
      step: step + 1
    });
    console.log("next step", this.state);
    // console.log(this.state);
  };

  // Go back to prev step
  prevStep = () => {
    const { step } = this.state;
    this.setState({
      step: step - 1
    });
  };

  // Handle fields change
  handleChange = input => e => {
    this.setState({ [input]: e.target.value });
    console.log(this.state);
  };

  uploadVideo = (files) => {
    this.setState({
      files: files
    })
  }

  submitForm = (event) => {
    const data = new FormData();
    this.state.files.forEach(file => {
      data.append('videos', file);
    });
    data.append('firstName', this.state.firstName);
    data.append('lastName', this.state.lastName);
    data.append('email', this.state.email);
    const config = {
      headers: {
        'content-type': 'multipart/form-data'
      }
    }
    axios.post('http://localhost:8080/api/videoupload', data, config).then(res => {
      console.log(res);
    });
  }

  render() {
    const { step } = this.state;
    const { firstName, lastName, email, files} = this.state;
    const values = { firstName, lastName, email, files};

    switch (step) {
      case 1:
        return (
          <FormUserDetails
            nextStep={this.nextStep}
            handleChange={this.handleChange}
            values={values}
            uploadVideo={this.uploadVideo}
          />
        );

      case 2:
        return (
          <Confirm
            nextStep={this.nextStep}
            prevStep={this.prevStep}
            values={values}
            submitForm={this.submitForm}
          />
        );
      case 3:
        return <Success />;
    }
  }
}

export default UserForm;
