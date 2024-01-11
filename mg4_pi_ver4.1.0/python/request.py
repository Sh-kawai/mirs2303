import time
import arduino_serial as arduino
from define import *

def set_runmode(state, speed, dist):
    speed = int(speed)
    dist = int(dist)
    command_data = [state + 1, speed, dist]
    arduino.send(command_data)

def get_runmode():
    command_data = [10, 0, 0]
    arduino.recv_clear()
    arduino.send(command_data)
    time.sleep(0.05)
    data = arduino.recv()

    return data[0], data[1], data[2]

def get_cammode():
    command_data = [13, 0, 0]
    arduino.recv_clear()
    arduino.send(command_data)
    time.sleep(0.05)
    data = arduino.recv()
    
    return data[0], data[1], data[2]

def get_dist():
    command_data = [11, 0, 0]
    arduino.recv_clear()
    arduino.send(command_data)
    time.sleep(0.05)
    data = arduino.recv()

    return data[0], data[1]

def get_batt():
    command_data = [12, 0, 0]
    arduino.recv_clear()
    arduino.send(command_data)
    time.sleep(0.05)

    return arduino.recv()[0] / 100.0

if __name__ == "__main__":
    if arduino.open():
        print(get_runmode())

        arduino.close()