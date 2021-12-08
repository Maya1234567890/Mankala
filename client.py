from socket import *
import os
import json
from threading import Thread

board_moves = []
server = None
client = None


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
                    and strategy_board[14 - j[2]][0] != j[0] and \
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


def thread_recv_API():
    """

    """
    global client

    while 1:
        try:
            msg = eval(client.recv(BUFSIZ).decode('utf-8'))
            print(msg)
            if msg[0] == 'stop':
                print("The GUI client stopped running. Exiting...")
                # send to server quit
                os._exit(1)
            elif msg[0] == "Board request":
                if not board_moves or type(board_moves[-1]) != bool:
                    client.send("wait".encode('utf-8'))
                else:
                    client.send("->".join([str(j) for j in board_moves]).encode('utf-8'))
        except SyntaxError:
            exit()


def server_recv():
    global server, board_moves

    GUI_client_talk_thread = Thread(target=lambda: thread_recv_API(), daemon=True)
    GUI_client_talk_thread.start()
    while True:
        try:
            msg_len = eval(server.recv(5).decode().lstrip("0"))
            msg = server.recv(msg_len).decode('utf-8')
            try:
                data = json.loads(msg)
            except:  # an error in the server
                data = "server down"
                board_moves.append(True)
            print(data)

            if data["type"] == "Board Update":
                board_moves.append(" ".join([str(j) for j in data['board']]))
                # ui.turn_lbl.setText("Your Turn: " + str(data["your turn"]))
                if data["your turn"]:
                    strategy(data['board'])

            elif data["type"] == "Game Over":
                board_moves.append(data['won'])

        except OSError:
            exit()
        except (NameError, SyntaxError, TypeError):  # errors in the server
            continue


def board_window(id):
    client.send("OK".encode('utf-8'))
    print(client.recv(1024).decode('utf-8'))
    client.send(("Game ID: " + str(id)).encode('utf-8'))
    server_recv()
    """server_recv_thread = Thread(target=lambda x=ui: server_recv(x), daemon=True)
    server_recv_thread.start()"""


def start_game(name):
    """

    """
    global server

    # if not name.isalnum():
    #     client.send("Enter a name, not a digit".encode('utf-8'))
    #     return -1

    server.send(json.dumps({"type": "Login", "name": name}).encode('utf-8'))
    msg = json.loads(server.recv(BUFSIZ).decode()[5:])
    print(msg)
    if msg["type"] != 'Login Successfull':
        client.send(msg['data'].encode('utf-8'))
        return -1

    # server.send(json.dumps({"type": "Start Game"}).encode('utf-8'))
    # msg = json.loads(server.recv(BUFSIZ).decode()[5:])
    # print(msg)
    # if msg['type'] != 'Success':
    #     client.send(msg['data'].encode('utf-8'))
    #     return -1

    game_id = 0  # msg['game_id']
    board_window(game_id)
    return 0


def join_game(name, id):
    """

    """
    global server

    if not name.isalnum() or not id.isdigit():
        client.send("Name can't be a digit and the game ID has to be a digit".encode('utf-8'))
        return -1

    server.send(json.dumps({"type": "Login", "name": name}).encode('utf-8'))
    msg = json.loads(server.recv(BUFSIZ).decode()[5:])
    print(msg)
    if msg["type"] != 'Login Successfull':
        client.send(msg['data'].encode('utf-8'))
        return -1

    server.send(json.dumps({"type": "Join Game", "game_id": eval(id)}).encode('utf-8'))
    """msg = json.loads(server.recv(BUFSIZ).decode()[5:])
    print(msg, "!!!")"""
    board_window(id)
    return 0


def wait_for_API():
    """

    """
    try:
        while 1:
            data = client.recv(1024).decode('utf-8')  # waiting for commands
            data = eval(data)  # the data arrives as a list form
            print("The GUI client sent:", data)
            if data[0] == 'start':
                n = start_game(data[1])
                if n != -1: break
            elif data[0] == 'join':
                n = join_game(data[1], data[2])
                if n != -1: break
    except OSError:
        # make an exit func
        exit()


def connect_to_API():
    """
    connecting to the GUI on C#
    """
    # becoming a server
    HOST = "127.0.0.1"
    PORT = 45000
    SERVER = socket(AF_INET, SOCK_STREAM)
    ADDR = (HOST, PORT)
    SERVER.bind(ADDR)
    # waiting for the winform
    SERVER.listen(5)
    print("Waiting for connection...")
    client, client_address = SERVER.accept()
    return client, client_address


# server details
HOST = '109.66.6.106'
PORT = 45000
BUFSIZ = 1024
ADDR = (HOST, PORT)
server = socket(AF_INET, SOCK_STREAM)
server.settimeout(5)

try:  # try to connect to the server's socket.
    server.connect(ADDR)
except ConnectionRefusedError:
    print("The server is closed")
except timeout:
    print("Time ran out. Please try again later")
finally:
    server.settimeout(None)
    msg = json.loads(server.recv(BUFSIZ).decode()[5:])  # get welcome message
    print(msg)

    client, client_address = connect_to_API()  # connect to the winform
    wait_for_API()  # wait for commands from the user
