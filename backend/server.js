var express = require('express');
var cors = require('cors');
var bodyParser = require('body-parser');
var fileUpload = require('express-fileupload');
var mongoose = require('mongoose');
var Signs = require('./models/signs');

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

mongoose.connect(process.env.MLAB_URI, {
  useUnifiedTopology: true,
  useCreateIndex: true,
  useFindAndModify: false,
  useNewUrlParser: true
});
mongoose.connection.on('error', console.error.bind(console, 'connection error: '));

app.get('/', async (req, res) => {
  res.send('Server online!');
});

app.post('/api/videoupload', function (req, res) {
  // console.log(req.files);
  // console.log(req.body);
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
      let newPath = './uploads/' + currentTime.toString() + '_' + item.name;
      item.mv(newPath, function(err) {
      });
      // Spawns a child process to run python script
      // const spawn = require('child_process').spawn;
      // const pythonProcess = spawn('python', ['../cnn/labeler.py', item.name, req.body.email, currentTime.toString()]);
      // pythonProcess.stdout.on('data', function(data) {
      //   console.log(data.toString());
      // });
      let filename = './pending/' + currentTime.toString() + '_' + item.name + '.json';
      let info = {
        filename: currentTime + '_' + item.name,
        originalFilename: item.name,
        email: req.body.email,
        firstName: req.body.firstName,
        lastName: req.body.lastName,
        uploadTime: currentTime.toString(),
        processed: false
      };
      infoString = JSON.stringify(info);
      fs.writeFile(filename, infoString, function(err) {
        if (err) {
          console.log(err);
          response.push('Error saving file');
        }
      });
    }
    res.json({
      'upload': 'success',
    });
  }
  catch (e) {
    console.log(e);
    res.json({
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

app.get('/api/locations/current', function (req, res) {
  console.log('testing');
  Signs.find({'missing': false}, function(err, signs) {
    console.log("Current:")
    console.log(signs);
    res.send(signs);
  });
});

app.get('/api/locations/missing', function (req, res) {
  console.log('testing');
  Signs.find({'missing': true}, function(err, signs) {
    console.log('Missing:')
    console.log(signs);
    res.send(signs);
  });
});

// app.post('/api/locations', function (req, res) {
//   try {
//     // Example response, needs to be replaced with actual connection to DB
//     var test_response = {
//       'locations': [
//         {
//           'latitude': 27.999634,
//           'longitude': -81.957009,
//           'signType': 'signType',
//           'image': 'imageURL'
//         },
//         {
//           'latitude': 27.996470,
//           'longitude': -81.957159,
//           'signType': 'signType',
//           'image': 'imageURL'
//         }
//       ]
//     }
//     res.json(test_response);
//   }
//   catch (e) {
//     console.log(e);
//     res.json({'locations': null});
//   }
// });

app.listen(port, () => {
  console.log('Application started on port: ', port);
});