import React, { Component } from 'react';
import { Navbar, 
  Nav,
  NavLink, 
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

          <Navbar.Brand href = "home"> SignSPOTTER </Navbar.Brand>

          <Navbar.Toggle aria-controls = "responsive-navbar-nav" />

          <Navbar.Collapse id = "responsive-navbar-nav">
            <Nav className = "mr-auto">
              <Nav.Link href = "userForm"> Upload Video </Nav.Link>
              <Nav.Link href = "about"> About </Nav.Link>
            </Nav>
          </Navbar.Collapse>

        </Navbar>

      </div>
    );
  }
}
export default NavBar;
