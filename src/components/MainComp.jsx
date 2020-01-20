import React, { Component } from 'react';
import NavBar from './NavBar';
import VideoUploadForm from './VideoUploadForm';
import {useDropzone} from 'react-dropzone';
//import './App.css';



class MainComp extends Component {
  
  render() {
    return (
      <div 
      className = "BackgroundComp">
        {/* <NavBar /> */}
        {/* <videoUploadForm /> */}
      </div>
    );
  }
}
export default MainComp;
