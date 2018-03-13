import random
import sys
import time
import getopt


class Tic(object):
    winning_combos = (
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6])

    winners = ('-1', '0', '1')

    squares = []

    #def __init__(self, squares=[]):
    #    if len(squares) == 0:
    #        self.squares = [None for i in range(9)]
    #    else:
    #        self.squares = squares

    def show(self):
        temp = noneToUnder(self.squares)
        for element in [temp[i:i + 3] for i in range(0, len(temp), 3)]:
            print element
        self.squares = underToNone(temp)

    def available_moves(self):
        """what spots are left empty?"""
        return [k for k, v in enumerate(self.squares) if v is None]

    def available_combos(self, player):
        """what combos are available?"""
        return self.available_moves() + self.get_squares(player)

    def complete(self):
        """is the game over?"""
        if None not in [v for v in self.squares]:
            return True
        if self.winner() != None:
            return True
        return False

    def X_won(self):
        return self.winner() == 'x'

    def O_won(self):
        return self.winner() == 'o'

    def tied(self):
        return self.complete() == True and self.winner() is None

    def winner(self):
        for player in ('x', 'o'):
            positions = self.get_squares(player)
            for combo in self.winning_combos:
                win = True
                for pos in combo:
                    if pos not in positions:
                        win = False
                if win:
                    return player
        return None

    def get_squares(self, player):
        """squares that belong to a player"""
        return [k for k, v in enumerate(self.squares) if v == player]

    def make_move(self, position, player):
        """place on square on the board"""
        self.squares[position] = player

    def alphabeta(self, node, player, alpha, beta):
        if node.complete():
            if node.X_won():
                return -1
            elif node.tied():
                return 0
            elif node.O_won():
                return 1
        for move in node.available_moves():
            node.make_move(move, player)
            val = self.alphabeta(node, get_enemy(player), alpha, beta)
            node.make_move(move, None)
            if player == 'o':
                if val > alpha:
                    alpha = val
                if alpha >= beta:
                    return beta
            else:
                if val < beta:
                    beta = val
                if beta <= alpha:
                    return alpha
        if player == 'o':
            return alpha
        else:
            return beta


def determine(board, player):
    a = -2
    choices = []
    if len(board.available_moves()) == 9:
        return 4
    for move in board.available_moves():
        board.make_move(move, player)
        val = board.alphabeta(board, get_enemy(player), -2, 2)
        board.make_move(move, None)
        #print "move:", move + 1, "causes:", board.winners[val + 1]
        if val > a:
            a = val
            choices = [move]
        elif val == a:
            choices.append(move)
    return random.choice(choices)


def get_enemy(player):
    if player == 'x':
        return 'o'
    return 'x'


def noneToUnder(board):
    temp = board
    for index, t in enumerate(temp):
        if t is None:
            temp[index] = "_"
    return temp


def underToNone(board):
    temp = board
    for index, t in enumerate(temp):
        if t is "_":
            temp[index] = None
    return temp


def upper(board):
    for index, b in enumerate(board):
        board[index] = b.upper()
    return board

def print_board(board):
    temp = ""
    for b in board:
        temp = temp + b
    print temp

if __name__ == "__main__":
    argv = sys.argv[1:]
    boards = Tic()

    try:
        opts, args = getopt.getopt(argv,"hf:b:v",["first=","board=","verbose="])
        for opt, arg in opts:
            if opt == '-h':
                print("%s -f x -b ____x____"%(__file__))
                sys.exit()
            elif opt in ("-v", "--verbose"):
                boards.show()
            elif opt in ("-b", "--board"):
                if len(arg) == 9:
                    board = list(arg)
                    boards.squares = underToNone(board)
                else:
                    print("wrong board!")
            elif opt in ("-f", "--first"):
                player1 = arg

        player = player1
        player = get_enemy(player)
        computer_move = determine(boards, player)
        boards.make_move(computer_move, player)
        print ""
        print_board(noneToUnder(boards.squares))
        print ""

        #while not boards.complete():
        #    player = player1
        #    player_move = int(raw_input("Next Move: ")) - 1
        #    if not player_move in boards.available_moves():
        #        continue
        #    boards.make_move(player_move, player)
        #    boards.show()
        #    if boards.complete():
        #        break
        #    player = get_enemy(player)
        #    computer_move = determine(boards, player)
        #    boards.make_move(computer_move, player)
        #    boards.show()
        #print "winner is", board.winner()

    except getopt.GetoptError:
        print("%s -f x -b ____x____"%(__file__))
        sys.exit(2)
