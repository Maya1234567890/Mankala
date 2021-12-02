from socket import *
import sys
import json
from threading import Thread
import loginUI
import boardUi
from PyQt5 import QtCore, QtGui, QtWidgets
from random import randint
import time

popup = []


def strategy(board):
    # if any turn can make you another turn
    for i, hole in enumerate(board[0:7]):
        if i == 0 or hole == 0: continue
        turn = i - hole  # the place where the last stone fell
        while turn < 0:
            if turn < -6: turn = turn - 1
            turn = turn + 14
        print(turn)  # the place where the last stone fell on the list board
        # another turn
        if turn == 0:
            move(i)
            return
        # a chance to steal
        if 0 < turn < 7 and board[turn] == 0:
            move(i)
            return
        # if I reach the enemy's side
        if hole > i:
            # checking the opponent's turns
            for j, op_hole in enumerate(board[8:]):
                if op_hole == 0: continue
                j = j + 8
                print(j, op_hole)
                op_turn = j - op_hole  # the place of the last stone fell
                while op_turn < 0:
                    if op_turn < -6: op_turn = op_turn - 1
                    op_turn = op_turn + 14
                print(op_turn)  # the place where the last stone fell on the list board
                # the enemy has a chance to steal from me but i can defend
                if 8 <= op_turn < 14 and board[op_turn] == 0 and (turn <= op_turn or turn <= j):
                    move(i)
                    return
                if op_turn == 7 and i <= j:
                    move(i)
                    return
    # temp
    move(randint(1, 6))
    return


    # print(board)


def move(index):
    global server
    # Make random move
    print(f"--Making a move from pit number {index}--")

    # Send Game Move message to server
    server.send(
        json.dumps({
            "type": "Game Move",
            "index": index
        }).encode('utf-8')
    )
    # temp
    time.sleep(2)

def update_board(board, ui):
    holes = ui.get_all_holes()
    for i, hole in enumerate(holes):
        hole.setText(str(board[i]))

def server_recv(ui):
    global server
    while True:
        try:
            msg_len = eval(server.recv(5).decode().strip("0"))
            # print(msg_len, 1)
            msg = server.recv(msg_len).decode('utf-8')
            # print(msg, 2)
            data = json.loads(msg)
            print(data)

            if data["type"] == "Board Update":
                # make a function to change the ui accordingly
                update_board(data['board'], ui)
                ui.turn_lbl.setText("Your Turn: " + str(data["your turn"]))
                if data["your turn"]: strategy(data['board'])

            elif data["type"] == "Notification":
                ui.opponent_lbl.setText("Game Opponent: " + data["data"][0:data["data"].index(" ")])
            elif data["type"] == "Success":
                ui.opponent_lbl.setText("Game Opponent: " + data["data"][data["data"].rfind(" "):])

                # If we got an error
            elif data["type"] == "Error":
                print(data)

                """if data["errtype"] == "Invalid Name":
                    print(data)"""

                if data["errtype"] == "Invalid Move":
                    strategy(data['board'])
                # Game over message (includes log)
            elif data["type"] == "Game Over":
                print(data)
        except OSError:
            exit()


def board_window(id):
    Form = QtWidgets.QWidget()
    ui = boardUi.Ui_Form()
    ui.setupUi(Form)
    ui.label_2.setText('Game ID: ' + str(id))
    Form.show()
    global popup
    popup.append(Form)

    server_recv_thread = Thread(target=lambda x=ui: server_recv(x), daemon=True)
    server_recv_thread.start()


def start_game(name):
    global server

    if not name.isalnum():
        print("Enter a name, not a digit")
        return
    server.send(json.dumps({"type": "Login", "name": name}).encode('utf-8'))
    msg = json.loads(server.recv(BUFSIZ).decode()[5:])
    print(msg)
    if msg["type"] != 'Login Successfull': return

    server.send(json.dumps({"type": "Start Game"}).encode('utf-8'))
    msg = json.loads(server.recv(BUFSIZ).decode()[5:])
    print(msg)
    if msg['type'] != 'Success': return

    game_id = msg['game_id']
    board_window(game_id)


def join_game(name, id):
    global server

    if not name.isalnum() or not id.isdigit():
        print("Name can't be a digit and the game ID has to be a digit")
        return

    server.send(json.dumps({"type": "Login", "name": name}).encode('utf-8'))
    msg = json.loads(server.recv(BUFSIZ).decode()[5:])
    print(msg)
    if msg["type"] != 'Login Successfull': return

    server.send(json.dumps({"type": "Join Game", "game_id": eval(id)}).encode('utf-8'))
    """msg = json.loads(server.recv(BUFSIZ).decode()[5:])
    print(msg, "!!!")"""
    board_window(id)


HOST = '109.66.6.106'
PORT = 45000
BUFSIZ = 1024
ADDR = (HOST, PORT)
server = socket(AF_INET, SOCK_STREAM)
server.settimeout(5)
app = QtWidgets.QApplication(sys.argv)

try:  # try to connect to the server's socket.
    server.connect(ADDR)
except ConnectionRefusedError:
    print("The server is closed")
except TimeoutError:
    print("Time ran out. Please try again later")
finally:
    server.settimeout(None)
    msg = json.loads(server.recv(BUFSIZ).decode()[5:])
    print(msg)

    window = QtWidgets.QMainWindow()
    login_window = loginUI.UI_login()
    login_window.setupUi(window)
    window.show()

    login_window.start_game_btn.clicked.connect(lambda: start_game(login_window.name_entry.text()))
    login_window.join_game_btn.clicked.connect(
        lambda: join_game(login_window.name_entry.text(), login_window.game_id_entry.text()))

while not app.exec_():
    server.send(json.dumps({"type": "Logout"}).encode('utf-8'))
    server.close()
    sys.exit()

# get second turn ✓
# protect or attack
# limit the number of your stones and if it gets to the maximum get rid of them
# try to get an empty hole ✓
# check if the other player can eat your stones ✓ => check all possible outcomes /
# check if he can mess up your next turn if no go for it! ✓
# check if you can mess his turn if you can go for it! ✓
# try to get rid off of the greatest heap at the end of your board if they are equal get rid off the closest to you stones.
# try to get rid off of the smallest heap at the start of your board
