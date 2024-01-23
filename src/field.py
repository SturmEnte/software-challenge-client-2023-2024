from colorama import Back

class Field():
    def __init__(self, type, passengerDirection=None, passengers=0):
        # self.q = q
        # self.r = r
        # self.s = s
        self.type = type # can be water, passenger, island
        self.passengerDirection = passengerDirection
        self.passengers = passengers
        self.currentField = False
    
    def __str__(self):
        out = "XX"
        if self.type == "water":
            if self.currentField:
                out = Back.LIGHTCYAN_EX
            else:
                out = Back.BLUE
            out += "~~"
        elif self.type == "island":
            out = Back.GREEN + "IS"
        elif self.type == "passenger":
            out = Back.YELLOW + "P" + str(self.passengers)
        out += Back.RESET
        return out
