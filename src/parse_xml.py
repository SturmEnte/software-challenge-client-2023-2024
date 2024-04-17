from board import Board
from field import Field
from player import Player

def convertCoordinates(fieldArrayCount, fieldCount, direction, center):
    q = None
    r = None
    s = None

    if direction == "RIGHT":
        if fieldCount < 3:
            q = fieldArrayCount - 1 + center['q']
            r = fieldCount - 2 + center['r']
            s = 3 - fieldCount - fieldArrayCount + center['s']
        else:
            q = 1 - fieldCount + fieldArrayCount + center['q']
            r = fieldCount - 2 + center['r']
            s = 1 - fieldArrayCount + center['s']
    elif direction == "UP_RIGHT":
        if fieldCount < 3:
            r = - fieldArrayCount + 1 + center['r']
            s = - fieldCount + 2 + center['s']
            q = - 3 + fieldCount + fieldArrayCount + center['q']
        else:
            r = - 1 + fieldCount - fieldArrayCount + center['r']
            s = - fieldCount + 2 + center['s']
            q = - 1 + fieldArrayCount + center['q']
    elif direction == "DOWN_RIGHT":
        if fieldCount < 3:
            s = - fieldArrayCount + 1 + center['s']
            q = - fieldCount + 2 + center['q']
            r = - 3 + fieldCount + fieldArrayCount + center['r']
        else:
            s = - 1 + fieldCount - fieldArrayCount + center['s']
            q = - fieldCount + 2 + center['q']
            r = - 1 + fieldArrayCount + center['r']
    elif direction == "LEFT":
        if fieldCount < 3:
            q = - fieldArrayCount + 1 + center['q']
            r = - fieldCount + 2 + center['r']
            s = - 3 + fieldCount + fieldArrayCount + center['s']
        else:
            q = - 1 + fieldCount - fieldArrayCount + center['q']
            r = - fieldCount + 2 + center['r']
            s = - 1 + fieldArrayCount + center['s']
    elif direction == "DOWN_LEFT":
        if fieldCount < 3:
            r = fieldArrayCount - 1 + center['r']
            s = fieldCount - 2 + center['s']
            q = 3 - fieldCount - fieldArrayCount + center['q']
        else:
            r = 1 - fieldCount + fieldArrayCount + center['r']
            s = fieldCount - 2 + center['s']
            q = 1 - fieldArrayCount + center['q']
    elif direction == "UP_LEFT":
        if fieldCount < 3:
            s = fieldArrayCount - 1 + center['s']
            q = fieldCount - 2 + center['q']
            r = 3 - fieldCount - fieldArrayCount + center['r']
        else:
            s = 1 - fieldCount + fieldArrayCount + center['s']
            q = fieldCount - 2 + center['q']
            r = 1 - fieldArrayCount + center['r']
    # TODO: implement all other directions, and fix the above ones; only the first one actually works as intended
    return q, r, s

def getCurrentDirection(direction, nextDirection):
    if (direction == nextDirection):
        currentDirection = "STRAIGHT"
    elif (direction == "RIGHT" and nextDirection == "UP_RIGHT") or (direction == "UP_RIGHT" and nextDirection == "UP_LEFT") or (direction == "UP_LEFT" and nextDirection == "LEFT") or (direction == "LEFT" and nextDirection == "DOWN_LEFT") or (direction == "DOWN_LEFT" and nextDirection == "DOWN_RIGHT") or (direction == "DOWN_RIGHT" and nextDirection == "RIGHT"):
        currentDirection = "UP"
    else:
        currentDirection = "DOWN"
    
    return currentDirection

