import random


class Tic(object):
    ##VERIFICA AS POSSIBILIDADES DE VITORIA##
    winning_combos = (
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6])

    ##DEFINE OS PESOS DE DERROTA(-1), EMPATE(0) E VITORIA(1)##
    winners = ('-1', '0', '1')

    squares = []

    ##CONSTRUCTOR##
    def __init__(self, squares=[]):
        ##LIMPA O TABULEIRO##
        if len(squares) == 0:
            self.squares = ['_' for i in range(9)]
        else:
            self.squares = squares

    def show(self):
        #for element in [self.squares[i:i + 3] for i in range(0, len(self.squares), 3)]:
        #    print( element )
        board = ''.join(self.squares)
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

    ##DEFINE QUAIS OS MOVIMENTOS DISPONIVEIS##
    ##QUAL CASA AINDA ESTA VAZIA?##
    def available_moves(self):
        return [k for k, v in enumerate(self.squares) if v is '_']

    ##DEFINE QUAIS JOGADAS FINAIS ESTAO DISPOIVEIS##
    def available_combos(self, player):
        return self.available_moves() + self.get_squares(player)

    ##VERIFICA SE O JOGO ACABOU##
    def complete(self):
        if '_' not in [v for v in self.squares]:
            return True
        if self.winner() != '_':
            return True
        return False

    ##DEFINE SE X GANHOU##
    def X_won(self):
        return self.winner() == 'X'

    ##DEFINE SE 0 GANHOU##
    def O_won(self):
        return self.winner() == 'O'

    ##DEFINE O EMPATE##
    def tied(self):
        return self.complete() == True and self.winner() is '_'

    ##DEFINE O VENCEDOR##
    def winner(self):
        for player in ('X', 'O'):
            positions = self.get_squares(player)
            for combo in self.winning_combos:
                win = True
                for pos in combo:
                    if pos not in positions:
                        win = False
                if win:
                    return player
        return '_'

    ##RETORNA AS CASAS QUE PERTENCEM AO PLAYER##
    def get_squares(self, player):
        return [k for k, v in enumerate(self.squares) if v == player]

    ##FAZ O MOVIMENTO##
    def make_move(self, position, player):
        """place on square on the board"""
        self.squares[position] = player

    ##MINMAX##
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
            node.make_move(move, '_')
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

##DETERMINA SITUACAO ATUAL##
def determine(board, player):
    a = -2
    choices = []
    if len(board.available_moves()) == 9:
        return 4
    for move in board.available_moves():
        board.make_move(move, player)
        val = board.alphabeta(board, get_enemy(player), -2, 2)
        board.make_move(move, '_')
        print( "move:", move + 1, "causes:", board.winners[val + 1] )
        if val > a:
            a = val
            choices = [move]
        elif val == a:
            choices.append(move)
    return random.choice(choices)


def get_enemy(player):
    if player == 'X':
        return 'O'
    return 'X'

if __name__ == "__main__":
    board = Tic()
    board.show()

    while not board.complete():
        player = 'X'
        player_move = int(raw_input("Next Move: ")) - 1
        if not player_move in board.available_moves():
            continue
        board.make_move(player_move, player)
        board.show()

        if board.complete():
            break
        player = get_enemy(player)
        computer_move = determine(board, player)
        board.make_move(computer_move, player)
        board.show()
    print( "winner is", board.winner() )
