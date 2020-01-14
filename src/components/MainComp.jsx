import React, { Component } from 'react';
import NavBar from './NavBar';
import DescriptionComp from './DescriptionComp';
import {useDropzone} from 'react-dropzone';
//import './App.css';



class BackgroundComp extends Component {
  
  render() {
    return (
      <div 
      className = "BackgroundComp">

        <NavBar />
        <DescriptionComp /> 

      </div>
    );
  }
}
export default BackgroundComp;
