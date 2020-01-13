# sign-spotter

## Getting Started
Sign Spotter is designed as an asset managment application that allows users to identify missing traffic signs. It is able to accomplish this through the use of a convolutional neural network that identifies the signs from user uploaded videos.

![Labeled Sign Picture](https://raw.githubusercontent.com/RoninHunter/sign-spotter/master/public/Labeled_Pic.jpg "Labeled Sign Picture")

## Prerequisites
\*On Windows, Python and ffmpeg should be added to the Windows Path

    Python
    ffmpeg


## Installation/Deployment
Clone repository

Create .env file in the **backend** folder with the following variables

      PORT={port of choice}

Terminal 1

    cd sign-spotter
    npm install
    npm start

Terminal 2

    cd sign-spotter/backend
    npm install
    node server