import time
import subprocess

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

def main():
    #ssh.bringup_jetson()
    subprocess.run(["/home/mirs2303/mirs2303/mg4_jetson/bringup.bash"])
    if not jetson.open():
        return
    if not arduino.open():
        return
    #if not io.open():
    #    return
    #if not uss.open(uss.ADDRESS_L) or not uss.open(uss.ADDRESS_R):
    #    return

    # スケジュール確認

    print("key_wait run")
    input()

    # susumu
    run_to_stop(LINE, 15, 1000)
    time.sleep(1)

    #**********************************
    rot_angle = 0
    request.set_runmode(CAM, 0, 255)
    time.sleep(5)
    request.set_runmode(CAM, 0, 0)
    time.sleep(1)
    
    angle = 90
    request.set_runmode(SER, angle, angle)
    time.sleep(1)
    
    print("key_wait photo")
    input()

    # 写真撮影
    jetson.send({"key":"pu1", "gdrive_main":gdrive_main})
    time.sleep(1)

    #**********************************

    print("key_wait return")
    input()

    run_to_stop(ROT, 60, 180)
    time.sleep(1)

    # kikann
    run_to_stop(LINE, 15, 1000)
    time.sleep(1)

    run_to_stop(ROT, 60, 180)
    time.sleep(1)

    cam_to_stop(-255)

    arduino.close()
    jetson.close()

if __name__ == "__main__":
    gdrive_main = False
    main()