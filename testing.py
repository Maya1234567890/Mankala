board = [0, 3, 1, 1, 1, 1, 1, 0, 1, 4, 0, 4, 2, 6]
# boar= [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

def strategy(board):
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

            """if op_turn == 0:
                print("hole", j)"""
            if 8 <= op_turn < 14 and board[op_turn] == 0 and hole > i and (turn <= op_turn or turn <= j):
                print("hole", i)
                return
            if op_turn == 7 and (turn <= j):
                print("hole", i)
                return
strategy(board)