import time

import arduino_serial as arduino
import request
import jetson_socket as jetson
import io
import uss
import ssh
from define import *

def run_to_stop(state, speed, dist):
    state_list = [STP,STR,ROT,LINE]
    if state in state_list:
        request.set_runmode(state, speed, dist)
        time.sleep(0.01)
        while True:
            state, speed, dist = request.get_runmode()
            if state == STP:
                return 0
    else:
        print(f"state error {state_list}: {state}")
        return -1

def cam_to_stop(pwm):
    request.set_runmode(CAM, 0, pwm)
    time.sleep(0.01)
    while True:
        state, height, pwm = request.get_runmode()
        if pwm == 0:
            return 0

def linetrace(speed=20, dist=1000):
    # 教室移動 & 撮影位置移動
    request.set_runmode(LINE, 20, 1000)
    time.sleep(0.01)
    while True:
        state, speed, dist = request.get_runmode()
        if state == STP:
            return

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
    run_to_stop(LINE, 20, 1000)
    #linetrace(20, 1000)
    
    #3 昇降
    pwm = 255
    cam_to_stop(pwm)
    
    # サーボモータ
    # 35度くらいが水平
    angle = 90
    request.set_runmode(SER, angle, angle)
    time.sleep(1)
    
    # 写真撮影
    jetson.send(["pu1_click_t", gdrive_main])
    # 写真撮影後
    while not jetson.send(["pu1_click_c"]):
        time.sleep(0.1)
    print("写真を撮影しました。")
    
    print("継続するには何らかを入力してください。")
    input()
    
    run_to_stop(ROT, 60, 180)
    # ラインに角度を合わせる
    request.set_runmode(LINE, 0, 1000)
    time.sleep(1)
    
    # 帰還
    run_to_stop(LINE, 20, 1000)
    #linetrace(20, 1000)

    arduino.close()
    jetson.close()
    io.close()
    

if __name__ == "__main__":
    gdrive_main = False
    main()