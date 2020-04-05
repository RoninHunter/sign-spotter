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
  last_sighting: String,
  image_path: String,
  missing: Boolean
});

var Signs = mongoose.model('Signs', signsSchema);

module.exports = Signs;