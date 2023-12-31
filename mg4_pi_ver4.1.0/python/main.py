import time

import arduino_serial as arduino
import request
import jetson_socket as jetson
from define import *

def main():
    if not arduino.open():
        return
    #if not jetson.open():
        return

    # スケジュール確認

    # 教室移動 & 撮影位置移動
    request.set_runmode(LINE, 0, 0)
    time.sleep(1)
    while True:
        state, speed, dist = request.get_runmode()
        if state == STP:
            break
    
    # 写真撮影
    


    arduino.close()

if __name__ == "__main__":
    main()