import socket

import upload
import get_img
import thread_ctrl
from define import *

"""
# p: 写真, v: 動画, u:アップロード
# s: スレッド開始, f: スレッド終了
# t: スレッド(自動終了), c: スレッド終了チェック
# 番号: 組み合わせ上被らないように
"""
S_EXPLAIN = """
#############################################
q:  終了

p1:   一枚 撮影(即時)
p2_s:   定期 撮影(スレッド開始)
p2_f:  定期 撮影終了(スレッド終了)

v1_t:   一動画 撮影(即時 30秒)(スレッド)
v1_c:   一動画 撮影 終了チェック

u1_t:   全画像 アップロード(スレッド)
u1_c:   全画像 アップロード チェック

pu1:  一枚 撮影&アップロード(即時)
pu2_s:  定期 撮影&アップロード(スレッド開始)
pu2_f: 定期 撮影&アップロード終了(スレッド終了)
##############################################
"""

# グローバル変数
_gdrive_main = False    

# socket client
def client(host=HOST, port=PORT):
  global _gdrive_main
  
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

    message = "client wait"
    
    try:
      
      if response == "q":
        message = "client close"
        break
      # p1:   一枚 撮影(即時)
      elif response == "p1":
        if not get_img.cap_flag():
          save_path = get_img.get_img()
          message = f"save picture:{save_path}"
        else:
          message = "other capture opened"
      # p2_s:   定期 撮影(スレッド開始)
      elif response == "p2_s":
        if not get_img.cap_flag():
          start_flag = thread_ctrl.thread_start("p2",get_img.get_auto_img, kwargs={"show":True})
          if start_flag:
            message = "start thread get_suto_img()"
          else:
            message = "already start thread save_suto_img()"
        else:
          message = "other capture opened"
      # p2_f:  定期 撮影終了(スレッド終了)
      elif response == "p2_f":
        fin_flag = thread_ctrl.thread_finish("p2")
        if fin_flag:
          message = "finish thread save_suto_img()"
        else:
          message = "didn't run thread save_suto_img()"
      # v1_t:   一動画 撮影(即時 30秒)(スレッド)
      elif response == "v1_t":
        if not get_img.cap_flag():
          thread_flag = thread_ctrl.auto_thread_run("v1", get_img.save_movie)
          if thread_flag:
            message = "auto-thread save_movie()"
          else:
            message = "run other save_movie()"
        else:
          message = "didn't run thread save_suto_img()"
      # v1_c:   一動画 撮影 終了チェック
      elif response == "v1_c":
        check_flag = thread_ctrl.auto_thread_check("v1")
        if check_flag:
          message = "finish save_movie()"
        else:
          message = "runnning save_movie()"
      # u1_t:   全画像 アップロード(スレッド)
      elif response == "u1_t":
        thread_flag = thread_ctrl.auto_thread_run("u1", upload.main, {"gdrive_main":_gdrive_main})
        if thread_flag:
          message = f"auto-thread upload.main() [gdrive_main={_gdrive_main}]"
        else:
          message = "run other upload.main()"
      # u1_c:   全画像 アップロード チェック
      elif response == "u1_c":
        check_flag = thread_ctrl.auto_thread_check("u1")
        if check_flag:
          message = "finish upload.main()"
        else:
          message = "running upload.main()"
      # pu1:  一枚 撮影&アップロード(即時)
      elif response == "pu1":
        if not get_img.cap_flag():
          save_path = get_img.get_img()
          save_file = os.path.basename(save_path)
          file_id = upload.upload(save_file, gdrive_main=_gdrive_main)
          message = f"save picture:{save_path}\n"
          message += f"upload id:{file_id} [gdrive_main={_gdrive_main}]"
        else:
          message = "other capture opened"
      # pu2_s:  定期 撮影&アップロード(スレッド開始)
      elif response == "pu2_s":
        start_flag = thread_ctrl.thread_start("pu2", None, None)
        if start_flag:
          message = "start thread ()"
        else:
          message = "already start thread ()"
      # pu2_F: 定期 撮影&アップロード終了(スレッド終了)
      elif response == "pu2_f":
        fin_flag = thread_ctrl.thread_finish("pu2")
        if fin_flag:
          message = "finish thread save_suto_img()"
        else:
          message = "didn't run thread save_suto_img()"
    
    except FileNotFoundError as e:
      message = f"[jetson] FileNotFoundError: {e}"
      print(message)
      print('Send : %s' % message)
      client.sendall(message.encode(letter_coding))
      client.close()
      exit()
    except Exception as e:
      message = f"[jetson] Cought an Exceptiion: {e}"
      print(message)
      print('Send : %s' % message)
      client.sendall(message.encode(letter_coding))
      client.close()
      exit()
    
    print('Send : %s' % message)
    client.send(message.encode(letter_coding))
  
  message = "client close"
  print('Send : %s' % message)
  client.sendall(message.encode(letter_coding))
  client.close()

if __name__ == "__main__":
  host = "127.0.0.1"
  port = 8080
  _gdrive_main = False # global
  client(host, port)