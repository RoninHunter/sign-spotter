import React, { Component } from 'react';
import NavBar from './components/NavBar';
import './App.css';


class App extends Component {
  render() {
    return (


      <div 
      
      // style = {{backgroundColor: '#2a2a2a',
        //        width: '1920px',
          //      height: '1080px'}}
      
      className="App">


        <NavBar />

        {/* <h1>Hello World!</h1> */}

        <p> Sign Spotter is designed as an asset managment application that allows users to identify missing traffic signs. 
          It is able to accomplish this through the use of a convolutional neural network that identifies the signs from user uploaded videos.</p>

      </div>
    );
  }
}
export default App;
