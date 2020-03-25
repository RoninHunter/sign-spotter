var mongoose = require('mongoose');
Schema = mongoose.Schema;

var signsSchema = new Schema({
  class: String,
  xmin: Number,
  ymax: Number,
  xmax: Number,
  ymin: Number,
  latitude: Number,
  longitude: Number,
  bearing: Number,
  side: String,
  last_sighting: Date,
  image_path: String
});

var Signs = mongoose.model('Signs', signsSchema);

module.exports = Signs;