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
            out = "S1"
        else:
            out = "S2"
        
        return out