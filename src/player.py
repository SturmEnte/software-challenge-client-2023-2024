try:
    from colorama import Back
    RED = Back.RED
    RESET = Back.RESET
except:
    RED = ""
    RESET = ""

class Player():
    def __init__(self, team, direction, speed, coal, passengers, freeTurns, points):
        self.team = team
        self.direction = direction
        self.speed = speed
        self.coal = coal
        self.passengers = passengers
        self.freeTurns = freeTurns
        self.points = points
        self.position = {}
    
    def setPosition(self, q, r, s):
        self.position['q'] = q
        self.position['r'] = r
        self.position['s'] = s
    
    def getPosition(self):
        return self.position['q'], self.position['r'], self.position['s']
    
    def __str__(self):
        out = ""

        if self.team == "ONE":
            out = RED + "S1"
        else:
            out = RED + "S2" # dont know what color to use, as background is already blue
        
        out += RESET
        return out