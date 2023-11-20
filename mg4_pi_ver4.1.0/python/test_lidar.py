import sock
import matplotlib.pyplot as plt
import config
import subprocess as sp
import sys
import time
import numpy as np
import threading
import time


def lidar_open():
    sp.run(["sh",
            "/home/pi/mirs2303/mirs2303/mg4_pi_ver4.1.0/python/lidar_cpp.sh"])

def getdata():
    s.read()
    s.send([255,3,254])
    while(1):
        if s.buffer_length() > 10:
            break
        time.sleep(0.1)
    
    return s.read()

def convertdata(received_data):
    out = np.zeros([int(len(received_data) / 10), 3])
    idx = 0
    for i in range(len(received_data)):
        if (i+9) >= len(received_data):
            break
        if received_data[i] == 255 and received_data[i+9] == 254:
            if received_data[i+1] == 11:
                for ii in range(3):
                    out[idx,0] += received_data[i+2+ii] * np.power(254,ii) / 1000.0
                    out[idx,1] += received_data[i+5+ii] * np.power(254,ii)
                out[idx,2] = received_data[i+8]
                
                idx += 1
    
    return out[:idx]
                
def disconnect():
    s.send([255,9,254])
    time.sleep(0.25)
    s.server.close()


def plotter(nparr):
    plt.clf()
    xy = np.zeros([len(nparr), 2])
    for i in range(len(nparr)):
        xy[i,0] = -1 * nparr[i,1] * np.cos(nparr[i,0] / 180.0 * np.pi)
        xy[i,1] = nparr[i,1] * np.sin(nparr[i,0] / 180.0 * np.pi)
    plt.xlim(-10 * 1000, 10 * 1000)
    plt.ylim(-10 * 1000, 10 * 1000)
    plt.scatter(xy[:,0], xy[:,1])
    plt.scatter([0],[0], c = "red", marker = "x")
    #plt.show()
    plt.pause(0.01)

def p():
    received_data = []
    while(1):
        received_data = getdata()
        if len(received_data) > 10:
            break
        time.sleep(0.5)
    nparr = convertdata(received_data)
    #plotter(nparr)

if __name__ == "__main__":
    #print("[INFO][lidar.py] : jetsonのデーモンプロセスをキルしています...")
    #sp.run(["sh",
    #        "/home/pi/mirs2303/mirs2303/mg4_pi_ver4.1.0/python/lidar_cpp.sh"])
    #time.sleep(1)
    
    s = sock.sock_server(config.RASPI_IP, config.SOCKET_PORT)
    while(1):
        if(s.server_started == True):
            break
    time.sleep(1)
    print("[INFO][lidar.py] : ソケット通信を確立しています...")
    lidar_thread = threading.Thread(target=lidar_open)
    lidar_thread.start()
    
    while(1):
        if (s.isconnected() > 0):
            break
    
    time.sleep(1)
    print("[INFO][lidar.py] : ソケット通信を確立しました...")

    send_data = 0
    while send_data == 0:
        print("入力してください 0:一時停止 1:1回取得 2:常時取得 -1:強制終了")
        send_data = int(input())
        if send_data >= -1 and send_data <= 2:
            s.send([send_data])
        if send_data is not 0:
            break
    
    if send_data == 2:
        while(1):
            start_time = time.time()
            p()
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"経過時間: {elapsed_time}秒")
    elif send_data == 1:
        p()