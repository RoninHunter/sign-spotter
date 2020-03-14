import sys
import labeler_scripts as scripts

def main():
  # arguements = sys.argv
  # video = arguements[1]
  # email = arguements[2]
  # time = arguements[3]
  # message = 'Recieved video '+ video+ ' from '+ email + ' at ' + time
  # print(message)
  # file = open('../cnn/' + video + time + '.txt', 'w')
  # file.write(message)
  # file.close()

  print(scripts.test('Test input'))
  print(scripts.split_video('/test/path', '/test/path'))

if __name__ == '__main__':
  main()