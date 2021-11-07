from socket import*
import sys
import json

HOST = '79.179.71.212'
PORT = 45000
BUFSIZ = 1024
ADDR = (HOST, PORT)
tcpcliesock = socket(AF_INET, SOCK_STREAM)
#tcpcliesock.settimeout(5)

try:  # try to connect to the server's socket.
    tcpcliesock.connect(ADDR)
except ConnectionRefusedError:
    print("The server is closed")
except timeout:
    print("Time ran out. Please try again later")
else:
    while 1:
        data = tcpcliesock.recv(BUFSIZ)
        print(data.decode('utf-8'))
        data = {}
        while 1:
            key = input(">>")
            if key == "": exit()
            value = input(">>")
            if value == "": value = True
            data[key] = value
        tcpcliesock.send(json.dumps(data).encode('utf-8'))

tcpcliesock.close()

