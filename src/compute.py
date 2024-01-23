from random import choice
from move import Move

def getPossibleMoves(state):
        pmvs = []
        if state.turn <= 7:
            return state.board.oneFishs
        if state.team == "ONE":
            positions = state.ones
        else:
            positions = state.twos
        for pos in positions:
            for direct in ((2,0),(-2,0),(1,1),(1,-1),(-1,1),(-1,-1)):
                destX = pos[0]
                destY = pos[1]
                while True:
                    destX = destX+direct[0]
                    destY = destY+direct[1]
                    if destX > 15 or destY > 7 or destX < 0 or destY < 0:
                        break
                    if state.board.getField(destX, destY) in (0,"ONE","TWO"):
                        break
                    pmvs.append((pos,(destX,destY)))
        return pmvs

def computeMove(state):
    move = Move()
    return move