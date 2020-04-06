import ffmpeg
#from ffprobe import FFProbe
import os
from pathlib import Path

import json
from collections import Counter

import numpy as np

import matplotlib.pyplot as plt
from scipy import interpolate


def split_video(filename, output_dir, fps):
    file = Path(filename).stem

    frame_count = frames(filename, fps)

    image = ffmpeg.input(filename)
    image = ffmpeg.filter(image, 'fps', fps = fps)

    image_left = ffmpeg.filter(image, 'crop', 'iw*.3', 'ih', '0', '0')
    image_right = ffmpeg.filter(image, 'crop', 'iw*.3', 'ih', 'iw*.7', '0')

    image_left  = ffmpeg.output(image_left,  os.path.join(output_dir, file + '_%d_image_l.jpg'))
    image_right = ffmpeg.output(image_right, os.path.join(output_dir, file + '_%d_image_r.jpg'))

    # result_left  = ffmpeg.run(image_left)
    # result_right = ffmpeg.run(image_right)

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


def interpolateGPSpoints(frameNum, lat_long, framesTotal):
    ret = []
    x = np.array(frameNum)
    y = np.array(lat_long)

    # Spline/Cubic interpolation
    f2_cubic = interpolate.interp1d(x,y, kind = 'cubic')

    for linX in range(1,framesTotal + 1):
        y_i = f2_cubic(linX)
        ret.append(y_i)  # interpolated value at this index

    return ret


# GPS class for bundling gps frame data
class json_GPSobj:

    # ['GPRMC', '121147.00', 'A', '2757.17350',  'N', '08156.42096',  'W', '40.754',     '89.68', '14      11   19']
    # ['GPRMC',   hhmmss.ss,   A,    [lati.tu],  N-S,     [long.it],  E-W,    knots,  TrueCourse,  day, month, year]

    def __init__(self, currentFrameIndex, seconds, latitude, longitude, velocity, azimuth, day, month, year, hour, minute, second):

        self.frameDict = {
                'oldeTime': '',
                'latitude': '',
                'longitude': '',
                'velocity': '',
                'azimuth': '',
                'day': '',
                'month': '',
                'year': '',
                'hour': '',
                'minute': '',
                'second': ''
            }

        self.frameDict['seconds']   = seconds

        self.frameDict['latitude']  = latitude
        self.frameDict['longitude'] = longitude

        # Speed over ground, Knots
        self.frameDict['velocity']  = velocity

        # True Course a.k.a Azimuth
        self.frameDict['azimuth']  = azimuth

        # Date block
        self.frameDict['day']       = day
        self.frameDict['month']     = month
        self.frameDict['year']      = year

         # Time block
        self.frameDict['hour']    = day
        self.frameDict['minute']  = month
        self.frameDict['second']  = year



    def currentFrameData(self):
        return self.frameDict
    

    def printFrameElement(self, currentFrameIndex, frameElement):
        return self.frameDict[frameElement]

    def getSeconds(self, currentFrameIndex, frameElement):
        return self.frameDict[frameElement]

    def deletKey(self, frameElement):
        del self.frameDict[frameElement]
    
    def printFrame(self):
        print(self.frameDict)
    

videoFrameDictionary = {}


