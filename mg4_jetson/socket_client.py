import socket

import main

host = "127.0.0.1"
port = 65353

# オブジェクトの作成をします
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((host, port)) #これでサーバーに接続します

print("success connection")

while True:
  print("Waiting server response...")
  response = client.recv(4096).decode()
  print('Received: %s' % response)
  
  if response == "True":
    main.main()
  
  message = "client wait"
  print('Send : %s' % message)
  client.send(message.encode())