from move import Move
from a_star import AStar

def positionDictToTuple(position: dict) -> tuple:
    return (position["q"], position["r"], position["s"])

def computeMove(state):
    move = Move()

    # for now we just try to get as far as possible
    path = AStar.run(state.board, positionDictToTuple(state.player.position), state.board.furthestField)

    # convert path to move
    

    return move