# Software Challenge 2023
# Spiel: Hey danke fuer den Fisch
#
# Spieler-Client
# board.py
#
# Mika Schiessler


class Board():
    def __init__(self):
        '''Board class'''
        self.board = {} # Structure: {q: {r: {s: fieldObject}}}
    
    def setField(self, q, r, s, field):
        if q not in self.board:
            self.board[q] = {}
        if r not in self.board[q]:
            self.board[q][r] = {}
        self.board[q][r][s] = field

    def getField(self, q, r, s):
        return self.board[q][r][s]
    
    # old
    def update(self, move, state):
        '''Updates the board using a tuple for the move: ((fromX, fromY),(toX, toY)) if startmove then (None, (toX, toY))'''
        toX, toY = move[1]
        if move[0] == None: #if it is a starting move
            self.oneFishs.remove((None,move[1]))
            if state.turn%2 and state.startTeam == "ONE" or not state.turn%2 and state.startTeam == "TWO": #if team one made the move
                self.board[toY][toX] = "ONE"
                state.ones.append(move[1])
            else: #if team two made the move
                self.board[toY][toX] = "TWO"
                state.twos.append(move[1])
        else:
            fromX, fromY = move[0]
            team = self.board[fromY][fromX]
            self.board[toY][toX] = team
            self.board[fromY][fromX] = 0
            if team == "ONE":
                state.ones.append(move[1])
                state.ones.remove(move[0])
            else:
                state.twos.append(move[1])
                state.twos.remove(move[0])
    
    def __str__(self):
        out = "\n            111111\n  0123456789012345"
        for lineCount, line in enumerate(self.board):
            out += "\n"
            out += str(lineCount)+" "
            if lineCount%2:
                out += " "
            for field in line:
                if field == None:
                    continue
                elif field == "ONE":
                    out += "\033[1;41mR\033[0m "
                elif field == "TWO":
                    out += "\033[1;44mB\033[0m "
                elif field == 0:
                    out += ". "
                else:
                    out += f"\033[1;47;30m{field}\033[0m "
        return out
