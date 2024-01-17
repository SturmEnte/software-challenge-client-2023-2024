# Software Challenge 2023
# Spiel: Hey danke fuer den Fisch
#
# Spieler-Client
# parse_xml.py
#
# Mika Schiessler


def parseMementoBoard(state):
    startTeam = state.find('startTeam').text
    fishes = []
    for i in state.find('fishes').findall('int'):
        fishes.append(int(i.text))
    board = []
    for a in state.find('board').findall('list'):
        line = []
        for b in a.findall('field'):
            if b.text in ("ONE", "TWO"):
                line.append(b.text)
            else:
                line.append(int(b.text))
        board.append(line)
    return startTeam, board, fishes

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
