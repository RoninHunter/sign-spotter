import React, { Component } from 'react';
import { Navbar, 
  Nav, 
  //NavDropdown, 
  //Form, 
  //FormControl, 
  //Button 
} from 'react-bootstrap';


class NavBar extends Component {
  render() {
    return (
      <div className = "navbar navbar-expand-lg navbar-light bg-light">

        <Navbar collapseOnSelect expand="lg" bg="dark" variant="dark">

          <Navbar.Brand href = "#home"> SignSPOTTER </Navbar.Brand>

          <Navbar.Toggle aria-controls = "responsive-navbar-nav" />

          <Navbar.Collapse id = "responsive-navbar-nav">
            <Nav className = "mr-auto">
              <Nav.Link href = "#uploadVideo"> Upload Video </Nav.Link>
              <Nav.Link href = "#status"> Status </Nav.Link>
              <Nav.Link href = "#about"> About </Nav.Link>
              <Nav.Link href = "#history"> History </Nav.Link>
            </Nav>
          </Navbar.Collapse>


        </Navbar>


      </div>
    );
  }
}
export default NavBar;
