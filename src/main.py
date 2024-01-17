# Software Challenge 2023
# Spiel: Hey danke fuer den Fisch
#
# Spieler-Client
# main.py
#
# Mika Schiessler


from network import Connection
from state import State
from compute import computeMove
from parse_xml import parseMemento, parseMementoBoard, parseResult
from xml.etree.ElementTree import fromstring

from time import time

conn = Connection()
conn.join()

while True:
    msgList = conn.recvGameplay()
    for msg in msgList:
        data = msg.find('data')
        msgType = data.attrib['class']
        if msgType == "moveRequest":
            move = computeMove(state)
            conn.sendMove(move)
        elif msgType == "memento":
            t1 = time()
            xmlState = data.find('state')
            turn = int(xmlState.attrib['turn'])
            if turn == 0:
                startTeam, board, fishes = parseMementoBoard(xmlState)
                state = State(conn.team, turn, startTeam, board, fishes)
            else:
                fishes, lastMove = parseMemento(xmlState)
                state.setData(turn, fishes, lastMove)
            t2 = time()
            print(f"Zeit: {t2-t1}   Zug: {turn}")
            state.printBoard()
        elif msgType == "welcomeMessage":
            conn.team = data.attrib['color']
        elif msgType == "result":
            print(parseResult(data, state.fishes))
            exit()
        else:
            print("ERROR! UNKNOWN MESSAGE: "+msgType)
