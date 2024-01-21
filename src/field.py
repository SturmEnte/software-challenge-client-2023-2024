class Field():
    def __init__(self, type, passengerDirection=None, passengers=0):
        # self.q = q
        # self.r = r
        # self.s = s
        self.type = type # can be water, passenger, island
        self.passengerDirection = passengerDirection
        self.passengers = passengers
    
    def __str__(self):
        out = "XX"
        if self.type == "water":
            out = "~~"
        elif self.type == "island":
            out = "IS"
        elif self.type == "passenger":
            out = "P" + str(self.passengers)
        return out
