# TODO: manage coal when turning
# TODO: prevent ship from reaching speeds below 1

from move import Move
from random import choice
from a_star import AStar, Node

MAX_SPEED = 4

neighboursDict = {
    (1, 0, -1): "RIGHT",
    (1, -1, 0): "UP_RIGHT",
    (0, -1, 1): "UP_LEFT",
    (-1, 0, 1): "LEFT",
    (-1, 1, 0): "DOWN_LEFT",
    (0, 1, -1): "DOWN_RIGHT"
}

neighboursDictReversed = {
    "RIGHT": (1, 0, -1),
    "UP_RIGHT": (1, -1, 0),
    "UP_LEFT": (0, -1, 1),
    "LEFT": (-1, 0, 1),
    "DOWN_LEFT": (-1, 1, 0),
    "DOWN_RIGHT": (0, 1, -1)
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

def getPossibleMoves(state):
    min_speed = state.player.speed - 1
    if min_speed < 1:
        min_speed = 1
    
    max_speed = state.player.speed + 1
    if max_speed > MAX_SPEED:
        max_speed = MAX_SPEED
    
    pmvs = getPossibleMovesRecursive(state.player.getPosition(), state.player.direction, state.player.coal, state.player.freeTurns, min_speed, max_speed)

    return pmvs

def getPossibleMovesRecursive(position, direction, coal, free_turns, min_speed, max_speed):
    node = Node(0, 0, position)
    for pos, field in node.getNeighbours():
        if field.type != "water":
            continue

        field_vector = getFieldVector(position, pos)
        if field_vector != direction:
            free_turns -= getVectorDifference(direction, field_vector)
            if free_turns < 0:
                coal -= free_turns
                free_turns = 0
                

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

        # check for push move
        doPushMove = False
        if state.opponent.getPosition() == field:
            doPushMove = True
        # TODO: check when pushmove could be left out to save 1 coal

        # advance 1 / extend last advance by 1
        lastAdvance += 1
        if lastAdvance > 1:
            move.undo()
            move.advance(lastAdvance)
        else:
            move.advance(1)

        # perform push move
        if doPushMove:
            lastAdvance = 0
            movementPoints -= 1
            node = Node(0, 0, state.opponent.getPosition())
            direction = "LEFT"
            directionFound = False
            for position, neighbour_field in node.getNeighbours(state.board):
                   
                # if field is not an obstacle
                if neighbour_field.type != "water":
                    continue
                    
                # if we wont traverse this field in the future
                if position in path[i:]:
                    continue
                    
                # if this isn't the field behind the opponent (against the rules)
                # relative_coords = neighboursDictReversed[state.opponent.direction]
                # pos = state.player.getPosition()
                # if position == (-relative_coords[0] + pos[0], -relative_coords[1] + pos[1], -relative_coords[2] + pos[2]):
                #     continue
                if position == state.player.getPosition():
                    continue

                direction = getFieldVector(state.opponent.getPosition(), position)
                directionFound = True
                break

            # if no field is suitable, use a field that will be in our path
            if not directionFound:
                for position, neighbour_field in node.getNeighbours(state.board):
                    
                    # if field is not an obstacle
                    if neighbour_field.type != "water":
                        continue
                        
                    # if this isn't the field behind the opponent (against the rules)
                    # relative_coords = neighboursDictReversed[state.opponent.direction]
                    # pos = state.player.getPosition()
                    # if position == (-relative_coords[0] + pos[0], -relative_coords[1] + pos[1], -relative_coords[2] + pos[2]):
                    #     continue
                    if position == state.player.getPosition():
                        continue

                    direction = getFieldVector(state.opponent.getPosition(), position)
                    directionFound = True
                    break

            move.push(direction)

        # end move if acceleration will be 1 or more OR the speed will be more than MAX_SPEED
        if movementPoints <= -1 or state.player.speed - movementPoints >= MAX_SPEED:
            break
    
    # calculate acceleration action
    acceleration = -movementPoints
    if acceleration != 0:
        move.acceleration(acceleration)
        coalNeeded += abs(acceleration) - 1
    
    # check if move is possible
    move_possible = True

    # check for minimum speed
    if state.player.speed - acceleration < 1 or len(path) <= 1:
        move_possible = False
    
    # check for coal requirement
    elif coalNeeded < state.player.coal:
        move_possible = False

    if not move_possible:
        move = getPossibleMoves(state).choice()
    
    print(f"movementPoints: {movementPoints}, freeTurns: {freeTurns}, coalNeeded: {coalNeeded}")
    print(move)

    return move