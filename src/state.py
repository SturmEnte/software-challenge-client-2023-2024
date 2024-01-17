from board import Board

class State():
    def __init__(self, team, turn, startTeam, board, fishes):
        self.team = team
        self.turn = turn
        self.startTeam = startTeam
        self.board = Board(board)
        self.fishes = fishes
        self.ones = []
        self.twos = []
    
    def setData(self, turn, fishes, lastMove):
        '''Updates all variable state values'''
        self.turn = turn
        self.fishes = fishes
        self.board.update(lastMove, self)
    
    def printBoard(self):
        print(self.board)
