import sys
import labeler_scripts as scripts
import os
import datetime
import ffmpeg
import os
from pathlib import Path
from bson.son import SON
from bson.objectid import ObjectId

def main():
  # arguements = sys.argv
  # video_filename = arguements[1]
  # email = arguements[2]
  # upload_time = arguements[3]

  jpeg_dir = os.path.join(os.path.dirname(__file__),'jpegs')
  fps = 10

  labels = []
  sign_matrix = {'addedLane': {},'curveLeft': {}, 'curveRight': {}, 'dip': {}, 'doNotEnter': {}, 'keepRight': {}, 'laneEnds': {}, 'merge': {}, 'noLeftTurn': {}, 'noRightTurn': {}, 'pedestrianCrossing': {}, 'rightLaneMustTurn': {}, 'school': {}, 'schoolSpeedLimit25': {}, 'signalAhead': {}, 'slow': {}, 'speedLimit15': {}, 'speedLimit25': {}, 'speedLimit30': {}, 'speedLimit35': {}, 'speedLimit40': {}, 'speedLimit45': {}, 'speedLimit50': {}, 'speedLimit55': {}, 'speedLimit65': {}, 'stop': {}, 'stopAhead': {}, 'yield': {}}

  # Temporary
  video_filename = '/home/egm42/sign-spotter/backend/uploads/REC_2020_04_04_08_40_13_F_Trim.mp4'
  email = 'test@email.com'
  upload_time = datetime.datetime.now()

  gps_list = scripts.gps_list(video_filename, fps)
  jpeg_list = []

  if(gps_list):
    # The last parameter is fps for processing video in to jpegs
    frame_count = scripts.split_video(video_filename, jpeg_dir, fps)['frame_count']
    
    # Frames start at 1, hence the range(1, frame_count + 1)
    for frame_num in range(1, frame_count + 1):

      left_img = os.path.join(jpeg_dir, Path(video_filename).stem + '_' + str(frame_num) + '_image_l.jpg')
      right_img = os.path.join(jpeg_dir, Path(video_filename).stem + '_' + str(frame_num) + '_image_r.jpg')
      jpeg_list.append(left_img)
      jpeg_list.append(right_img)

      left_labels = scripts.label(left_img)
      right_labels = scripts.label(right_img)
      
      left_labels = process_labels(left_labels, frame_num, video_filename, email, upload_time, left_img, gps_list, 'left')
      right_labels = process_labels(right_labels, frame_num, video_filename, email, upload_time, right_img, gps_list, 'right')
      labels += left_labels + right_labels

      for label in left_labels + right_labels:
        if 'class' in label.keys():
          if frame_num not in sign_matrix[label['class']].keys():
            sign_matrix[label['class']][frame_num] = {}
          sign_matrix[label['class']][frame_num][label['side']] = True
      
  else:
    scripts.send_email('no_gps', email)

  for side in ['left', 'right']:
    for sign in sign_matrix.keys():
      sightings = 0
      blanks = 0
      last_sighting = 0
      for frame_num in range(1, frame_count + 1):
        if frame_num in sign_matrix[sign].keys():
          if side in sign_matrix[sign][frame_num].keys():
            sightings += 1
            last_sighting = frame_num
          else:
            blanks += 1
            # TODO: tweak amount of blank frames and sightings needed to trigger saving of sign
            if(blanks >= 2 and sightings >= 1):
              save_label(last_sighting, labels, side)
              sightings = 0
              last_sighting = 0
        else:
          blanks += 1
          # TODO: tweak amount of blank frames and sightings needed to trigger saving of sign
          if(blanks >= 2 and sightings >= 1):
            save_label(last_sighting, labels, side)
            sightings = 0
            last_sighting = 0
      # TODO: tweak amount of blank frames and sightings needed to trigger saving of sign
      if(sightings >= 1 and last_sighting != 0):
        save_label(last_sighting, labels, side)

  # for label in labels:
  #   print('---------------------------------------------------------------')
  #   print(label)
  # print(sign_matrix)
  # db.save_to_mongo(labels)

  # Delete images from jpegs folder after processing and uploading to DB
  for image in jpeg_list:
    os.remove(image)

  # iterate through all gps points and check if signs have been updated
  signs_db = scripts.DB('signs')
  new_sightings = gps_list[1]['datetime']

  for frame in range(1, frame_count + 1):
    latitude = gps_list[frame]['latitude']
    longitude = gps_list[frame]['longitude']
    azimuth = gps_list[frame]['azimuth']

    # Query looks for closest sign within the maxDistance that has a similar azimuth
    query = {'location': SON([('$near', [latitude, longitude]), ('$maxDistance', 0.0003)]), 'azimuth': {'$gte': (azimuth - 10) % 360, '$lte': (azimuth + 10) % 360}}
    existing_signs = signs_db.get_data(query)
  
    if(existing_signs.count() != 0):
      existing_id = existing_signs[0]['_id']

      # TODO: build logic checking datetime
      if(existing_signs[0]['last_sighting'] < new_sightings):
        update = {
          'missing': True
        }

        signs_db.update_data(existing_id, update)

  # Delete video after processing
  # os.remove(video_filename)

