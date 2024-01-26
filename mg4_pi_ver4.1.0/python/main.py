import time
import subprocess

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
        time.sleep(0.5)
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
        time.sleep(0.5)
        if pwm == 0:
            return 0

def cam_to_stop_time(pwm, time_):
    request.set_runmode(CAM, 0, pwm)
    time.sleep(time_)
    request.set_runmode(CAM, 0, 0)

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

    line_speed = 20
    rot_speed = 60
    wait_time = 1
    break_flag = False

    cam_to_stop_time(-255, 10)
    cam_to_stop(-255)
    request.set_runmode(SER, 30, 30)

    # susumu
    for i in range(2):
        break_flag = False
        rot_flag = pow(-1, i)
        while True:
            print(f"{i} LINE")
            run_to_stop(LINE, line_speed, 100)
            time.sleep(wait_time)
            
            state = request.get_light()[0]
            print(f"{i} LINE_STATE {state}")

            if state == STP:
                break_flag = True

            print(f"{i} ROT")
            run_to_stop(ROT, rot_speed, -90 * rot_flag)
            time.sleep(wait_time)
            
            print(f"{i} PHOTO")
            jetson.send({"key":"p1"})
            time.sleep(wait_time)

            #print(f"{i} CAM")
            #cam_to_stop_time(-255, 5)
            print(f"{i} ROT")
            run_to_stop(ROT, rot_speed, 180 * rot_flag)
            time.sleep(wait_time)
            
            print(f"{i} PHOTO")
            jetson.send({"key":"p1"})
            time.sleep(wait_time)

            print(f"{i} ROT")
            run_to_stop(ROT, rot_speed, -90 * rot_flag)
            time.sleep(wait_time)

            if break_flag:
                break
        
        print("white line stop")
        run_to_stop(ROT, rot_speed, 180)
        time.sleep(wait_time)

    arduino.close()
    jetson.close()

if __name__ == "__main__":
    gdrive_main = True
    main()