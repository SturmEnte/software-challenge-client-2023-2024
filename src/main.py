#!/bin/python3

from network import Connection
from state import State
from compute import computeMove
from parse_xml import parseMemento, parseMementoStart, parseResult, parseError

from xml.etree.ElementTree import fromstring, tostring
import os.path
import sys
from time import time

# Default values
host = "localhost"
port = 13050
reservation_code = None

# Check the arguments for new values
for i, arg in enumerate(sys.argv):

    if arg == "--host" or arg == "-h":
        host = sys.argv[i+1]

    elif arg == "--port" or arg == "-p":
        port = int(sys.argv[i+1])

    elif arg == "--reservation" or arg == "-r":
        reservation_code = sys.argv[i+1]

print("Host:", host)
print("Port:", port)
print("Reservation Code:", reservation_code)

conn = Connection(host=host, port=port)
conn.join(reservation_code=reservation_code)

print("Connected and joined room:", conn.roomId)

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