def save_label(last_sighting, labels, side):
  signs_db = scripts.DB('signs')

  if(side == 'left'):
    label = [labels[last_sighting * 2 - 2]]
  else:
    label = [labels[last_sighting * 2 - 1]]

  sign_class = label[0]['class']
  latitude = label[0]['location'][0]
  longitude = label[0]['location'][1]
  azimuth = label[0]['azimuth']
  last_sighting = label[0]['last_sighting']

  query = {'class': sign_class, 'location': SON([('$near', [latitude, longitude]), ('$maxDistance', 0.0003)]), 'azimuth': {'$gte': (azimuth - 15) % 360, '$lte': (azimuth + 15) % 360}}
  existing_signs = signs_db.get_data(query)
  
  if(existing_signs.count() != 0):
    existing_id = existing_signs[0]['_id']
    prev_lat = existing_signs[0]['location'][0]
    prev_long = existing_signs[0]['location'][1]
    prev_bear = existing_signs[0]['azimuth']
    prev_sight = existing_signs[0]['sightings']

    update = {
      'location': [(prev_lat * prev_sight + latitude)/(prev_sight + 1), (prev_long * prev_sight + longitude)/(prev_sight + 1)],
      'azimuth': (prev_bear * prev_sight + azimuth)/(prev_sight + 1),
      'sightings': prev_sight + 1,
      'last_sighting': last_sighting
    }

    signs_db.update_data(existing_id, update)
    
  else:
    signs_db.save_to_mongo(label)

def process_labels(labels, frame_num, video_filename, email, upload_time, image_path, gps_list, side):
  if(labels):
    for label in labels:
      label['frame'] = frame_num
      label['original_video_filename'] = video_filename
      label['location'] = [gps_list[frame_num]['latitude'], gps_list[frame_num]['longitude']]
      year = gps_list[frame_num]['year']
      month = gps_list[frame_num]['month']
      day = gps_list[frame_num]['day']
      hour = gps_list[frame_num]['hour']
      minute = gps_list[frame_num]['minute']
      second = gps_list[frame_num]['second']
      datetimestamp = datetime.datetime(year, month, day, hour, minute, second)
      label['last_sighting'] = datetimestamp
      # label['last_sighting'] = gps_list[frame_num]['datetime']
      label['azimuth'] = gps_list[frame_num]['azimuth']
      label['user_email'] = email
      label['upload_time'] = upload_time
      label['side'] = side
      label['image_path'] = image_path
      label['missing'] = False
      label['sightings'] = 1

      return labels
  else:
    label = {}
    label['frame'] = frame_num
    label['original_video_filename'] = video_filename
    label['location'] = [gps_list[frame_num]['latitude'], gps_list[frame_num]['longitude']]
    year = gps_list[frame_num]['year']
    month = gps_list[frame_num]['month']
    day = gps_list[frame_num]['day']
    hour = gps_list[frame_num]['hour']
    minute = gps_list[frame_num]['minute']
    second = gps_list[frame_num]['second']
    datetimestamp = datetime.datetime(year, month, day, hour, minute, second)
    label['last_sighting'] = datetimestamp
    label['last_sighting'] = gps_list[frame_num]['datetime']
    label['azimuth'] = gps_list[frame_num]['azimuth']
    label['user_email'] = email
    label['upload_time'] = upload_time
    label['side'] = side
    label['image_path'] = image_path
    label['missing'] = False
    label['sightings'] = 1

    return [label]

if __name__ == '__main__':
  main()
 