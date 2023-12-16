import socket

import upload, get_img

from define import *

def client(host=HOST, port=PORT):
  letter_coding = "UTF-8"

  # オブジェクトの作成をします
  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  client.connect((host, port)) #これでサーバーに接続します

  print("success connection")
  while True:
    print("Waiting server response...")
    response = client.recv(4096).decode()
    print('Received: %s' % response)

    if response == "q":
      break
    elif response == "1":
      get_img.get_img(place="kari")
    elif response == "2":
      upload.main()

    message = "client wait"
    print('Send : %s' % message)
    client.send(message.encode(letter_coding))
  
  message = "client close"
  print('Send : %s' % message)
  client.send(message.encode(letter_coding))
  client.close()

if __name__ == "__main__":
  host = "127.0.0.1"
  port = 8080
  client(host=host, port=port)