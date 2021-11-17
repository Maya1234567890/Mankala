from socket import *
import sys
import json
from threading import Thread
import loginUI
import boardUi
from PyQt5 import QtCore, QtGui, QtWidgets


def server_recv(socket):
    while 1:
        try:
            #data = json.loads(socket.recv(BUFSIZ).decode()[5:])
            data = socket.recv(BUFSIZ).decode('utf-8')
            print(data)
        except OSError:
            exit()


def start_game(name):
    if not name.isalnum():
        print("Enter a name, not a digit")
        return
    tcpcliesock.send(json.dumps({"type":"Login","name":name}).encode('utf-8'))
    """data = json.loads(tcpcliesock.recv(BUFSIZ).decode()[5:])
    print(data)
    if data["type"] != "Error":
        tcpcliesock.send(json.dumps({"type": "Start Game"}).encode('utf-8'))
        data = json.loads(tcpcliesock.recv(BUFSIZ).decode()[5:])
    print(data)"""
    tcpcliesock.send(json.dumps({"type": "Start Game"}).encode('utf-8'))

    # trying to open the board window, however failing :(
    """win = QtWidgets.QMainWindow()
    mancala_window = boardUi.Ui_Form()
    mancala_window.setupUi(win)
    win.show()"""


def join_game(name, id):
    if not name.isalnum() or not id.isdigit():
        print("Name can't be a digit and the game ID has to be a digit")
        return
    tcpcliesock.send(json.dumps({"type":"Login","name":name}).encode('utf-8'))
    tcpcliesock.send(json.dumps({"type": "Join Game", "game_id": eval(id)}).encode('utf-8'))

    """data = json.loads(tcpcliesock.recv(BUFSIZ).decode()[5:])
    print(data)
    if data["type"] != "Error":
        tcpcliesock.send(json.dumps({"type": "Join Game", "game_id":eval(id)}).encode('utf-8'))
        data = json.loads(tcpcliesock.recv(BUFSIZ).decode()[5:])
    print(data)"""


HOST = '79.179.102.188'
PORT = 45000
BUFSIZ = 1024
ADDR = (HOST, PORT)
tcpcliesock = socket(AF_INET, SOCK_STREAM)
tcpcliesock.settimeout(5)
app = QtWidgets.QApplication(sys.argv)

try:  # try to connect to the server's socket.
    tcpcliesock.connect(ADDR)
except ConnectionRefusedError:
    print("The server is closed")
except TimeoutError:
    print("Time ran out. Please try again later")
finally:
    tcpcliesock.settimeout(None)
    server_recv_thread = Thread(target=lambda: server_recv(tcpcliesock), daemon=True)
    server_recv_thread.start()

    window = QtWidgets.QMainWindow()
    login_window = loginUI.UI_login()
    login_window.setupUi(window)
    window.show()

    login_window.start_game_btn.clicked.connect(lambda: start_game(login_window.name_entry.text()))
    login_window.join_game_btn.clicked.connect(lambda: join_game(login_window.name_entry.text(), login_window.game_id_entry.text()))


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
