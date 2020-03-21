import sys
import labeler_scripts as scripts
import os
import datetime
import ffmpeg
import os
from pathlib import Path

def main():
  # arguements = sys.argv
  # video_filename = arguements[1]
  # email = arguements[2]
  # upload_time = arguements[3]

  jpeg_dir = os.path.join(os.path.dirname(__file__),'jpegs')
  fps = 10
  
  # Temporary
  video_filename = '/home/egm42/sign-spotter/backend/uploads/REC_2019_04_12_10_04_29_F_Trim1_Trim.mp4'
  email = 'test@email.com'
  upload_time = datetime.datetime.now()
  

  gps_list = scripts.gps_list(video_filename, fps)

  # Creates a class for the DB data will be saved to
  db = scripts.DB('labels')
  labels = []

  if(gps_list):
    # The last parameter is fps for processing video in to jpegs
    frame_count = scripts.split_video(video_filename, jpeg_dir, fps)['frame_count']
    
    # Frames start at 1, hence the range(1, frame_count + 1)
    for frame_num in range(1, frame_count + 1):

      left_img = os.path.join(jpeg_dir, Path(video_filename).stem + '_' + str(frame_num) + '_image_l.jpg')
      right_img = os.path.join(jpeg_dir, Path(video_filename).stem + '_' + str(frame_num) + '_image_r.jpg')

      left_labels = scripts.label(left_img)
      right_labels = scripts.label(right_img)
      
      left_labels = process_labels(left_labels, frame_num, video_filename, email, upload_time, left_img, gps_list, db, 'left')
      right_labels = process_labels(right_labels, frame_num, video_filename, email, upload_time, right_img, gps_list, db, 'right')

      labels = labels + left_labels + right_labels
  else:
    scripts.send_email('no_gps', email)

  # print(labels)
  # print(labels)
  db.save_to_mongo(labels)

  #TODO: Delete images from jpeg_list

def process_labels(labels, frame_num, video_filename, email, upload_time, image_path, gps_list, db, side):
  if(labels):
    for label in labels:
      label['frame'] = frame_num
      label['original_video_filename'] = video_filename
      label['latitude'] = gps_list[frame_num]['latitude']
      label['longitude'] = gps_list[frame_num]['longitude']
      label['bearing'] = gps_list[frame_num]['bearing']
      label['user_email'] = email
      label['upload_time'] = upload_time
      label['side'] = side
      label['image_path'] = image_path

      return labels
  else:
    label = {}
    label['frame'] = frame_num
    label['original_video_filename'] = video_filename
    label['latitude'] = gps_list[frame_num]['latitude']
    label['longitude'] = gps_list[frame_num]['longitude']
    label['bearing'] = gps_list[frame_num]['bearing']
    label['user_email'] = email
    label['upload_time'] = upload_time
    label['side'] = side
    label['image_path'] = image_path

    return [label]

if __name__ == '__main__':
  main()