def gps_list(filename, fps):

    os.system('ffmpeg -i ' + filename + ' -an -vn -bsf:s mov2textsub -scodec copy -f rawvideo ' + filename + '_sub.txt')

    # os.system('ffmpeg -i /home/User/sign-spotter/backend/uploads/REC_2019_11_14_04_10_49_F.MP4 -an -vn -bsf:s mov2textsub -scodec copy -f rawvideo sub.txt')


    line = []
    framePerLine = []
    current_Frame = 0
    emptyFrameTrigger = -1
    fullFrameTrigger = -1
    emptyFrameCount = 0
    framesNum = 0

    #Time acumulator 
    hour   = ''
    minute = ''
    second  = ''
    curHour = -1
    curMinute = -1
    curSecond = -1

    frameStamp = []
    timeForInterp = []
    longForInterp = []
    latForInterp = []
    speedForInterp = []
    azimuthForInterp = []

    frameInturpDict = {
            'oldeTime': '',
            'latitude': '',
            'longitude': '',
            'velocity': '',
            'azimuth': '',
            'day': '',
            'month': '',
            'year': '',
            'hour': '',
            'minute': '',
            'second': '',
        }

    

    with open(filename + '_sub.txt', 'r') as f:
    
        for line in f:

            # Counting the number of gps frames
            framesNum = lineFrameCount(line, "gsensori")

            framePerLine.append(framesNum)

            for cur_Frame in range(1, framesNum + 1):
                            
                if(curSecond >= 0):
                    if(-1 != curSecond  and  curSecond < 60):
                        curSecond = curSecond + 1.0/fps
                    elif(-1 != curMinute  and  curMinute):
                        # if(curMinute + 1 < 60.000000000000000):
                        curMinute = curMinute + 1
                    elif(-1 != curHour  and  curHour < 23):
                        curHour = curHour + 1
                    else:
                        curHour   = 0
                        curMinute = 0
                        curSecond = 0

                    frameInturpDict['hour']   = curHour
                    frameInturpDict['minute'] = curMinute
                    frameInturpDict['second'] = curSecond

                    # print(frameInturpDict['hour'], frameInturpDict['minute'], frameInturpDict['second'])

                else:
                    frameInturpDict['hour']   = -1
                    frameInturpDict['minute'] = -1
                    frameInturpDict['second'] = -1
                    
                    emptyFrameCount += 1

                videoFrameDictionary[current_Frame + cur_Frame] = frameInturpDict

                print((current_Frame + cur_Frame),videoFrameDictionary[current_Frame + cur_Frame]['hour'], 
                    videoFrameDictionary[current_Frame + cur_Frame]['minute'], 
                    videoFrameDictionary[current_Frame + cur_Frame]['second'])

            current_Frame = current_Frame + framesNum

            # Frist couple of frames ############################################################################
            if(emptyFrameTrigger == 1 and fullFrameTrigger == -1):

                firstHour   = curHour
                firstMinute = curMinute
                firstSecond = curSecond
            
                
                firstSecond = (firstSecond - emptyFrameCount/fps) - 1/fps

                for curEmptyFrame in range(1, emptyFrameCount + 1):

                    if(-1 != firstSecond  and  firstSecond < 60):
                        firstSecond = firstSecond + 1.0/fps
                    elif(-1 != firstMinute  and  firstMinute < 60):
                        firstMinute = firstMinute + 1
                    elif(-1 != firstHour  and  firstHour < 23):
                        firstHour = firstHour + 1
                    else:
                        firstSecond = 0
                        firstMinute = 0
                        firstHour   = 0

                    

                    videoFrameDictionary[curEmptyFrame]['hour']   = firstHour
                    videoFrameDictionary[curEmptyFrame]['minute'] = firstMinute
                    videoFrameDictionary[curEmptyFrame]['second'] = firstSecond

                    # print(videoFrameDictionary[curEmptyFrame]['hour'], 
                    #     videoFrameDictionary[curEmptyFrame]['minute'], 
                    #     videoFrameDictionary[curEmptyFrame]['second'])
                    
                fullFrameTrigger = 1


            #      0           1      2         3         4      5             6     7             8          9             10     11    12
            # ['GPRMC', '125647.00', 'A', '2757.17350',  'N', '08156.42096',  'W', '40.754',     '89.68', '14 11 19'        12     56    47 
            # ['GPRMC',   hhmmss.ss,   A,    [lati.tu],  N-S,     [long.it],  E-W,    knots,  TrueCourse,  day,month,year, hour,minute,second]

            # Find index of the GPRMC and truncate all before this position in line
            # then pass remaining to gpsInfoSlice
            gpsInfoSlice = line[line.find("GPRMC"):len(line)-8] 

            if(gpsInfoSlice):
                # Take a look at the original gps frame slices
                # print(gpsInfoSlice)

                # GPSplace.append(line.find("GPRMC"))


                lineList = gpsInfoSlice.split(",")

                latTemp = str(latConverter(lineList[3]))
                lineList[3] = latTemp[0:9] #+ ' ' + lineList[4]
                # print(lineList[3])

                longTemp = str(longConverter(lineList[5]))
                lineList[5] = longTemp[0:9] #+ ' ' + lineList[6]
                # print(lineList[5])


                ### DATE
                dateStr = ''
                for dateData in lineList[9:10]:
                    dateStr = dateData
                day   = ''
                month = ''
                year  = ''

                day   = dateStr[0:2]
                month = dateStr[2:4]
                year  = dateStr[4:]



                # print(lineList[1])
                ### TIME
                timeStr = ''
                for timeData in lineList[1:2]:
                    timeStr = timeData

                hour    = timeStr[0:2]
                minute  = timeStr[2:4]
                second  = timeStr[4:]

                curHour   = int(hour)
                curMinute = int(minute)
                curSecond = float(second)
                emptyFrameTrigger = 1

                # print(curHour, curMinute, curSecond)



                ## print(current_Frame)
                ## print(lineList[3][0:9])
                ## print(float(lineList[3][0:9]))



                # These three are for interp function
                frameStamp.append(int(current_Frame))
                timeForInterp.append(float(lineList[1]))
                latForInterp.append(float(lineList[3][0:9]))
                longForInterp.append(float(lineList[5][0:9]))
                speedForInterp.append(float(lineList[7]))
                azimuthForInterp.append(float(lineList[8]))


                #                                  1           3            5            7             8                      
                #                            frameIndex,     time,    latitude,   longitude,    velocity,      azimuth, day, month, year)
                jsonGPSlist = json_GPSobj(current_Frame, lineList[1], lineList[3], lineList[5], lineList[7],  lineList[8], day, month, year , str(curHour), str(curMinute), str(curSecond))
                
                videoFrameDictionary[current_Frame] = jsonGPSlist.currentFrameData()
                 

    print(videoFrameDictionary)



    frameStamp.insert(0,0)
    frameStamp.append(current_Frame)
    frameStampTup = tuple(frameStamp)

    latCopyFirstElement = latForInterp[0]
    latCopyLastElement = latForInterp[-1]
    latForInterp.insert(0,latCopyFirstElement)
    latForInterp.append(latCopyLastElement)
    latTup = tuple(latForInterp)
    interpLat = interpolateGPSpoints(frameStampTup, latTup, current_Frame)

    longCopyFirstElement = longForInterp[0]
    longCopyLastElement = longForInterp[-1]
    longForInterp.insert(0,longCopyFirstElement)
    longForInterp.append(longCopyLastElement)
    longTup = tuple(longForInterp)
    interpLong = interpolateGPSpoints(frameStampTup, longTup, current_Frame)

    speedCopyFirstElement = speedForInterp[0]
    speedCopyLastElement = speedForInterp[-1]
    speedForInterp.insert(0,speedCopyFirstElement)
    speedForInterp.append(speedCopyLastElement)
    speedTup = tuple(speedForInterp)
    interpSpeed = interpolateGPSpoints(frameStampTup, speedTup, current_Frame)

    azimuthCopyFirstElement = azimuthForInterp[0]
    azimuthCopyLastElement = azimuthForInterp[-1]
    azimuthForInterp.insert(0,azimuthCopyFirstElement)
    azimuthForInterp.append(azimuthCopyLastElement)
    azimuthTup = tuple(azimuthForInterp)
    interpAzimuth = interpolateGPSpoints(frameStampTup, azimuthTup, current_Frame)

    # for frame in range(1, len(videoFrameDictionary) + 1):       
        # print(videoFrameDictionary[frame]['hour'], videoFrameDictionary[frame]['second'], videoFrameDictionary[frame]['second'])

    
    # for frame in range(1, len(videoFrameDictionary) + 1):
        
    #     videoFrameDictionary[frame]['latitude']  = str(interpLat[frame - 1])
    #     videoFrameDictionary[frame]['longitude'] = str(interpLong[frame -1])
    #     videoFrameDictionary[frame]['velocity']  = str(interpSpeed[frame - 1])
    #     videoFrameDictionary[frame]['azimuth']   = str(interpAzimuth[frame -1])




    #     print(frame, videoFrameDictionary[frame]['latitude'], 
    #                  videoFrameDictionary[frame]['longitude'], 
    #                  videoFrameDictionary[frame]['velocity'], 
    #                  videoFrameDictionary[frame]['azimuth'],

    #                  videoFrameDictionary[frame]['hour'],
    #                  videoFrameDictionary[frame]['minute'],
    #                  videoFrameDictionary[frame]['second'],
    #                  )



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