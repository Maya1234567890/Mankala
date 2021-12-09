"""
Mancala Client For Competition Mode
Authors: Maya Vaksin & Mike Shlapakov
The program connects with the mancala server & the GUI winform client and runs the game via a strategy bot & board graphics
Runs on python, c# on windows
"""

from socket import *
import json
import time

# global vars
server = None
client = None


def calculate_end_hole(i, hole):
    """
    the function receives the current pit on the board and the number of marbles it has.
    the function calculates what slot will the current set of marbles end in
    it returns the place of the last slot on the board.
    """
    sum = i
    for j in range(hole):   # go over the board number of marbles times
        # skipping the sum slot for the enemy and making the user go in a circle across the board
        if (8 <= i <= 13 and sum == 1) or (1 <= i <= 6 and sum == 0):
            sum = 13
        # if it's one of the player's slots and it needs to skip the enemy's sum pit
        elif 1 <= i <= 6 and sum == 8:
            sum = 6
        else:   # the marbles simply go over normal slots
            sum = sum - 1
    print("the last ball from pit", i, "will fall in hole number", sum)
    return sum


def strategy(board):
    """
    the function receives a lost board with the current positions in the game.

    the function chooses what is the best course of action with this strategy:
    1) extra turn
    2) a chance for the player to steal marbles
    3) if the enemy can steal marbles from the player, the player trues to find a way to stop it from happening
    4) if the enemy has a chance for an extra turn, the player trues to find a way to stop it from happening
    5) taking the most amount of marbles from one of the three slots at the end
    6) taking the least amount of marbles from one of the three slots at the beginning

    the function makes a turn and returns.
    """

    strategy_board = []  # for each slot: [slot number, amount of balls in the slot, the ending slot for the game move]
    # (we know, we should have made this a dictionary)

    for i, hole in enumerate(board):
        # if the slot is the sum slot
        if i == 0 or i == 7:
            strategy_board.append(None)
            continue
        end_pit = calculate_end_hole(i, hole)  # where the last ball from the pit ends at
        strategy_board.append([i, hole, end_pit])  # save the information
    print(strategy_board)

    # if I can have another turn. this has to be done separately!
    for i in strategy_board[1:7]:  # for all the balls on the user's side
        if i[2] == 0:  # if the ball ends in the sum pit
            move(i[0])  # make a move
            return

    # seeing if the user can steal balls to his side
    for i in strategy_board[1:7]:
        if i[1] == 0: continue  # if there are no balls in the pit
        if strategy_board[i[2]][1] == 0 and strategy_board[14 - i[2]][1] != 0:
            """if the end pit for the user is empty
            if the opposite pit from the user's end pit is not empty"""
            move(i[0])
            return

        for j in strategy_board[8:14]:  # for all the balls on the enemy's side
            if j[1] == 0: continue  # skip if the pit is empty

            # if the enemy has a chance to steal from me
            if j[2] != 7 and (strategy_board[j[2]][1] == 0 or j[1] == 13) \
                    and strategy_board[14 - j[2]][0] != j[0] and \
                    (strategy_board[14 - j[2]][1] != 0 or j[1] == 13):
                """if the enemy doesn't end in his sum pit
                if the end pit for the enemy is empty/he makes one circle, coming back to his first pit which is now empty
                if the opposite pit isn't the enemy's pit, since it will be empty
                if the opposite pit isn't empty or if the enemy makes a one circle, so every slot has at least one ball
                """
                # if the user can defend itself
                if i[1] > i[0] and (i[2] <= j[2] or i[2] <= j[0]):
                    """if the user has more balls in the pit than it's index (then it will reach the enemy's side)
                    if the user's end slot is smaller than the enemy's end slot or smaller than the enemy's starting index 
                    """
                    move(i[0])
                    return

            # if the enemy has a chance for a second turn and the user can ruin it
            if i[1] > i[0] and j[2] == 7 and i[2] <= j[0]:
                """ if the user reaches the enemy's side
                if the enemy can get a second turn
                if the user's ending slot is smaller than the enemy's index
                """
                move(i[0])
                return

    # finding the max amount of marbles in a slot from the end of the board
    max = strategy_board[4][1]
    j = 4
    for i in range(4, 7):
        if strategy_board[i][1] > max:
            max = strategy_board[i][1]
            j = i
    if max != 0:
        move(j)
        return

    # finding the min amount of marbles in a slot from the beginning of the board
    min = strategy_board[1][1]
    j = 1
    for i in range(1, 4):
        if min == 0 or (strategy_board[i][1] != 0 and strategy_board[i][1] < min):
            min = strategy_board[i][1]
            j = i
    if min != 0:
        move(j)
        return


def move(index):
    """
    the function sends the server the player's move
    """
    global server
    print(f"--Making a move from pit number {index}--")

    # Send Game Move message to server
    server.send(
        json.dumps({
            "type": "Game Move",
            "index": index
        }).encode('utf-8')
    )


