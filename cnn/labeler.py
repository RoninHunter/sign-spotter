import sys
import labeler_scripts as scripts
import os
import datetime
import ffmpeg
import os
from pathlib import Path
from bson.son import SON
from bson.objectid import ObjectId
import time
import json

def main():
  files = os.listdir(os.path.join(os.getcwd(), 'backend', 'pending'))
  time.sleep(len(files) * 3)
  if(files):
    print('Files to process:', files)
    for file in files:
      data = {}
      jsonpath = os.path.join(os.getcwd(), 'backend', 'pending', file)
      print('json read:', jsonpath)
      try:
        with open(jsonpath) as f:
          data = json.load(f)
        print(data)
        filename = os.path.join(os.getcwd(), 'backend', 'uploads', data['filename'])
        original_filename = data['originalFilename']
        email = data['email']
        first_name = data['firstName']
        last_name = data['lastName']
        upload_time = data['uploadTime']
        processed = data['processed']
        scripts.emailSender(email, first_name + '' + last_name,  0)
        
        if(not processed):
          print('processing video')
          data['processed'] = True
          with open(jsonpath, 'w') as f:
            json.dump(data, f)
          try:
            # replace with process function
            print(filename, email, upload_time, first_name, last_name)
            response = process(filename, email, upload_time, first_name, last_name)
            print('Success processing', original_filename)
            removefile(jsonpath)
            removefile(filename)
            time.sleep(3)
          except:
            pass
        else:
          print('Error processing file', original_filename)
          #email user
          errfilename = os.path.join(os.getcwd(), 'backend', 'uploads', os.path.basename(jsonpath).split('.json')[0])
          removefile(jsonpath)
          removefile(errfilename)
          time.sleep(1)
      except json.JSONDecodeError as e:
        print('Error processing file', jsonpath)
        errfilename = os.path.join(os.getcwd(), 'backend', 'uploads', os.path.basename(jsonpath).split('.json')[0])
        removefile(jsonpath)
        try:
          process(errfilename, 'email@email.com', time.time(), 'err', 'vid')
        except:
          pass
        removefile(errfilename)
        time.sleep(1)
      
  else:
    print('No videos to process')
    time.sleep(10)

def removefile(filepath):
  try:
    os.remove(filepath)
  except FileNotFoundError as e:
    print('File does not exist')

def process(filepath, email, upload_time, first_name, last_name):
  # arguements = sys.argv
  # video_filename = arguements[1]
  # email = arguements[2]
  # upload_time = arguements[3]
  # user = arguements[4]

  jpeg_dir = os.path.join(os.path.dirname(__file__),'jpegs')
  fps = 10

  startTime = time.time()
  endTime = time.time()
  print(endTime - startTime)

  labels = []
  sign_matrix = {'addedLane': {},'curveLeft': {}, 'curveRight': {}, 'dip': {}, 'doNotEnter': {}, 'keepRight': {}, 'laneEnds': {}, 'merge': {}, 'noLeftTurn': {}, 'noRightTurn': {}, 'pedestrianCrossing': {}, 'rightLaneMustTurn': {}, 'school': {}, 'schoolSpeedLimit25': {}, 'signalAhead': {}, 'slow': {}, 'speedLimit15': {}, 'speedLimit25': {}, 'speedLimit30': {}, 'speedLimit35': {}, 'speedLimit40': {}, 'speedLimit45': {}, 'speedLimit50': {}, 'speedLimit55': {}, 'speedLimit65': {}, 'stop': {}, 'stopAhead': {}, 'yield': {}}

  # Temporary
  video_filename = filepath
  email = email
  upload_time = upload_time
  try:
    gps_list = scripts.gps_list(video_filename, fps)
  except FileNotFoundError as e:
    scripts.emailSender(email, first_name + '' + last_name,  5)
  jpeg_list = []

  imageLabeler = scripts.tensorflowLabeler()

  if(gps_list):
    print('gps exists')
    # The last parameter is fps for processing video in to jpegs
    frame_count = scripts.split_video(video_filename, jpeg_dir, fps)
    frame_count = len(gps_list)
    
    # Frames start at 1, hence the range(1, frame_count + 1)
    for frame_num in range(1, frame_count + 1):
    # if(frame_num >=550 and frame_num <=558):
    # if(frame_num > 598):
      # left_img = os.path.join(jpeg_dir, Path(video_filename).stem + '_' + str(frame_num) + '_image_l.jpg')
      right_img = os.path.join(jpeg_dir, Path(video_filename).stem + '_' + str(frame_num) + '_image_r.jpg')
      # jpeg_list.append(left_img)
      # print(right_img)
      jpeg_list.append(right_img)
      # print(jpeg_list)

      # left_labels = imageLabeler.labelDarknet(left_img)
      right_labels = imageLabeler.labelDarknet(right_img, 'right')
      # right_labels = imageLabeler.labelTensor(right_img, 'right')

      # left_labels = process_labels(left_labels, frame_num, video_filename, email, upload_time, left_img, gps_list, 'left')
      right_labels = process_labels(right_labels, frame_num, video_filename, email, upload_time, right_img, gps_list, 'right')
      # labels += left_labels + right_labels
      labels += right_labels

      # for label in left_labels + right_labels:
      for label in right_labels:
        if 'class' in label.keys():
          if frame_num not in sign_matrix[label['class']].keys():
            sign_matrix[label['class']][frame_num] = {}
          sign_matrix[label['class']][frame_num][label['side']] = True
  
  signs_found = False

  print('Processing labels')
  for side in ['right']:
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
            if(blanks >= 2 and sightings >= 3):
              save_label(last_sighting, labels, side)
              signs_found = True
              sightings = 0
              last_sighting = 0
        else:
          blanks += 1
          # TODO: tweak amount of blank frames and sightings needed to trigger saving of sign
          if(blanks >= 2 and sightings >= 3):
            save_label(last_sighting, labels, side)
            signs_found = True
            sightings = 0
            last_sighting = 0
      # TODO: tweak amount of blank frames and sightings needed to trigger saving of sign
      if(sightings >= 3 and last_sighting != 0):
        save_label(last_sighting, labels, side)
        signs_found = True

  if(signs_found):
    scripts.emailSender(email, first_name + '' + last_name,  1)
  else:
    scripts.emailSender(email, first_name + '' + last_name,  2)
  # for label in labels:
  #   print('---------------------------------------------------------------')
  #   print(label)
  # print(sign_matrix)
  # db.save_to_mongo(labels)

  # Delete images from jpegs folder after processing and uploading to DB
  for image in jpeg_list:
    removefile(image)

  # iterate through all gps points and check if signs have been updated
  print('Processing GPS list')

  signs_db = scripts.DB('signs')
  year = int(gps_list[1]['year'])
  month = int(gps_list[1]['month'])
  day = int(gps_list[1]['day'])
  hour = int(gps_list[1]['hour'])
  minute = int(gps_list[1]['minute'])
  second = int(float(gps_list[1]['second']))
  microsecond = int(round((second % 1) * 1000000,0))
  if(microsecond == 1):
    second += 1
    microsecond = 0
  new_sightings = datetime.datetime(year, month, day, hour, minute, second, microsecond) - datetime.timedelta(minutes=1)

  for frame in range(1, frame_count + 1):
    latitude = float(gps_list[frame]['latitude'])
    longitude = float(gps_list[frame]['longitude'])
    azimuth = int(float(gps_list[frame]['azimuth']))

    # Query looks for closest sign within the maxDistance that has a similar azimuth
    query = {'location': SON([('$near', [latitude, longitude]), ('$maxDistance', 0.0003)]), 'azimuth': {'$gte': (azimuth - 15) % 360, '$lte': (azimuth + 15) % 360}}
    existing_signs = signs_db.get_data(query)
  
    if(existing_signs.count() != 0):
      existing_id = existing_signs[0]['_id']

      # TODO: build logic checking datetime
      if(existing_signs[0]['last_sighting'] < new_sightings):
        update = {
          'missing': True
        }

        signs_db.update_data(existing_id, update)

  endTime = time.time()
  print(endTime - startTime)

