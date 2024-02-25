class Move():
    def __init__(self):
        self.actions = []
    
    def advance(self, distance: int):
        '''Advance in the current direction by given number of fields.'''
        self.actions.append(f'<advance distance="{distance}" />')
        
    def turn(self, direction: str):
        '''The direction you want to turn to.'''
        self.actions.append(f'<turn direction="{direction}" />')
    
    def acceleration(self, acc: int):
        '''Change the current speed by given number. Can be positive or negative. 1 or -1 don't cost any coal (per move). Only use once per move; will be at the top of the actions list.'''
        self.actions = [f'<acceleration acc="{acc}" />'] + self.actions
    
    def push(self, direction: str):
        '''The direction you want to push the opponent, if you get onto the same field.'''
        self.actions.append(f'<push direction="{direction}" />')
    
    def undo(self):
        '''removes the last action from the move'''
        self.actions.pop(-1)
    
    def __repr__(self) -> str:
        out = "<actions>\n"
        for action in self.actions:
            out += "    " + action + "\n"
        out += "</actions>"
        return out