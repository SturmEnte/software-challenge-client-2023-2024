class State():
    def __init__(self, team, turn, startTeam, board, nextDirection, players):
        self.team = team
        self.turn = turn
        self.startTeam = startTeam
        self.board = board
        self.nextDirection = nextDirection

        if players[0].team == self.team:
            self.player = players[0]
            self.opponent = players[1]
        else:
            self.player = players[1]
            self.opponent = players[0]
    
    def setData(self, turn, board, nextDirection, players):
        '''Updates all variable state values'''
        self.turn = turn
        self.nextDirection = nextDirection
        self.board = board
        
        if players[0].team == self.team:
            self.player = players[0]
            self.opponent = players[1]
        else:
            self.player = players[1]
            self.opponent = players[0]
    
    def printBoard(self):
        board_2d = {}

        x_min = 999999
        y_min = 999999
        x_max = -999999
        y_max = -999999

        player_xy = self.board.axialToDoubleheight(
            self.player.position['q'],
            self.player.position['r'],
            self.player.position['s']
        )
        opponent_xy = self.board.axialToDoubleheight(
            self.opponent.position['q'],
            self.opponent.position['r'],
            self.opponent.position['s']
        )

        for q in self.board.board:
            for r in self.board.board[q]:
                for s in self.board.board[q][r]:
                    x, y = self.board.axialToDoubleheight(q, r, s)

                    if y not in board_2d:
                        board_2d[y] = {}
                    board_2d[y][x] = self.board.board[q][r][s]

                    if x > x_max:
                        x_max = x
                    elif x < x_min:
                        x_min = x
                    
                    if y > y_max:
                        y_max = y
                    elif y < y_min:
                        y_min = y
        
        out = "----------Board-----------\n"

        for y in range(y_min, y_max+1):
            for x in range(x_min, x_max+1):
                if y in board_2d:
                    if x in board_2d[y]:
                        if player_xy == (x, y):
                            out += str(self.player)
                            continue
                        elif opponent_xy == (x, y):
                            out += str(self.opponent)
                            continue
                        out += str(board_2d[y][x])
                        continue
                out += "  "
            out += "\n"
        
        print(out)
    
    def printPlayer(self, printOwnPlayer=True):
        player = None

        if printOwnPlayer:
            player = self.player
        else:
            player = self.opponent

        out = f"""
----------Player----------
Team:       {player.team}
Position:   q: {player.position['q']}, r: {player.position['r']}, s: {player.position['s']}
Direction:  {player.direction}
Speed:      {player.speed}
Coal:       {player.coal}
Passengers: {player.passengers}
Free Turns: {player.freeTurns}
Points:     {player.points}
"""

        print(out)

    def printState(self):
        print("---------------State---------------\n")
        self.printBoard()
        self.printPlayer()
        self.printPlayer(False)
        print("-----------------------------------")
    
    def printBoardSegments(self):
        for i, segment in enumerate(self.board.segments):
            print(f"SEGMENT {i}:")
            for field in segment:
                print(f"    {field[1].type}")