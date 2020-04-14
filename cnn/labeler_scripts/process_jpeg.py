# darknetpy installed using prebuilt binary: https://github.com/danielgatis/darknetpy
from darknetpy.detector import Detector
from matplotlib import image, patches, pyplot as plt
# import tensorflow as tf
import time
import os
import numpy as np
import cv2
from PIL import Image

class imageLabeler():
    def __init__(self):
        # self.classes = {
        # 	1: 'stop',
        #     2: 'speedLimit15',
        #     3: 'speedLimit20',
        #     4: 'speedLimit25',
        #     5: 'speedLimit30',
        #     6: 'speedLimit35',
        #     7: 'speedLimit40',
        #     8: 'speedLimit45',
        #     9: 'speedLimit50',
        #     10: 'speedLimit55',
        #     11: 'speedLimit60',
        #     12: 'speedLimit65',
        #     13: 'pedestrianCrossing',
        #     14: 'bicycleLane',
        #     15: 'suicideLane',
        #     16: 'yield',
        #     17: 'signalAhead',
        #     18: 'addedLane',
        #     19: 'curveLeft',
        #     20: 'curveRight',
        #     21: 'dip',
        #     22: 'doNotEnter',
        #     23: 'keepRight',
        #     24: 'laneEnds',
        #     25: 'merge',
        #     26: 'noLeftTurn',
        #     27: 'noRightTurn',
        #     28: 'rightLaneMustTurn',
        #     29: 'school',
        #     30: 'slow',
        #     31: 'stopAhead',
        #     32: 'schoolSpeedLimit25',
        #     33: 'schoolSpeedLimit15'
        # }	
        self.detector = Detector(
            os.path.join(os.getcwd(), 'cnn/models/darknet', 'coco.data'),
            os.path.join(os.getcwd(), 'cnn/models/darknet', 'yolov3.cfg'),
            os.path.join(os.getcwd(), 'cnn/models/darknet', 'yolov3.weights')
        )

    def labelDarknet(self, image_path, side):
        boxes = self.detector.detect(image_path)

        im = Image.open(image_path)

        labels = []
        for box in boxes:
            labels.append(
                {
                    'class': box['class'],
                    'xmin': box['left']/im.size[0],
                    'xmax': box['right']/im.size[0],
                    'ymin': box['top']/im.size[1],
                    'ymax': box['bottom']/im.size[1],
                    'side': side
                }
            )
        
        return labels

    def drawImage(self, boxes, image_path, dest):
        fig, ax = plt.subplots(1)
        ax.imshow(image.imread(image_path))

        colors = ['r', 'b', 'y']

        for i, box in enumerate(boxes):
            l = box['left']
            t = box['top']
            b = box['bottom']
            r = box['right']
            c = box['class']
            color = colors[i % len(colors)]
            
            rect = patches.Rectangle(
                (l, t), 
                r - l, 
                b - t,
                linewidth = 1, 
                edgecolor = color, 
                facecolor = 'none'
            )
            
            ax.text(l, t, c, fontsize = 12, bbox = {'facecolor': color, 'pad': 2, 'ec': color})
            ax.add_patch(rect)

        plt.savefig(os.path.join(dest, os.path.basename(image_path)))
        

    def labelTensor(self, image_path, side):
        model_location = os.path.join(os.getcwd(), 'cnn/models/tensorflow')
        checkpoint = os.path.join(model_location, 'frozen_inference_graph.pb')
        labels = os.path.join(model_location, 'labelmap.pb.txt')
        config = os.path.join(model_location, 'pipeline.config')
    #     model_location = '/home/egm42/sign-spotter/cnn/models/tensorflow'
    #     checkpoint = '/home/egm42/sign-spotter/cnn/models/tensorflow/frozen_inference_graph.pb'
    #     labels = '/home/egm42/sign-spotter/cnn/models/tensorflow/labelmap.pbtxt'
    #     num_classes = 33

    

    #     detection_graph = tf.Graph()
    #     with detection_graph.as_default():
    #         od_graph_def = tf.GraphDef()
    #         with tf.gfile.GFile(checkpoint, 'rb') as fid:
    #             serialized_graph = fid.read()
    #             od_graph_def.ParseFromString(serialized_graph)
    #             tf.import_graph_def(od_graph_def, name='')

    #         sess = tf.Session(graph=detection_graph)

    #     image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

    #     # Output tensors are the detection boxes, scores, and classes
    #     # Each box represents a part of the image where a particular object was detected
    #     detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

    #     # Each score represents level of confidence for each of the objects.
    #     # The score is shown on the result image, together with the class label.
    #     detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
    #     detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')

    #     # Number of objects detected
    #     num_detections = detection_graph.get_tensor_by_name('num_detections:0')

    #     # Load image using OpenCV and
    #     # expand image dimensions to have shape: [1, None, None, 3]
    #     # i.e. a single-column array, where each item in the column has the pixel RGB value
    #     image = cv2.imread(image_path)
    #     image_expanded = np.expand_dims(image, axis=0)

    #     (boxes, scores, classes, num) = sess.run(
    #         [detection_boxes, detection_scores, detection_classes, num_detections],
    #         feed_dict={image_tensor: image_expanded})


    #     labels = []
    #     box = []
    #     for n in range(int(num[0])):
    #         # print(scores[0][n])
    #         if(scores[0][n] >= 0.6):
    #             label = {
    #                 'class': self.classes[classes[0][n]],
    #                 'ymin': float(boxes[0][n][0]),
    #                 'xmin': float(boxes[0][n][1]),
    #                 'ymax': float(boxes[0][n][2]),
    #                 'xmax': float(boxes[0][n][3]),
    #                 'side': side
    #             }
    #             box = boxes[0][n]
    #             labels.append(label)
    #     print(image_path, labels)
    #     # cv2.imwrite(os.path.join(CWD_PATH,"test_images","output_" + IMAGE_NAME),new_image)

    #     return labels

if __name__ == '__main__':
    labeler = imageLabeler()
    # labels = labeler.labelDarknet('/home/egm42/sign-spotter/cnn/jpegs/REC_2020_04_04_08_40_13_F_57_image_r.jpg')
    labels = labeler.labelDarknet('/home/egm42/sign-spotter/cnn/models/darknet/eagle.jpg')
    print(labels)
