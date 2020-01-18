import React, { Component } from 'react';

class About extends Component {
  render() {
    return (
      <div>
        <div style={{display: 'flex', justifyContent: 'center'}}>
          <h1>About</h1>
        </div>
        <div>
          <p>
            Various applications have shown the promise that Deep Neural Networks allot. This peeked our interest and led to the developement of this application which makes use of convolutional neural networks for classification of traffic signs.
          </p>
        </div>
        <div>
          <h4>Luis Ruiz</h4>
          <p>
            Pending update
          </p>
        </div>
        <br/>
        <div>
          <h4>Jeremy Green</h4>
          <p>
            Pending update
          </p>
        </div>
      </div>
    );
  }
}

export default About;