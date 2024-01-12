import time

import arduino_serial as arduino
import request
import jetson_socket as jetson
import io
import uss
import ssh
from define import *

def main():
    #ssh.bringup_jetson()
    if not jetson.open():
        return
    if not arduino.open():
        return
    if not io.open():
        return
    if not uss.open(uss.ADDRESS_L) or not uss.open(uss.ADDRESS_R):
        return

    # スケジュール確認

    # 教室移動 & 撮影位置移動
    request.set_runmode(LINE, 0, 0)
    time.sleep(0.01)
    while True:
        state, speed, dist = request.get_runmode()
        if state == STP:
            break
    
    pwm = 255
    request.set_runmode(CAM, 0, pwm)
    time.sleep(0.01)
    while True:
        state, height_curr, pwm_curr = request.get_cammode()
        if pwm == 0:
            break
    
    angle = 90
    request.set_runmode(SER, angle, angle)
    time.sleep(1)
    
    # 写真撮影
    jetson.send("p1")


    arduino.close()

if __name__ == "__main__":
    main()