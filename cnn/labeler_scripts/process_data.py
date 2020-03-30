import pymongo
import os
from pathlib import Path
from dotenv import load_dotenv
import gridfs

# Used to get environment variables located in the cnn folder
env_dir = Path(os.path.dirname(__file__)).parent
env_path = os.path.join(env_dir, '.env')
load_dotenv(dotenv_path=env_path)

class DB():
    def __init__(self, collection):
        self.client = pymongo.MongoClient(os.getenv('MLAB_URI'), retryWrites = False)
        self.db = self.client.get_default_database()
        self.coll = self.db[collection]
        self.fs = gridfs.GridFS(self.db)
        self.coll.create_index([('location', pymongo.GEO2D)])

    def save_to_mongo(self, labels):
        # fs.put saves image using GridFS; it returns an ID that is used to associate the uploaded image to the labels that are being saved
        # TODO: make filetype match the file being uploaded
        
        
        for label in labels:
            image_path = label['image_path']
            image_id = self.fs.put(open(image_path, 'rb'), filename=image_path, filetype='jpeg')
            label['image_id'] = image_id
        self.coll.insert_many(labels)
        print('Labels saved to DB')

        # This code was used for testing purposes. Using the image_id, fs.get will return the binary image data
        # print(image_id)
        # file2 = open('/home/egm42/sign-spotter/cnn/test.png', 'wb')
        # file2.write(self.fs.get(image_id).read())
        # file2.close()
        
    # TODO: create a generic get_data function that will get the data that matches the query(parameters)
    def get_data(self, parameters):
        return self.coll.find(parameters).limit(3)

# TODO: send emails to the user depending on the error encountered, or when processing is done
def send_email(message, email):
    if(message == 'no_gps'):
        print('no gps')


