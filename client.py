from socket import *
import sys
import json
from threading import Thread
import loginUI
import boardUi
from PyQt5 import QtCore, QtGui, QtWidgets
#from random import randint
import time

popup = []


def calculate_end_hole(i, hole):
    """
    :param i:
    :param hole:
    :return:
    """
    sum = i
    for j in range(hole):
        if (8 <= i <= 13 and sum == 1) or (1 <= i <= 6 and sum == 0):
            sum = 13
        elif 1 <= i <= 6 and sum == 8:
            sum = 6
        else:
            sum = sum - 1
    print("the last ball from pit", i, "will fall in hole number", sum)
    return sum


def strategy(board):
    strategy_board = []

    for i, hole in enumerate(board):
        if i == 0 or i == 7:
            strategy_board.append(None)
            continue
        end_pit = calculate_end_hole(i, hole)
        strategy_board.append([i, hole, end_pit])
    print(strategy_board)

    """if I can have another turn
    this has to be done separately"""
    for i in strategy_board[1:7]:
        if i[2] == 0:
            move(i[0])
            return

    for i in strategy_board[1:7]:
        if i[1] == 0: continue
        # if I can move the balls in the pit and the if there are balls in the pit
        if i[2] != 0 and i[2] != 7:
            # if I can steal and if it's worth to steal
            if strategy_board[i[2]][1] == 0 and strategy_board[14 - i[2]][1] != 0:
                move(i[0])
                return

        for j in strategy_board[8:14]:
            if j[1] == 0: continue
            # if the enemy has a chance to steal from me
            if j[2] != 7 and (strategy_board[j[2]][1] == 0 or j[1] == 13) \
                    and strategy_board[14 - j[2]][0] != j[0] and\
                    (strategy_board[14 - j[2]][1] != 0 or j[1] == 13):
                # if I can defend myself
                if i[1] > i[0] and (i[2] <= j[2] or i[2] <= j[0]):
                    move(i[0])
                    return

            # if the enemy has a chance for a second turn and I can ruin it
            if i[1] > i[0] and j[2] == 7 and i[2] <= j[0]:
                move(i[0])
                return

    max = strategy_board[4][1]
    j = 4
    for i in range(4, 7):
        if strategy_board[i][1] > max:
            max = strategy_board[i][1]
            j = i
    if max != 0:
        move(j)
        return

    min = strategy_board[1][1]
    j = 1
    for i in range(1, 4):
        if min == 0 or (strategy_board[i][1] != 0 and strategy_board[i][1] < min):
            min = strategy_board[i][1]
            j = i
    if min != 0:
        move(j)
        return
    # temp
"""    move(randint(1, 6))
    print("random")
    return"""

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


def update_board(board, ui):
    holes = ui.get_all_holes()
    for i, hole in enumerate(holes):
        hole.setText(str(board[i]))
        # temp
        #time.sleep(0.5)


def server_recv(ui):
    global server
    while True:
        try:
            msg_len = eval(server.recv(5).decode().lstrip("0"))
            # print(msg_len, 1)
            msg = server.recv(msg_len).decode('utf-8')
            # print(msg, 2)
            data = json.loads(msg)
            print(data)
            """# Get message length
            msg_length = int(server.recv(5))

            # Receive message
            data = json.loads(server.recv(msg_length))
            print(data)"""

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
                if data["won"]:
                    print("WON!")
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
# protect or attack ✓/
# limit the number of your stones and if it gets to the maximum get rid of them ✓
# try to get an empty hole ✓
# check if the other player can eat your stones ✓ => check all possible outcomes /
# check if he can mess up your next turn if no go for it! ✓
# check if you can mess his turn if you can go for it! ✓
# try to get rid off of the greatest heap at the end of your board if they are equal get rid off the closest to you stones. ✓
# try to get rid off of the smallest heap at the start of your board ✓