def parseBoard(boardTag, nextDirection):
    board = Board()

    segments = boardTag.findall('segment')

    segmentsCount = len(segments)
    board.segment_counter = segmentsCount - 1
    
    directions = []
    for segment in segments:
        board.segments.append([])
        directions.append(segment.attrib['direction'])
    directions.append(nextDirection)
    
    for segmentCount, segment in enumerate(segments):
        # direction = segment.attrib['direction']
        segmentDirection = directions[segmentCount]
        nextSegmentDirection = directions[segmentCount+1]
        currentDirection = getCurrentDirection(segmentDirection, nextSegmentDirection)
        centerTag = segment.find('center')
        center = {"q": int(centerTag.attrib['q']), "r": int(centerTag.attrib['r']), "s": int(centerTag.attrib['s'])}

        for fieldArrayCount, fieldArray in enumerate(segment.findall('field-array')):
            for fieldCount, fieldName in enumerate(fieldArray):

                fieldType = fieldName.tag
                # print(fieldType)
                # print(convertCoordinates(fieldArrayCount, fieldCount, direction, center))
                field = Field(fieldType)

                if fieldType == "passenger":
                    field.passengerDirection = fieldName.attrib['direction']
                    field.passengers = fieldName.attrib['passenger'] # maybe change to boolean
                
                # set current fields
                if fieldArrayCount in (0, 1):
                    if fieldCount == 2:
                        field.currentField = True
                elif fieldArrayCount == 2:
                    if fieldCount == 1:
                        if currentDirection == "UP":
                            field.currentField = True
                    elif fieldCount == 2:
                        if currentDirection == "STRAIGHT":
                            field.currentField = True
                    elif fieldCount == 3:
                        if currentDirection == "DOWN":
                            field.currentField = True
                elif fieldArrayCount == 3:
                    if fieldCount == 0:
                        if currentDirection == "UP":
                            field.currentField = True
                    elif fieldCount == 2:
                        if currentDirection == "STRAIGHT":
                            field.currentField = True
                    elif fieldCount == 4:
                        if currentDirection == "DOWN":
                            field.currentField = True
                
                coords = convertCoordinates(fieldArrayCount, fieldCount, segmentDirection, center)
                board.setField(coords[0], coords[1], coords[2], field)
                board.segments[segmentCount].append(((coords[0], coords[1], coords[2]), field))

                # check for farthest field
                if segmentCount == segmentsCount - 1 and fieldArrayCount == 3:
                    if field.currentField:
                        board.farthestField = coords

    return board

def parseShips(ships):
    players = []
    for ship in ships:

        player = Player(
            ship.attrib['team'],
            ship.attrib['direction'],
            int(ship.attrib['speed']),
            int(ship.attrib['coal']),
            int(ship.attrib['passengers']),
            int(ship.attrib['freeTurns']),
            int(ship.attrib['points'])
        )

        position = ship.find('position')
        player.setPosition(
            int(position.attrib['q']),
            int(position.attrib['r']),
            int(position.attrib['s'])
        )

        players.append(player)
    
    return players

def parseMementoStart(state):
    startTeam = state.attrib['startTeam']
    boardTag = state.find('board')
    nextDirection = boardTag.attrib['nextDirection']

    # parse board
    board = parseBoard(boardTag, nextDirection)
    
    # parse ships
    players = parseShips(state.findall('ship'))

    return startTeam, board, nextDirection, players

def parseMemento(state):
    boardTag = state.find('board')
    nextDirection = boardTag.attrib['nextDirection']

    # parse board (could be skipped if the board didnt change or maybe just update new parts)
    board = parseBoard(boardTag, nextDirection)

    # parse ships (could maybe be calculated from lastMove, if we want to use lastMove at all)
    players = parseShips(state.findall('ship'))

    return board, nextDirection, players

def parseResult(data, state):
    score_one = data.find('scores').findall('entry')[0]
    score_two = data.find('scores').findall('entry')[1]

    winner = data.find('winner')

    if winner.attrib['team'] == "ONE":
        team = "ONE"
        playername = score_one.find('player').attrib['name']
    else:
        team = "TWO"
        playername = score_two.find('player').attrib['name']
    
    if state.team == "ONE":
        our_score = score_one
        opponent_score = score_two
    else:
        our_score = score_two
        opponent_score = score_one

    

    regular = winner.attrib['regular']
    reason = winner.attrib['reason']

    our_stats = our_score.find('score').findall('part')
    opponent_stats = opponent_score.find('score').findall('part')
    
    csv = f'{state.startTeam},{state.team},{state.opponent.team},{team},{regular},{our_stats[0].text},{our_stats[1].text},{our_stats[2].text},{opponent_stats[0].text},{opponent_stats[1].text},{opponent_stats[2].text},{reason}'
    
    result = f'''--------------Result---------------
WINNER: {playername} (Team {team})

Regular: {regular}
Reason: {reason}

----------Player----------
Siegespunkte: {our_stats[0].text}
Punkte:       {our_stats[1].text}
Passagiere:   {our_stats[2].text}

---------Opponent---------
Siegespunkte: {opponent_stats[0].text}
Punkte:       {opponent_stats[1].text}
Passagiere:   {opponent_stats[2].text}

-----------------------------------'''

    return result, csv

def parseError(data):
    message = data.attrib['message']
    return f'---------------Error---------------\nError message from server:\n{message}\n-----------------------------------'