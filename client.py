from socket import *
import sys
import json
from threading import Thread


def server_recv(socket):
    while 1:
        data = socket.recv(1024)
        print(data)


HOST = '79.179.71.212'
PORT = 45000
BUFSIZ = 1024
ADDR = (HOST, PORT)
tcpcliesock = socket(AF_INET, SOCK_STREAM)
# tcpcliesock.settimeout(5)

try:  # try to connect to the server's socket.
    tcpcliesock.connect(ADDR)
except ConnectionRefusedError:
    print("The server is closed")
except timeout:
    print("Time ran out. Please try again later")
else:
    server_recv_thread = Thread(target=lambda: server_recv(tcpcliesock), daemon=True)
    server_recv_thread.start()
    #Thread.start(server_recv(tcpcliesock))
    data = {}
    while 1:
        while 1:
            key = input(">>")
            if key == "": break
            value = input(">>")
            if value == "": value = 0
            data[key] = value
        tcpcliesock.send(json.dumps(data).encode('utf-8'))

tcpcliesock.close()
