import sys
import labeler_scripts as scripts
import os
import datetime

def main():
  jpeg_dir = os.path.join(os.path.dirname(__file__),'jpegs')

  # arguements = sys.argv
  # video_filename = arguements[1]
  # email = arguements[2]
  # upload_time = arguements[3]

  # Temporary
  video_filename = '/path/to/video'
  email = 'test@email.com'
  upload_time = datetime.datetime.now()

  gps_list = scripts.gps_list(video_filename)

  if(gps_list):
    jpeg_list = scripts.split_video(video_filename, jpeg_dir)

    
    for image in jpeg_list:
      labels = scripts.label(image['path'])
      if(labels):
        for label in labels:
          label['frame'] = image['frame']
          label['original_filename'] = video_filename
          label['latitude'] = gps_list[image['frame']]['latitude']
          label['longitude'] = gps_list[image['frame']]['longitude']
          label['bearing'] = gps_list[image['frame']]['bearing']
          label['user_email'] = email
          label['upload_time'] = upload_time
        scripts.save_to_mongo(labels)
      else:
        # TODO: image should still be saved to DB
        print('no labels')
  else:
    scripts.send_email('no_gps', email)

if __name__ == '__main__':
  main()