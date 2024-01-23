from network import Connection
from state import State
from compute import computeMove
from parse_xml import parseMemento, parseMementoStart, parseResult
from xml.etree.ElementTree import fromstring, tostring

from time import time

conn = Connection()
conn.join()

while True:
    msgList = conn.recvGameplay()
    for msg in msgList:
        print("\nNEW MESSAGE:\n" + tostring(msg).decode("utf-8") + "\n" + "-"*35)
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
                startTeam, board, nextDirection, players = parseMementoStart(xmlState)
                state = State(conn.team, turn, startTeam, board, nextDirection, players)
            else:
                board, nextDirection, players = parseMemento(xmlState)
                state.setData(turn, board, nextDirection, players)
            t2 = time()
            print(f"Zeit: {t2-t1}   Zug: {turn}")
            state.printState()
        elif msgType == "welcomeMessage":
            conn.team = data.attrib['color']
        elif msgType == "result":
            print(parseResult(data, state.fishes))
            exit()
        else:
            print("ERROR! UNKNOWN MESSAGE: "+msgType)
