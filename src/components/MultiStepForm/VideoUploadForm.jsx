import React, {Component} from 'react';
import { makeStyles } from '@material-ui/core/styles';
// import Paper from '@material-ui/core/Paper';
import Dropzone from 'react-dropzone';

// import {useDropzone} from 'react-dropzone'
import RootRef from '@material-ui/core/RootRef'

class VideoUploadForm extends Component {
  constructor(props) {
    super(props)
  
    this.state = {
      files: null
    }
  }

  fileList() {
    if(this.state.files) {
      const fileList = this.state.files.map(file => (
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

  onDrop = (acceptedFiles) => {
    // console.log(acceptedFiles);
    this.setState({
      files: acceptedFiles
    });
    this.props.uploadVideo(acceptedFiles);
  }

  render() {
    return (
      <div className="text-center mt-5">
        <Dropzone onDrop={this.onDrop}>
          {({getRootProps, getInputProps}) => (
            <div {...getRootProps()}>
              <input {...getInputProps()} />
              Click me to upload a file!
              {this.fileList()}
            </div>
          )}
        </Dropzone>
      </div>
    );
  }
}

export default VideoUploadForm;