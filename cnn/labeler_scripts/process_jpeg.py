# darknetpy installed using prebuilt binary: https://github.com/danielgatis/darknetpy
from darknetpy.detector import Detector
from matplotlib import image, patches, pyplot as plt
# import tensorflow as tf
# from python_utils import label_map_util
# import time
import os

class imageLabeler():
    def __init__(self):
        self.detector = Detector(
            os.path.join(os.getcwd(), 'cnn/models/darknet', 'signspotter.data'),
            os.path.join(os.getcwd(), 'cnn/models/darknet', 'yolov3.cfg'),
            os.path.join(os.getcwd(), 'cnn/models/darknet', 'yolov3_3000.weights')
        )

    def labelDarknet(self, image_path):
        # detector = Detector(
        # '/home/egm42/sign-spotter/cnn/models/darknet/signspotter.data',
        # '/home/egm42/sign-spotter/cnn/models/darknet/yolov3.cfg',
        # '/home/egm42/sign-spotter/cnn/models/darknet/yolov3_3000.weights'
        # )
        # print(time.time())
        print('labeling')
        labels = self.detector.detect(image_path)
        # print(time.time())

        fig, ax = plt.subplots(1)
        ax.imshow(image.imread(image_path))

        colors = ['r', 'b', 'y']

        for i, box in enumerate(labels):
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

        plt.savefig('test.png')
        # Tensorflow model
        # model_location = '/home/egm42/sign-spotter/cnn/models/tensorflow'
        # checkpoint = '/home/egm42/sign-spotter/cnn/models/tensorflow/frozen_inference_graph.pb'
        # labels = '/home/egm42/sign-spotter/cnn/models/tensorflow/labelmap.pbtxt'
        # num_classes = 33

        # label_map = label_map_util.load_labelmap(labels)
        # categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=num_classes, use_display_name=True)
        # category_index = label_map_util.create_category_index(categories)
        return labels

    def labelTensor(image_path):
        labels = []

        return labels

if __name__ == '__main__':
    labeler = imageLabeler()
    labels = labeler.labelDarknet('/home/egm42/sign-spotter/cnn/jpegs/REC_2020_04_04_08_40_13_F_57_image_r.jpg')
    print(labels)