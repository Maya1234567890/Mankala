from socket import *
import sys
import json
from threading import Thread
import loginUI
import boardUi
from PyQt5 import QtCore, QtGui, QtWidgets
import time

popup = []


def server_recv():
    global tcpcliesock
    while True:
        try:
            msg = json.loads(tcpcliesock.recv(BUFSIZ).decode()[5:])
            # msg = socket.recv(BUFSIZ).decode('utf-8')
            print(msg)
        except OSError:
            exit()


def board_window(id):
    Form = QtWidgets.QWidget()
    ui = boardUi.Ui_Form()
    ui.setupUi(Form)
    ui.label_2.setText('Game ID: ' + str(id))
    Form.show()  # TODO command show doesn't work. Why?
    global popup
    popup.append(Form)

    server_recv_thread = Thread(target=lambda: server_recv(), daemon=True)
    server_recv_thread.start()


def start_game(name):
    global tcpcliesock
    if not name.isalnum():
        print("Enter a name, not a digit")
        return
    tcpcliesock.send(json.dumps({"type":"Login","name":name}).encode('utf-8'))
    msg = json.loads(tcpcliesock.recv(BUFSIZ).decode()[5:])
    print(msg)
    if msg["type"] != 'Welcome':
        print(msg)
        return
    tcpcliesock.send(json.dumps({"type": "Start Game"}).encode('utf-8'))
    msg = json.loads(tcpcliesock.recv(BUFSIZ).decode()[5:])
    if msg['type'] != 'Login Successfull':
        print(msg)
        return
    msg = json.loads(tcpcliesock.recv(BUFSIZ).decode()[5:])
    if msg['type'] != 'Success':
        print(msg)
        return

    game_id = msg['game_id']
    board_window(game_id)

    # trying to open the board window, however failing :(
    print(":P")
    Form = QtWidgets.QWidget()
    ui = boardUi.Ui_Form()
    ui.setupUi(Form)
    Form.show()

    global popup
    popup.append(Form)


def join_game(name, id):
    global tcpcliesock
    if not name.isalnum() or not id.isdigit():
        print("Name can't be a digit and the game ID has to be a digit")
        return
    tcpcliesock.send(json.dumps({"type":"Login","name":name}).encode('utf-8'))

    msg = json.loads(tcpcliesock.recv(BUFSIZ).decode()[5:])
    print(msg)
    if msg["type"] != 'Welcome':
        print(msg)
        return
    tcpcliesock.send(json.dumps({"type": "Join Game", "game_id":eval(id)}).encode('utf-8'))
    msg = json.loads(tcpcliesock.recv(BUFSIZ).decode()[5:])
    print(msg)
    board_window(id)


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

    window = QtWidgets.QMainWindow()
    login_window = loginUI.UI_login()
    login_window.setupUi(window)
    window.show()

    login_window.start_game_btn.clicked.connect(lambda: start_game(login_window.name_entry.text()))
    login_window.join_game_btn.clicked.connect(lambda: join_game(login_window.name_entry.text(), login_window.game_id_entry.text()))

while not app.exec_():
    tcpcliesock.send(json.dumps({"type": "Logout"}).encode('utf-8'))
    tcpcliesock.close()
    sys.exit()


# get second turn
# protect or attack
# limit the number of your stones and if it gets to the maximum get rid of them
# try to get an empty hole
# check if the other player can eat your stones == check all possible outcomes
# check if he can mess up your next turn if no go for it!
# check if you can mess his turn if you can go for it!
# try to get rid off of the greatest heap at the end of your board if they are equal get rid off the closest to you stones.
# try to get rid off of the smallest heap at the start of your board
