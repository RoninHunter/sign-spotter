import ffmpeg
import os
from pathlib import Path

def split_video(filename, output_dir, fps):
    file = Path(filename).stem

    frame_count = frames(filename, fps)

    image = ffmpeg.input(filename)
    image = ffmpeg.filter(image, 'fps', fps=fps)

    image_left = ffmpeg.filter(image, 'crop', 'iw*.3', 'ih', '0', '0')
    image_right = ffmpeg.filter(image, 'crop', 'iw*.3', 'ih', 'iw*.7', '0')

    image_left = ffmpeg.output(image_left, os.path.join(output_dir, file + '_%d_image_l.jpg'))
    image_right = ffmpeg.output(image_right, os.path.join(output_dir, file + '_%d_image_r.jpg'))

    result_left = ffmpeg.run(image_left)
    result_right = ffmpeg.run(image_right)

    return {'frame_count': frame_count}

def gps_list(filename, fps):
    frame_count = frames(filename, fps)

    placeholder = {}
    # TODO: extract gps info from video file and convert to json object
    for frame in range(1, frame_count+1):
        placeholder[frame] = {
            'latitude': 20 + frame/10,
            'longitude': 81 + frame/10,
            'bearing': 90 * frame,
            'datetime': 'datetime'
        }
    return placeholder

def frames(filename, fps):
    # print(ffmpeg.probe(filename))
    return round(float(ffmpeg.probe(filename)['streams'][0]['duration'])*fps)

if __name__ == '__main__':
    print('')

    # a = split_video('/home/egm42/sign-spotter/backend/uploads/1584227441905_REC_2019_11_14_04_10_49_F.mp4', '/home/egm42/sign-spotter/cnn/jpegs')

    # a = split_video('/home/egm42/sign-spotter/backend/uploads/REC_2019_04_12_10_04_29_F_Trim1_Trim.mp4', '/home/egm42/sign-spotter/cnn/jpegs', 10)

    # print(a)
    
    # print(frames('',10))