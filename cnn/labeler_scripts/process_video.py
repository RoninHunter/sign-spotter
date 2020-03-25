import ffmpeg
#from ffprobe import FFProbe
import os
from pathlib import Path

import json
from collections import Counter
import numpy as np


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



def lineFrameCount(lineStr,lineSubStr):
    total = Counter([lineStr[i: i+len(lineSubStr)] for i in range(len(lineStr))])
    return total[lineSubStr]

def latConverter(lat):
    headDigits = 0
    value = 0
    headDigits = lat[0:2]
    value = lat[2:] 
    return (float(value)/60) + float(headDigits)

def longConverter(lat):
    headDigits = 0
    value = 0
    headDigits = lat[0:3]
    value = lat[3:] 
    return (float(value)/60) + float(headDigits)



# GPS class for bundling gps frame data
class json_GPSobj:

# ['GPRMC', '121147.00', 'A', '2757.17350',  'N', '08156.42096',  'W', '40.754',     '89.68', '14      11   19']
# ['GPRMC',   hhmmss.ss,   A,    [lati.tu],  N-S,     [long.it],  E-W,    knots,  TrueCourse,  day, month, year]

    def __init__(self, currentFrameIndex, seconds, latitude, longitude, velocity, azimuth, day, month, year):

        self.frameDict = {
                'seconds': '',
                'latitude': '',
                'longitude': '',
                #'velocity': '',
                'azimuth': '',
                'day': '',
                'month': '',
                'year': ''
            }

        self.frameDict['seconds']   = seconds

        self.frameDict['latitude']  = latitude
        self.frameDict['longitude'] = longitude

        # Speed over ground, Knots
        # self.frameDict['velocity']  = velocity

        # True Course a.k.a Azimuth
        self.frameDict['azimuth']  = azimuth

        # Date and Time block
        self.frameDict['day']       = day
        self.frameDict['month']     = month
        self.frameDict['year']      = year

    def currentFrameData(self):
        return self.frameDict
    

    def printFrameElement(self, currentFrameIndex, frameElement):
        return self.frameDict[frameElement]

    def deletKey(self, frameElement):
        del self.frameDict[frameElement]
    
    def printFrame(self):
        print(self.frameDict)
    

videoFrameDictionary = {}


def gps_list(filename, fps):

    line = []
    framePerLine = []
    current_Frame = 0
    framesNum = 0

    with open('/home/lil-as/sign-spotter/backend/uploads/sub.txt', 'r') as f:
        for line in f:
            current_Frame =  current_Frame + 1
            # print(line, end='')

            # Counting the number of gps frames
            framesNum = lineFrameCount(line, "gsensori")
            framePerLine.append(framesNum)
            
            #      0           1      2         3         4      5             6     7             8          9
            # ['GPRMC', '121147.00', 'A', '2757.17350',  'N', '08156.42096',  'W', '40.754',     '89.68', '14 11 19']
            # ['GPRMC',   hhmmss.ss,   A,    [lati.tu],  N-S,     [long.it],  E-W,    knots,  TrueCourse,  day,month,year]

            # Find index of the GPRMC and truncate all before this position in line
            # then pass remaining to gpsInfoSlice
            gpsInfoSlice = line[line.find("GPRMC"):len(line)-8] 

            if(gpsInfoSlice):
                print(gpsInfoSlice)
                # GPSplace.append(line.find("GPRMC"))

                lineList = gpsInfoSlice.split(",")
                print(' ')
                print(lineList)
                print(' ')


                latTemp = str(latConverter(lineList[3]))
                lineList[3] = latTemp[0:9] + ' ' + lineList[4]
                print(lineList[3])

                longTemp = str(longConverter(lineList[5]))
                lineList[5] = longTemp[0:9] + ' ' + lineList[6]
                print(lineList[5])


                dateStr = ''
                for dateData in lineList[9:10]:
                    dateStr = dateData
                day   = ''
                month = ''
                year  = ''

                day   = dateStr[0:2]
                month = dateStr[2:4]
                year  = dateStr[4:]


                #                                  1           3            5            7             8                      
                #                            frameIndex,     seconds,    latitude,   longitude,    velocity,      azimuth, day, month, year)
                jsonGPSlist = json_GPSobj(current_Frame, lineList[1], lineList[3], lineList[5], lineList[7],  lineList[8], day, month, year)

                
                videoFrameDictionary[current_Frame] = jsonGPSlist.currentFrameData()

                 
                # print(videoFrameDictionary)

    return videoFrameDictionary





def frames(filename, fps):
    filename = '/home/egm42/sign-spotter/backend/uploads/1584227441905_REC_2019_11_14_04_10_49_F.mp4'

    print(ffmpeg.probe(filename))
    return round(float(ffmpeg.probe(filename)['streams'][0]['duration'])*fps)

if __name__ == '__main__':

    # a = split_video('/home/egm42/sign-spotter/backend/uploads/1584227441905_REC_2019_11_14_04_10_49_F.mp4', '/home/egm42/sign-spotter/cnn/jpegs')

    # a = split_video('/home/egm42/sign-spotter/backend/uploads/REC_2019_04_12_10_04_29_F_Trim1_Trim.mp4', '/home/egm42/sign-spotter/cnn/jpegs', 10)

    # print(a)

   gps_list("/home/lil-as/sign-spotter/backend/uploads/REC_2019_11_14_04_10_49_F.MP4", 10)