def save_label(last_sighting, labels, side):
  print('Saving label')
  signs_db = scripts.DB('signs')
  # print(last_sighting)
  # print(len(labels))
  # if(side == 'left'):
  #   label = [labels[last_sighting * 2 - 2]]
  # else:
  #   label = [labels[last_sighting * 2 - 1]]

  # label = labels[last_sighting - 598]
  label = labels[last_sighting]
  # print(label)
  sign_class = label['class']
  latitude = float(label['location'][0])
  longitude = float(label['location'][1])
  azimuth = int(float(label['azimuth']))
  last_sighting = label['last_sighting']

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
    print('Updating Mongo')
    signs_db.update_data(existing_id, update)
    
  else:
    print('Saveing to Mongo')
    signs_db.save_to_mongo([label])
  print('End of save label')

def process_labels(labels, frame_num, video_filename, email, upload_time, image_path, gps_list, side):
  print('Processing label')
  if(labels):
    for label in labels:
      label['frame'] = frame_num
      label['original_video_filename'] = video_filename
      label['location'] = [float(gps_list[frame_num]['latitude']), float(gps_list[frame_num]['longitude'])]
      year = int(gps_list[frame_num]['year'])
      month = int(gps_list[frame_num]['month'])
      day = int(gps_list[frame_num]['day'])
      hour = int(gps_list[frame_num]['hour'])
      minute = int(gps_list[frame_num]['minute'])
      second = int(float(gps_list[frame_num]['second']))
      microsecond = int(round((second % 1) * 1000000,0))
      if(microsecond == 1):
        second += 1
        microsecond = 0
      datetimestamp = datetime.datetime(year, month, day, hour, minute, second, microsecond)
      label['last_sighting'] = datetimestamp
      label['azimuth'] = float(gps_list[frame_num]['azimuth']) % 360
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
    year = int(gps_list[frame_num]['year'])
    month = int(gps_list[frame_num]['month'])
    day = int(gps_list[frame_num]['day'])
    hour = int(gps_list[frame_num]['hour'])
    minute = int(gps_list[frame_num]['minute'])
    second = int(float(gps_list[frame_num]['second']))
    microsecond = int(round((second % 1) * 1000000,0))
    if(microsecond == 1):
      second += 1
      microsecond = 0
    datetimestamp = datetime.datetime(year, month, day, hour, minute, second, microsecond)
    label['last_sighting'] = datetimestamp
    label['azimuth'] = float(gps_list[frame_num]['azimuth']) % 360
    label['user_email'] = email
    label['upload_time'] = upload_time
    label['side'] = side
    label['image_path'] = image_path
    label['missing'] = False
    label['sightings'] = 1

    return [label]

if __name__ == '__main__':
  while(True):
    main()
