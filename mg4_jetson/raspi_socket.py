import socket

import main, get_img

host = "172.25.19.3"
port = 8080
letter_coding = "UTF-8"

# オブジェクトの作成をします
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((host, port)) #これでサーバーに接続します

print("success connection")

print("Waiting server response...")
response = client.recv(4096).decode(letter_coding)
print('Received: %s' % response)

print(response == "True")
if response == "True":
  get_img.get_img
  main.main()

message = "client wait"
print('Send : %s' % message)
client.send(message.encode(letter_coding))