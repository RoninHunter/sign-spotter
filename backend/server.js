var express = require('express');
var cors = require('cors');
var bodyParser = require('body-parser');
var fileUpload = require('express-fileupload');
var fs = require('fs');

require('dotenv').config();

const port = process.env.PORT || 8081;

var app = express();

app.use(fileUpload());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({
  extended: true
}));
app.use(cors());

// Creates uploads directory; needed for uploading video to backend
if (!fs.existsSync('./uploads/')) {
  fs.mkdirSync('./uploads')
}

app.get('/', async (req, res) => {
  res.send('Server online!');
});

app.post('/api/videoupload', function (req, res) {
  try {
    let date = new Date();
    let currentTime = date.getTime();
    let videos = []

    // Allows for 1 ore multiple videos to be processed, output is an array of videos
    if (Array.isArray(req.files.videos)) {
      videos = req.files.videos;
    } else {
      videos.push(req.files.videos);
    }

    // Iterates though each video and saves to uploads folder as well as calls the python script
    videos.forEach(saveVideos);
    function saveVideos(item, index) {
      let newPath = './uploads/' + currentTime + '_' + item.name + '.mp4';
      item.mv(newPath, function(err) {
        if (err) {
          console.log(err);
          response.push('Error saving file');
        }
      });
      // Spawns a child process to run python script
      const spawn = require('child_process').spawn;
      const pythonProcess = spawn('python', ['../cnn/labeler.py', item.name, req.body.email, currentTime.toString()]);
      pythonProcess.stdout.on('data', function(data) {
        console.log(data.toString());
      });
    }
    res.json({
      'upload': 'success',
    });
  }
  catch (e) {
    console.log(e);
    res.statusCode(400).json({
      'upload': 'fail',
    });
  }
});

app.post('/api/history', function (req, res) {
  try {
    // Example response, needs to be replaced with actual connection to DB
    var test_response = {
      'history': [
        {
          'video': 'url',
          'name': 'video_1.mp4',
          'labelsURL': 'url'
        },
        {
          'video': 'url',
          'name': 'video_2.mp4',
          'labelsURL': 'url'
        }
      ]
    }
    res.json(test_response);
  }
  catch (e) {
    console.log(e);
    res.json({'history': null});
  }
});

app.post('/api/locations', function (req, res) {
  try {
    // Example response, needs to be replaced with actual connection to DB
    var test_response = {
      'locations': [
        {
          'latitude': 27.999634,
          'longitude': -81.957009,
          'signType': 'signType',
          'image': 'imageURL'
        },
        {
          'latitude': 27.996470,
          'longitude': -81.957159,
          'signType': 'signType',
          'image': 'imageURL'
        }
      ]
    }
    res.json(test_response);
  }
  catch (e) {
    console.log(e);
    res.json({'locations': null});
  }
});

app.listen(port, () => {
  console.log('Application started on port: ', port);
});