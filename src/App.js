
import React, { Component } from 'react';

import BackgroundComp from './components/MainComp';

import Container from 'react-bootstrap/Container'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'

import Image from 'react-bootstrap/Image'


//import {useDropzone} from 'react-dropzone';
import './App.css';

class App extends Component {
  
  render() {
    return (

        <div 
        className = "App">

          <Container>
          
            <Row>
              <Col xs={6} md={4}>
                <Image src="./M8jWnf1.jpg" fluid />
                <BackgroundComp />
              </Col>
            </Row>

          </Container>

          

        </div>
    );
  }
}
export default App;

/*
import React from "react";
import { BrowserRouter as Router } from "react-router-dom";
import {
  Navbar,
  NavbarBrand,
  NavbarNav,
  NavItem,
  NavLink,
  NavbarToggler,
  Collapse,
  Mask,
  Row,
  Col,
  Btn,
  View,
  Container,
  FormInline,
  Animation
} from "react-bootstrap";
import "./index.css";

class App extends React.Component {
  state = {
    collapsed: false
  };

  handleTogglerClick = () => {
    this.setState({
      collapsed: !this.state.collapsed
    });
  };

  render() {
    const overlay = (
      <div
        id="sidenav-overlay"
        style={{ backgroundColor: "transparent" }}
        onClick={this.handleTogglerClick}
      />
    );
    return (
      <div id="apppage">
        <Router>
          <div>
            <Navbar
              color="primary-color"
              dark
              expand="md"
              fixed="top"
              scrolling
              transparent
            >
              <Container>
                <NavbarBrand>
                  <strong className="white-text">MDB</strong>
                </NavbarBrand>
                <NavbarToggler onClick={this.handleTogglerClick} />
                <Collapse isOpen={this.state.collapsed} navbar>
                  <NavbarNav left>
                    <NavItem active>
                      <NavLink to="#!">Home</NavLink>
                    </NavItem>
                    <NavItem>
                      <NavLink to="#!">Link</NavLink>
                    </NavItem>
                    <NavItem>
                      <NavLink to="#!">Profile</NavLink>
                    </NavItem>
                  </NavbarNav>
                  <NavbarNav right>
                    <NavItem>
                      <FormInline waves>
                        <div className="md-form my-0">
                          <input
                            className="form-control mr-sm-2"
                            type="text"
                            placeholder="Search"
                            aria-label="Search"
                          />
                        </div>
                      </FormInline>
                    </NavItem>
                  </NavbarNav>
                </Collapse>
              </Container>
            </Navbar>
            {this.state.collapsed && overlay}
          </div>
        </Router>
        <View>
          <Mask className="d-flex justify-content-center align-items-center gradient">
            <Container>
              <Row>
                <Col
                  md="6"
                  className="white-text text-center text-md-left mt-xl-5 mb-5"
                >
                  <Animation type="fadeInLeft" delay=".3s">
                    <h1 className="h1-responsive font-weight-bold mt-sm-5">
                      Make purchases with our app
                    </h1>
                    <hr className="hr-light" />
                    <h6 className="mb-4">
                      Lorem ipsum dolor sit amet, consectetur adipisicing elit.
                      Rem repellendus quasi fuga nesciunt dolorum nulla magnam
                      veniam sapiente, fugiat! Commodi sequi non animi ea dolor
                      molestiae iste.
                    </h6>
                    <Btn color="white">Download</Btn>
                    <Btn outline color="white">
                      Learn More
                    </Btn>
                  </Animation>
                </Col>

                <Col md="6" xl="5" className="mt-xl-5">
                  <Animation type="fadeInRight" delay=".3s">
                    <img
                      src="https://mdbootstrap.com/img/Mockups/Transparent/Small/admin-new.png"
                      alt=""
                      className="img-fluid"
                    />
                  </Animation>
                </Col>
              </Row>
            </Container>
          </Mask>
        </View>

        <Container>
          <Row className="py-5">
            <Col md="12" className="text-center">
              <p>
                Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
                eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut
                enim ad minim veniam, quis nostrud exercitation ullamco laboris
                nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor
                in reprehenderit in voluptate velit esse cillum dolore eu fugiat
                nulla pariatur. Excepteur sint occaecat cupidatat non proident,
                sunt in culpa qui officia deserunt mollit anim id est laborum.
              </p>
            </Col>
          </Row>
        </Container>
      </div>
    );
  }
}

export default App;

*/