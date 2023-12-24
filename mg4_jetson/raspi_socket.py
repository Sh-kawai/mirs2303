import socket
import threading
import queue

import mg4_jetson.upload as upload
import get_img
from define import *

def client(host=HOST, port=PORT):
  
  state = 0
  # エンコード
  letter_coding = "UTF-8"

  # オブジェクトの作成
  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  # サーバーに接続
  client.connect((host, port))

  # thread share data(get_auto_img)
  q_stop = queue.Queue(1)
  auto_run = False
  
  # thread share data(upload soon)
  q_save_e = queue.Queue(1)
  
  #capture flag
  cap_open_state = False
  
  print("success connection")
  while True:
    print("Waiting server response...")
    response = client.recv(4096).decode()
    print('Received: %s' % response)

    message = "client wait"

    try:
      if response == "q":
        break
      elif response == "1": # get_img once
        if not cap_open_state:
          get_img.save_img()
        else:
          message = "already open capture\nDon't save_img()"
      elif response == "2": # start get_auto_img
        if not auto_run or not cap_open_state:
          thread_get_auto_img = threading.Thread(target=get_img.save_auto_img, kwargs={"q_stop": q_stop, "show":True}, daemon=True)
          thread_get_auto_img.start()
          message = "Start get_auto_img()"
        else:
          message = "already start get_auto_img()"
        auto_run = True
        cap_open_state = True
      elif response == "22": # stop get_auto_img
        if auto_run:
          # thread end process
          q_stop.put(True)
          thread_get_auto_img.join()
          message = "Finish get_auto_img()"
        else:
          message = "don't run get_auto_img()"
        auto_run = False
        cap_open_state = False
      elif response == "3": # upload for gdrive
        upload.main(gdrive_main=True)
      elif response == "4": # upload soon
        pass

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