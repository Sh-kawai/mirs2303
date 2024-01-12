import socket
import threading
import subprocess 
import pickle

import raspi_socket
from define import *

def client_open():
    #subprocess.run(["cd", f"{JETSON_PATH}"])
    subprocess.run(["python", "c:/Users/kawai/OneDrive - 独立行政法人 国立高等専門学校機構/4年/MIRS/プログラム/開発プログラム/mg4_jetson/raspi_socket.py"])

def server(host=HOST, port=PORT):
    client_thread = threading.Thread(target=client_open, daemon=True)
    client_thread.start()
    
    serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    serversock.bind((host,port))
    serversock.listen(10)
    timeout = 10 #[s]
    serversock.settimeout(timeout)  # timeout setting
    print(f"waiting for connection...(timeout {timeout}sec)")

    try:
        clientsock, client_address = serversock.accept()
    except socket.timeout:
        print(f"Timeout: No connection within {timeout} second.")
        return
    except KeyboardInterrupt:
        print("[ctrl + c] program interrtupt")
        return
        
    print("success connection")
    print(raspi_socket.S_EXPLAIN)
    
    while True:
        
        s_msg_dist = {}
        print("[please input send code]")
        print("key")
        key = input()
        s_msg_dist["key"] = key
        if "u" in key:
            print("gdrive_main (T or F)")
            _g = input()
            if _g == "t" or _g == "T":
                s_msg_dist["gdrive_main"] = True
            else:
                s_msg_dist["gdrive_main"] = False                
        if "v" in key:
            print("rec_time[s]")
            rec_time = int(input())
            s_msg_dist["rec_time"] = rec_time
                
        
        s_data = pickle.dumps(s_msg_dist)
        
        print(raspi_socket.S_EXPLAIN)

        print(f"[server] Send : {s_msg_dist}")
        #clientsock.sendall(s_msg.encode())
        clientsock.sendall(s_data)
        print("[server] waiting client response...")

        rcvmsg = clientsock.recv(1024).decode()
        for i, msg in enumerate(rcvmsg.split("\n")):
            print(f"[server] Recv{i} : {msg}")

        if "q" in s_msg_dist or rcvmsg == "client close":
            break 

    clientsock.close()
    serversock.close()

if __name__ == "__main__":
    host = "127.0.0.1"
    port = 8080
    server(host=host, port=port)