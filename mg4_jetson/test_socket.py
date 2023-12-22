import socket
import threading
import time
import paramiko

import raspi_socket
from define import *

def ssh_remote():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    # client side setting ip address
    IP = HOST
    USER = "pi"
    PASS = "raspberry"
    client.connect(IP, username=USER, password=PASS)
    
    EXEC_CMD = "cd ~/mirs2303/mirs2303/mg4_pi_ver4.1.0; ./main"
    
    stdin, stdout, stderr = client.exec_command(EXEC_CMD)
    
    print

def server(host=HOST, port=PORT):
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

    while True:
        print("end-socket:q, get_img:1, get_auto_img:2 upload:3")
        s_msg = input()

        print("send:%s" % s_msg)
        clientsock.sendall(s_msg.encode())
        print("waiting client response...")

        rcvmsg = clientsock.recv(1024).decode()
        print("Received:%s" % (rcvmsg))

        if s_msg == "q" or rcvmsg == "client close":
            break

    clientsock.close()

if __name__ == "__main__":
    host = "127.0.0.1"
    port = 8080
    server(host=host, port=port)