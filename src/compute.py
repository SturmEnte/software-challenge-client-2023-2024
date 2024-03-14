# TODO: make player unable to go through opponent (not allowed)
# TODO: push action when move ends on opponent
# TODO: calculate movement points, while repecting push move
# TODO: manage coal when turning
# TODO: prevent ship from reaching speeds below 1

from move import Move
from a_star import AStar

MAX_SPEED = 4

neighboursDict = {
    (1, 0, -1): "RIGHT",
    (1, -1, 0): "UP_RIGHT",
    (0, -1, 1): "UP_LEFT",
    (-1, 0, 1): "LEFT",
    (-1, 1, 0): "DOWN_LEFT",
    (0, 1, -1): "DOWN_RIGHT"
}

vectorDifferenceDict = {
    "RIGHT": (0, 3),
    "UP_RIGHT": (1, 2),
    "UP_LEFT": (2, 1),
    "LEFT": (3, 0),
    "DOWN_LEFT": (4, 5),
    "DOWN_RIGHT": (5, 4)
}

def positionDictToTuple(position: dict) -> tuple:
    return (position["q"], position["r"], position["s"])

def getFieldVector(pos1: tuple, pos2: tuple):
    '''pos2 must be adjacent to pos1'''
    difference = (pos2[0] - pos1[0], pos2[1] - pos1[1], pos2[2] - pos1[2])
    return neighboursDict[difference]

def getVectorDifference(vec1: str, vec2: str):
    return min(abs(vectorDifferenceDict[vec1][0] - vectorDifferenceDict[vec2][0]), abs(vectorDifferenceDict[vec1][1] - vectorDifferenceDict[vec2][1]))

def computeMove(state):
    move = Move()
    coalNeeded = 0
    freeTurns = state.player.freeTurns
    movementPoints = state.player.speed

    # for now we just try to get as far as possible
    path = AStar.run(state.board, positionDictToTuple(state.player.position), state.board.farthestField)

    # convert path to move
    currentDirection = state.player.direction
    lastAdvance = 0
    # pos = state.player.getPosition()
    onCurrentField = False
    for i, field in enumerate(path[1:]):
        # TODO: check for push move
        
        # check if ship needs to turn
        fieldVector = getFieldVector(path[i], field)
        if fieldVector != currentDirection:
            move.turn(fieldVector)
            lastAdvance = 0
            onCurrentField = False

            # calculate coal needed for turn
            directionDifference = getVectorDifference(fieldVector, currentDirection)
            freeTurns -= directionDifference
            if freeTurns < 0:
                coalNeeded -= freeTurns
                freeTurns = 0
            
            currentDirection = fieldVector

        # calculate movement points for passing current fields
        if state.board.getField(field[0], field[1], field[2]).currentField:
            if not onCurrentField:
                onCurrentField = True
                movementPoints -= 2

                # dont perform move, if coal would be needed for acceleration or speed would be too high
                if movementPoints == -2 or state.player.speed - movementPoints >= MAX_SPEED:
                    movementPoints += 2
                    break
            else:
                movementPoints -= 1

        else:
            onCurrentField = False
            movementPoints -= 1

        # advance 1 / extend last advance by 1
        lastAdvance += 1
        if lastAdvance > 1:
            move.undo()
            move.advance(lastAdvance)
        else:
            move.advance(1)

        # end move if acceleration will be 1 or more OR the speed will be more than MAX_SPEED
        if movementPoints <= -1 or state.player.speed - movementPoints >= MAX_SPEED:
            break
    
    # calculate acceleration action
    acceleration = - movementPoints
    if acceleration != 0:
        move.acceleration(acceleration)

    print(f"movementPoints: {movementPoints}, freeTurns: {freeTurns}, coalNeeded: {coalNeeded}")
    print(move)

    return move