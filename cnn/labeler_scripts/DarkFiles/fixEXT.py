import os
import shutil


def fixEXT(files):
  for file in files:
    with open(file, 'r') as f:
      with open(file + 'new.txt', 'w') as newf:
        for imgpath in f:
          if(os.path.isfile(imgpath)):
            newf.write(imgpath + '\n')
          else:
            editpath = imgpath.split('.')[0] + '.png'
            newf.write(editpath + '\n')
  
if __name__ == '__main__':
  # Absolute path for train and test text files
  fixEXT(['/home/lil-as/Desktop/DARKNET_GOODS/train.txt', '/home/lil-as/Desktop/DARKNET_GOODS/test.txt'])