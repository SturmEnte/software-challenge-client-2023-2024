try:
    from colorama import Back
    GREEN = Back.GREEN
    YELLOW = Back.YELLOW
    BLACK = Back.BLACK
    RED = Back.RED
    BLUE = Back.BLUE
    LIGHTCYAN = Back.LIGHTCYAN_EX
    RESET = Back.RESET
except:
    GREEN = ""
    YELLOW = ""
    BLACK = ""
    RED = ""
    BLUE = ""
    LIGHTCYAN = ""
    RESET = ""

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
                out = LIGHTCYAN
            else:
                out = BLUE
            out += "~~"
        elif self.type == "island":
            out = GREEN + "IS"
        elif self.type == "passenger":
            out = YELLOW + "P" + str(self.passengers)
        elif self.type == "goal":
            out = BLACK + "$$"
        elif self.type == "path":                           # only for testing purposes
            out = RED + "!!"                           #
        out += RESET
        return out