def server_recv():
    """
    the function forever listens to the server after a login (for competition mode).
    it talks with the GUI client and updates it about the game.
    """
    global server, client

    while True:
        try:
            msg_len = eval(server.recv(5).decode().lstrip("0"))
            msg = server.recv(msg_len).decode('utf-8')
            try:
                data = json.loads(msg)
            except json.decoder.JSONDecodeError:  # an error in the server
                # they will be times in non-competition mode when the server won't send a json type log
                data = {"type": "Game over", "won": True}  # we assume we won by not having the log
            print(data)

            if data["type"] == "Board Update":
                client.send(" ".join([str(j) for j in data['board']]).encode('utf-8'))
                time.sleep(1)  # so the GUI client won't get two messages at once
                if data["your turn"]: strategy(data['board'])  # make a move

            elif data["type"] == "Game Over":
                client.send("You won" if data["won"] else "You lose".encode('utf-8'))
                time.sleep(1)  # so the GUI client won't get two messages at once

            """In earlier versions the function also caught data types such as notification or error,
            "but in competition mode it is not needed since the server never sends those type of messages"""

        except OSError:  # the server disconnected
            exit()
        except (NameError, SyntaxError, TypeError):  # errors in the server. The client remains to listen
            continue


def board_window(id):
    """
    the function gets the game's ID
    it talks with the client before going into the game, as to set the basis for it
    """
    client.send("OK".encode('utf-8'))  # telling the GUI client the game can begin the game
    print(client.recv(1024).decode('utf-8'))  # the GUI client telling the server it's ready to begin
    client.send(("Game ID: " + str(id)).encode('utf-8'))
    server_recv()   # starting the actual gameplay


def start_game(name):
    """
    the function gets the user's name sent by the GUI client
    it makes a login with the server (competition mode) and checks for errors
    returns 0 if finds success, -1 if doesn't
    """
    global server, client

    if not name.isalnum():
        client.send("Enter a name, not a digit".encode('utf-8'))
        return -1

    server.send(json.dumps({"type": "Login", "name": name}).encode('utf-8'))
    msg = json.loads(server.recv(BUFSIZ).decode()[5:])
    print(msg)
    if msg["type"] != 'Login Successfull':
        client.send(msg['data'].encode('utf-8'))
        return -1

    # this code is only relevant for non-competition mode, to start the game manually.
    """server.send(json.dumps({"type": "Start Game"}).encode('utf-8'))
    msg = json.loads(server.recv(BUFSIZ).decode()[5:])  # sending game ID
    print(msg)
    if msg['type'] != 'Success':
        client.send(msg['data'].encode('utf-8'))
        return -1
    game_id = msg['game_id']"""

    # next, python client receives error/board update
    game_id = 0  # in competition-mode there is no real game ID
    board_window(game_id)
    return 0


def join_game(name, id):
    """
    A function that lets you join a normal (not competition mode) game.
    gets the user's name and the game's ID from the GUI client
    returns 0 if finds success, -1 if doesn't
    """
    global server, client

    if not name.isalnum() or not id.isdigit():
        # send the client the error
        client.send("Name can't be a digit and the game ID has to be a digit".encode('utf-8'))
        return -1

    server.send(json.dumps({"type": "Login", "name": name}).encode('utf-8'))
    msg = json.loads(server.recv(BUFSIZ).decode()[5:])
    print(msg)
    if msg["type"] != 'Login Successfull':
        # send the client the error
        client.send(msg['data'].encode('utf-8'))
        return -1

    server.send(json.dumps({"type": "Join Game", "game_id": eval(id)}).encode('utf-8'))
    # next, python client receives error/board update
    board_window(id)
    return 0


def wait_for_API():
    """
    Waiting for either a join game/start game command from the c# user.
    """
    try:
        while 1:
            data = client.recv(1024).decode('utf-8')  # waiting for command
            data = eval(data)  # the data arrives as a list form
            print("The GUI client sent:", data)
            if data[0] == 'start':
                n = start_game(data[1])
                if n != -1: break  # if there was no problem in the connection
            elif data[0] == 'join':
                n = join_game(data[1], data[2])
                if n != -1: break  # if there was no problem in the connection

    except OSError:  # the winform client disconnected
        exit()


def connect_to_API():
    """
    connecting to the GUI on C#
    Returning the GUI client's details
    """
    # becoming a server for the GUI
    HOST = "127.0.0.1"
    PORT = 45000
    SERVER = socket(AF_INET, SOCK_STREAM)
    ADDR = (HOST, PORT)
    SERVER.bind(ADDR)
    # waiting for the winform
    SERVER.listen(5)
    print("Waiting for connection...")
    client, client_address = SERVER.accept()  # accepting connection
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
    wait_for_API()  # wait for commands from the graphics user
