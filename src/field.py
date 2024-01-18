class Field():
    def __init__(self, type, passengerDirection=None, passengers=0):
        # self.q = q
        # self.r = r
        # self.s = s
        self.type = type # can be water, passenger, island
        self.passengerDirection = passengerDirection
        self.passengers = passengers
