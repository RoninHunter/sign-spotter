var express = require('express');
var cors = require('cors');
var bodyParser = require('body-parser');
var fileUpload = require('express-fileupload');

require('dotenv').config();

const port = process.env.PORT || 8081;

var app = express();

app.use(fileUpload());

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({
  extended: true
}));

app.use(cors());

app.get('/', async (req, res) => {
  res.send('Server online!');
});

app.post('/api/videoupload', function (req, res) {
  var response = [];
  try {
    let date = new Date();
    let currentTime = date.getTime();
    let videos = []
    videos.push(req.files.videos)
    console.log(videos);
    videos.forEach(saveVideos);
    function saveVideos(item, index) {
      let newPath = './uploads/' + currentTime + '_' + item.name + '.mp4';
      item.mv(newPath, function(err) {
        if (err) {
          console.log(err);
          response.push('Error saving file');
        }
      });
      const spawn = require('child_process').spawn;
      const pythonProcess = spawn('python', ['../cnn/labeler.py', item.name, req.body.email, currentTime]);
      pythonProcess.stdout.on('data', function(data) {
        response.push(data.toString());
        res.json({
          'upload': 'success',
          'response': response
        })
      });
    }
  }
  catch (e) {
    console.log(e);
    res.json({
      'upload': 'fail',
      'response': response
    });
  }
});

app.post('/api/history', function (req, res) {
  try {
    var test_response = {
      'history': [
        {
          'url': 'url',
          'name': 'name',
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