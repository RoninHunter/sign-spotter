import React, { Component } from 'react';

import MuiThemeProvider from '@material-ui/core/styles/MuiThemeProvider';

import MainComp from './components/MainComp';

import NavBar from './components/NavBar';

import UserForm from './components/MultiStepForm/UserForm';
//import { HomePage } from './components/HomePage';
import About from './components/About';

import Image from 'react-bootstrap/Image'

import {
  BrowserRouter as Router,
  Switch,
  Route,
  Redirect,
  Link
} from "react-router-dom";


//import {useDropzone} from 'react-dropzone';
import './App.css';

class App extends Component {
  
  render() {
    return (
      <div className="App">

        <NavBar/>

        <Router>
        
          <div>


            <Switch>

              <Route path="/about">
                <About />
              </Route>

              <Route path="/userForm">
                <UserForm />
              </Route>

              <Route path="/">
                {/* <HomePage /> */}
              </Route>

              <Redirect to = "/" />

            </Switch>

          </div>
        </Router>

              
         <img src="./M8jWnf1.jpg" 
          class="rounded mx-auto d-block" alt="Responsive image">
        </img> 


      </div>

    );
  }
}

export default App;


// function Home() {
//   return <h2>Home</h2>;
// }


// function Aboutmenu() {
//   return <h2>About</h2>;
// }

// function VideoUpload() {
//   return <h2>Video Upload</h2>;
// }