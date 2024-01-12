import socket
import pickle
from define import *

serversock = None
clientsock = None

def open(host=HOST, port=PORT):
    global serversock, clientsock

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
        return None
    except KeyboardInterrupt:
        print("[ctrl + c] program interrtupt")
        return None
        
    print("success connection")
    return clientsock

def send(s_msgs):
    global clientsock
    send_data = pickle.dumps(s_msgs)
    clientsock.sendall(send_data)
    rcvmsg = clientsock.recv(1024).decode()
    return rcvmsg

def close():
    global serversock, clientsock
    clientsock.close()
    serversock.close()
    print("[server] socket closed")

if __name__ == "__main__":
    if open():
        while True:
            print("[please input send code]")
            s_msgs = input()

            print("[server] Send : %s" % s_msgs)
            print("[server] waiting client response...")
            rcvmsg = send(s_msgs)
            for i, msg in enumerate(rcvmsg.split("\n")):
                print(f"[server] Recv{i} : {msg}")
            
            if s_msgs == "q" or rcvmsg == "client close":
                break
        close()