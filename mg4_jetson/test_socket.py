import socket
import threading
import time
import raspi_socket
from define import *

def server(host=HOST, port=PORT):
    serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    serversock.bind((host,port))
    serversock.listen(10)
    timeout = 10 #[s]
    serversock.settimeout(timeout)  # timeout setting
    print("waiting for connection...")

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
        print("end-socket:q, get_img:1, upload:2 auto_img:3")
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