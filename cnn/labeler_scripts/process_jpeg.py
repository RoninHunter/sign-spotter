import random

def label(image_path):
    labels = []
    if(bool(random.getrandbits(1))):
        labels = [{'class': 'stop', 'xmin': 1, 'ymax': 2, 'xmax': 3, 'ymin': 4}]
    return labels