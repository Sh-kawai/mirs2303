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

    line_speed = 20
    rot_speed = 60
    wait_time = 1

    # susumu
    for i in range(2):
        while True:
            run_to_stop(LINE, line_speed, 300)
            time.sleep(wait_time)
            
            state = request.get_light()[0]
            print(state)
            if state == STP:
                break

            run_to_stop(ROT, rot_speed, 90)
            time.sleep(wait_time)
                    
            jetson.send({"key":"p1"})
            time.sleep(wait_time)

            run_to_stop(ROT, rot_speed, -180)
            time.sleep(wait_time)
                    
            jetson.send({"key":"p1"})
            time.sleep(wait_time)

            run_to_stop(ROT, rot_speed, 90)
            time.sleep(wait_time)
        
        print("white line stop")
        run_to_stop(ROT, rot_speed, 180)
        time.sleep(wait_time)

    arduino.close()
    jetson.close()

if __name__ == "__main__":
    gdrive_main = True
    main()