import React, { Component } from 'react';

import NavBar from './components/NavBar';
import UserForm from './components/UserForm';
import Home from './components/HomePage';
import About from './components/About';

import {BrowserRouter, Switch, Route, Redirect} from "react-router-dom";

import './App.css';

class App extends Component {  
  render() {
    return (
      <div className="App">
        <div className="darkenBackground">
          <NavBar/>
          <div className="content">
            <BrowserRouter>
              <Switch>
                <Route path  = "/home"     component={Home} />
                <Route path  = "/about"    component={About} />
                <Route path  = "/userForm" component={UserForm}/>
                <Redirect to = "/home" />
              </Switch>
            </BrowserRouter>
          </div>
        </div>
      </div>
    );
  }
}

export default App;