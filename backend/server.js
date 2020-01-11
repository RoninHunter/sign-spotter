var express = require('express');
var cors = require('cors');
var bodyParser = require('body-parser');

require('dotenv').config();

const port = process.env.PORT || 8081;

var app = express();
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({
  extended: true
}));

app.use(cors());

app.get('/', async (req, res) => {
  res.send('Server online!');
});

app.listen(port, () => {
  console.log('Application started on port: ', port);
});