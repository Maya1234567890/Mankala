from socket import *
import sys
import json
from threading import Thread
import loginUI
from PyQt5 import QtCore, QtGui, QtWidgets


def server_recv(socket):
    while 1:
        data = json.loads(socket.recv(BUFSIZ).decode()[5:])
        print(data)


def start_game(name):
    if not name.isalnum():
        print(name)
        return
    tcpcliesock.send(json.dumps({"type":"Login","name":name}).encode('utf-8'))
    data = json.loads(tcpcliesock.recv(BUFSIZ).decode()[5:])
    print(data)
    if data["type"] != "Error":
        tcpcliesock.send(json.dumps({"type": "Start Game"}).encode('utf-8'))
        data = json.loads(tcpcliesock.recv(BUFSIZ).decode()[5:])
    print(data)


def join_game(name, id):
    if not name.isalnum() or not id.isdigit():
        print(name, id)
        return
    tcpcliesock.send(json.dumps({"type":"Login","name":name}).encode('utf-8'))
    data = json.loads(tcpcliesock.recv(BUFSIZ).decode()[5:])
    print(data)
    if data["type"] != "Error":
        tcpcliesock.send(json.dumps({"type": "Join Game", "game_id":eval(id)}).encode('utf-8'))
        data = json.loads(tcpcliesock.recv(BUFSIZ).decode()[5:])
    print(data)


HOST = '109.65.31.250'
PORT = 45000
BUFSIZ = 1024
ADDR = (HOST, PORT)
tcpcliesock = socket(AF_INET, SOCK_STREAM)
# tcpcliesock.settimeout(5)
app = QtWidgets.QApplication(sys.argv)

try:  # try to connect to the server's socket.
    tcpcliesock.connect(ADDR)
except ConnectionRefusedError:
    print("The server is closed")
except TimeoutError:
    print("Time ran out. Please try again later")
finally:
    window = QtWidgets.QMainWindow()
    login_window = loginUI.UI_login()
    login_window.setupUi(window)
    window.show()

    login_window.start_game_btn.clicked.connect(lambda: start_game(login_window.name_entry.text()))
    login_window.join_game_btn.clicked.connect(lambda: join_game(login_window.name_entry.text(), login_window.game_id_entry.text()))
    # server_recv_thread = Thread(target=lambda: server_recv(tcpcliesock), daemon=True)
    # server_recv_thread.start()

    # data = {}
    # while 1:
    #     while 1:
    #         key = input(">> ")
    #         if key == "": break
    #         value = input(">> ")
    #         if value.isdigit(): value = eval(value)
    #         data[key] = value
    #     tcpcliesock.send(json.dumps(data).encode('utf-8'))

while not app.exec_():
    # tcpcliesock.send(json.dumps({"type": "logout"}).encode('utf-8'))
    tcpcliesock.close()
    sys.exit()

