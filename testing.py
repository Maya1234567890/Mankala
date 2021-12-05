board = [0, 6, 3, 4, 0, 0, 3, 0, 8, 17, 0, 3, 2, 1]
# boar= [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

"""def strategy(board):
    # if any turn can make you another turn
    for i, hole in enumerate(board[0:7]):
        if i == 0 or hole == 0: continue
        print(i, hole)
        turn = i-hole # te place of the last stone fell
        while turn<0:
            if turn<-6: turn = turn-1
            turn = turn + 14
        print("sof tor",turn)
        if turn == 0:
            print("hole",i)
            return
        if 0<turn<7 and board[turn] == 0:
            print("hole",i)
            return

        #ליריב יש הזדמנות לגנוב ממני כדורים
        for j, op_hole in enumerate(board[8:]):
            if op_hole == 0: continue
            j = j + 8
            print(j, op_hole)
            op_turn = j - op_hole  # te place of the last stone fell
            while op_turn < 0:
                if op_turn < -6: op_turn = op_turn - 1
                op_turn = op_turn+14
            print("sof tor yariv", op_turn)

            if op_turn == 0:
                print("hole", j)
            if 8 <= op_turn < 14 and board[op_turn] == 0 and hole > i and (turn <= op_turn or turn <= j):
                print("hole", i)
                return
            if op_turn == 7 and (turn <= j):
                print("hole", i)
                return"""


def calculate_end_hole(i, hole):
    """
    :param i:
    :param hole:
    :return:
    """
    sum = i
    for j in range(hole):
        if (8<=i<=13 and sum == 1) or (1<=i<=6 and sum == 0):
            sum = 13
        elif 1<=i<=6 and sum == 8:
            sum = 6
        else:
            sum = sum - 1
    print("the last ball from pit", i, "will fall in hole number", sum)
    return sum

    """if 8<=i<=13 and sum != 1: sum = sum - 1
        if 8 <= i <= 13 and sum == 1: sum = sum = 13
        if 1<=i<=7
        
    turn = i - hole  # the place where the last stone fell
    while turn < 0:
        if turn < -6: turn = turn - 1
        turn = turn + 14
    # the place where the last stone fell on the list board
    print("the last ball from pit", i, "will fall in hole number", turn)
    return turn"""


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
            print(i[0])
            return

    for i in strategy_board[1:7]:
        if i[1] == 0: continue
        # if I can move the balls in the pit and the if there are balls in the pit
        if i[2] != 0 and i[2] != 7:
            # if I can steal and if it's worth to steal
            if strategy_board[i[2]][1] == 0 and strategy_board[14 - i[2]][1] != 0:
                print(i[0])
                return

        for j in strategy_board[8:14]:
            if j[1] == 0: continue
            # if the enemy has a chance to steal from me
            if j[2] != 7 and (strategy_board[j[2]][1] == 0 or j[0] == j[2]) and strategy_board[14 - j[2]][1] != 0:
                # if I can defend myself
                if i[1] > i[0] and (i[2] <= j[2] or i[2] <= j[0]):
                    print(i[0])
                    return

            # if the enemy has a chance for a second turn and I can ruin it
            if i[1] > i[0] and j[2] == 7 and i[2] <= j[0]:
                print(i[0])
                return

    max = strategy_board[4][1]
    j = 4
    for i in range (4, 7):
        if strategy_board[i][1] > max:
            max = strategy_board[i][1]
            j = i
    if max != 0:
        print(j)
        return

    min = strategy_board[1][1]
    j = 1
    for i in range(1, 4):
        if min == 0 or (strategy_board[i][1] != 0 and strategy_board[i][1] < min):
            min = strategy_board[i][1]
            j = i
    if min != 0:
        print(j)
        return

strategy(board)