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
        pass
    elif direction == "DOWN_RIGHT":
        pass

    return q, r, s

def parseMementoBoard(state):
    startTeam = state.attrib['startTeam']
    boardTag = state.find('board')
    nextDirection = boardTag.attrib['nextDirection']
    board = Board()

    # parse board
    for segment in boardTag.findall('segment'):
        direction = segment.attrib['direction']
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
                
                coords = convertCoordinates(fieldArrayCount, fieldCount, direction, center)
                board.setField(coords[0], coords[1], coords[2], field)
    
    # parse ships
    players = []
    for ship in state.findall('ship'):

        player = Player(
            ship.attrib['team'],
            ship.attrib['direction'],
            ship.attrib['speed'],
            ship.attrib['coal'],
            ship.attrib['passengers'],
            ship.attrib['freeTurns'],
            ship.attrib['points']
        )

        position = ship.find('position')
        player.setPosition(
            int(position.attrib['q']),
            int(position.attrib['r']),
            int(position.attrib['s'])
        )

        players.append(player)

    return startTeam, board, nextDirection, players

def parseMemento(state):
    fishes = []
    for i in state.find('fishes').findall('int'):
        fishes.append(int(i.text))
    lastMove = state.find('lastMove')
    fr = lastMove.find('from')
    to = lastMove.find('to')
    if fr != None:
        fr = (int(fr.attrib['x']), int(fr.attrib['y']))
    to = (int(to.attrib['x']), int(to.attrib['y']))
    lastMove = (fr, to)
    return fishes, lastMove

def parseResult(data, fishes):
    if data.find('winner').attrib['team'] == "ONE":
        team = "1"
        color = "\033[31m"
        playername = data.find('scores').findall('entry')[0].find('player').attrib['name']
    else:
        team = "2"
        color = "\033[34m"
        playername = data.find('scores').findall('entry')[1].find('player').attrib['name']
    
    return f'\n\n\033[1mGEWINNER: {color}{playername} (Team {team})\033[0m\n\033[1mFISCHE: {fishes[0]}:{fishes[1]}'
