def save_to_mongo(labels):
    # TODO: save data to mongo, the original image should also be saved to mongo

    print('Labels saved to DB')
    print(labels)

def send_email(message, email):
    if(message == 'no_gps'):
        print('no gps')