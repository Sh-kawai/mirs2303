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
    print("waiting for connection...")

    clientsock, client_address = serversock.accept()
    print("success connection")

    while True:
        print("end-socket:q, get_img:1, upload:2 auto_img:3")
        s_msg = input()

        print("send:%s" % s_msg)
        clientsock.sendall(s_msg.encode())
        print("waiting client response...")

        rcvmsg = clientsock.recv(1024).decode()
        print("Received:%s" % (rcvmsg))

        if s_msg == "q":
            break

    clientsock.close()

if __name__ == "__main__":
    host = "127.0.0.1"
    port = 8080
    server(host=host, port=port)