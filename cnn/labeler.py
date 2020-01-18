import sys

def main():
  arguements = sys.argv
  video = arguements[1]
  email = arguements[2]
  time = arguements[3]
  message = 'Recieved video '+ video+ ' from '+ email + ' at ' + time
  print(message)
  file = open('C:/Users/luisg/Documents/GitHub/sign-spotter/cnn/' + video + time + '.txt', 'w')
  file.write(message)
  file.close()

if __name__ == '__main__':
  main()