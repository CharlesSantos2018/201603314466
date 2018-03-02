import sys
import time
import getopt
import random

# Retorna os movimentos livres
def available_moves(board):
        return [k for k, v in enumerate(board) if v is '_']

def get_squares(board, player):
        return [k for k, v in enumerate(board) if v == player]

def winner(board):
    winning_combos = (
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6])

    for player in ('X', 'O'):
        positions = get_squares(board,player)
        for combo in winning_combos:
            win = True
            for pos in combo:
                if pos not in positions:
                    win = False
            if win:
                return player
        return '_'

def complete(board):
        if '_' not in [v for v in board]:
            return True
        if winner(board) != '_':
            return True
        return False

# Retorna o inimigo
def get_enemy(player):
    if player.upper() == 'X':
        return 'O'
    return 'X'

def make_move(board, position, player):
    board[position] = player

def minimax(board, player, alpha, beta):
        if complete(board):
            if winner(board) == 'x':
                return -1
            elif complete(board) == True and winner(board) is '_':
                return 0
            elif winner(board) == 'o':
                return 1
        for move in available_moves(board):
            make_move(board,move, player)
            val = minimax(board, get_enemy(player), alpha, beta)
            make_move(board,move, '_')
            if player == 'O':
                if val > alpha:
                    alpha = val
                if alpha >= beta:
                    return beta
            else:
                if val < beta:
                    beta = val
                if beta <= alpha:
                    return alpha
        if player == 'O':
            return alpha
        else:
            return beta

# Determinar o jogo
def determine(board, player):
    winners = ('-1', '0', '1')
    a = -2
    choices = []
    if len(available_moves(board)) == 9:
        return 4
    for move in available_moves(board):
        make_move(board,move, player)
        val = minimax(board, get_enemy(player), -2, 2)
        make_move(board,move, '_')
        print( "move:", move + 1, "causes:", winners[val + 1] )
        if val > a:
            a = val
            choices = [move]
        elif val == a:
            choices.append(move)
    return random.choice(choices)

def print_board(board):
    board = ''.join(board)
    if len(board) == 9:
        print("           ")
        for line in range(3):
            line_str = ''
            line_bar = ['','|','|']
            for item in board[line*3:line*3+3]:
                if item.upper() == 'X':
                    line_str += ' X ' + line_bar.pop()
                elif item.upper() == 'O':
                    line_str += ' O ' + line_bar.pop()
                else:
                    line_str += '   ' + line_bar.pop()
            print(line_str)
            if line == 2:
                print("           ")
            else:
                print("-----------")


if __name__ == "__main__":
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv,"hf:b:v",["first=","board=","verbose="])
        for opt, arg in opts:
            if opt == '-h':
                print("%s -f x -b ____x____"%(__file__))
                sys.exit()
            elif opt == '-f':
                first = arg
            elif opt in ("-v", "--verbose"):
                print_board(board)
                enemy = get_enemy(first)
                computer_move = determine(board, enemy)
                print(available_moves(board))
            elif opt in ("-b", "--board"):

                if len(arg) == 9:
                    board = list(arg)
                else:
                    print("wrong board!")




    except getopt.GetoptError:
        print("%s -f x -b ____x____"%(__file__))
        sys.exit(2)
