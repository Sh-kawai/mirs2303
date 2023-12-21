import socket
import threading
import upload, get_img

from define import *

def client(host=HOST, port=PORT):
  
  state = 0
  # エンコード
  letter_coding = "UTF-8"

  # オブジェクトの作成
  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  # サーバーに接続
  client.connect((host, port))
  

  print("success connection")
  while True:
    print("Waiting server response...")
    response = client.recv(4096).decode()
    print('Received: %s' % response)

    try:
      if response == "q":
        break
      elif response == "1":
        get_img.get_img(place="kari")
      elif response == "2":
        thread = threading.Thread(target=get_img.get_img, kwargs={"time_auto": True}, daemon=True)
        thread.start()
      elif response == "22":
        # thread end process
        pass
      elif response == "3":
        upload.main()

    except FileNotFoundError as e:
      message = f"[jetson] FileNotFoundError: {e}"
      print(message)
      print('Send : %s' % message)
      client.send(message.encode(letter_coding))
      client.close()
      exit()
    except Exception as e:
      message = f"[jetson] Cought an Exceptiion: {e}"
      print(message)
      print('Send : %s' % message)
      client.send(message.encode(letter_coding))
      client.close()
      exit()

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
  client(host, port)