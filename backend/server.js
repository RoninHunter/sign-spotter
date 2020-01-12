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
  try {
    let date = new Date();
    let videos = req.files.videos;
    console.log(req.body.email);
    console.log(date.getTime());
    videos.forEach(saveVideos);
    function saveVideos(item, index) {
      item.mv('./uploads/' + date.getTime() + '_' + item.name + '.mp4', function(err) {
        if (err) {
          console.log(err);
        }
      });
    }
    res.json({'upload': 'success'});
  }
  catch (e) {
    console.log(e);
    res.json({'upload': 'fail'});
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