import time

import arduino_serial as arduino
import request
import jetson_socket as jetson
import io
#import uss
import ssh
from define import *

def run_to_stop(state, speed, dist):
    state_list = [STP,STR,ROT,LINE]
    if state in state_list:
        request.set_runmode(state, speed, dist)
        time.sleep(0.01)
        print(f"set state {state}")
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
    print("set state CAM")
    while True:
        state, height, pwm = request.get_cammode()
        print(pwm)
        time.sleep(0.5)
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
    #if not io.open():
    #    return
    #if not uss.open(uss.ADDRESS_L) or not uss.open(uss.ADDRESS_R):
    #    return

    # スケジュール確認

    print("key_wait run straight and rotation left")
    input()

    # 教室移動 & 撮影位置移動
    #run_to_stop(LINE, 20, 1000)
    run_to_stop(STR, 15, 350)
    #linetrace(20, 1000)
    time.sleep(1)
    
    run_to_stop(ROT, 30, 90)
    time.sleep(1)

    print("key_wait up camera and serbo")

    cam_to_stop(255)
    time.sleep(1)

    request.set_runmode(SER, 45, 45)
    time.sleep(1)

    jetson.send({"key":"pu1_click", "gdrive_main":False})
    time.sleep(1)

    print("key_wait rotation and straight return")
    run_to_stop(ROT, 30, 90)
    time.sleep(1)

    run_to_stop(STR, 15, 300)
    time.sleep(1)

    arduino.close()
    jetson.close()
    #io.close()

    return
    

if __name__ == "__main__":
    gdrive_main = False
    main()