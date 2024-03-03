from network import Connection
from state import State
from compute import computeMove
from parse_xml import parseMemento, parseMementoStart, parseResult, parseError
from xml.etree.ElementTree import fromstring, tostring
import os.path

from time import time

conn = Connection()
conn.join()

while True:
    msgList = conn.recvGameplay()
    for msg in msgList:
        # print("\nNEW MESSAGE:\n" + tostring(msg).decode("utf-8") + "\n" + "-"*35)
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
            result, csv = parseResult(data, state)
            print(result)
            if os.path.isfile("../test/result.csv"):
                with open("../test/result.csv", "a") as f:
                    f.write("\n"+csv)
            exit()
        elif msgType == "error":
            print(parseError(data))
        else:
            print("ERROR! UNKNOWN MESSAGE: "+msgType)
