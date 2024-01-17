# Software Challenge 2023
# Spiel: Hey danke fuer den Fisch
#
# Spieler-Client
# board.py
#
# Mika Schiessler


class Board():
    def __init__(self, content):
        for i in range(32):
            content.insert(i*2, None)
        self.board = content
    def __str__(self):
        out = "  0 1 2 3 4 5 6 7"
        for count, field in enumerate(self.board):
            if field == None:
                continue
            if not count%8:
                out += "\n"+str(count/8)[0]+" "
            if count%16 == 8:
                out += " "
            if field == "ONE":
                out += "\033[1;41mR\033[0m "
            elif field == "TWO":
                out += "\033[1;44mB\033[0m "
            elif field == 0:
                out += ". "
            else:
                out += f"\033[1;47;30m{field}\033[0m "
        return out
                                              
