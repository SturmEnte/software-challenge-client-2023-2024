from parse_xml import parseMementoStart # parseMementoStart is imported, because it also returns the start team
from time import time
from state import State
from xml.etree.ElementTree import fromstring
from compute import computeMove

with open("../test/memento2.xml", "r") as msg:
    msg = msg.read()
    print("\nNEW MESSAGE:\n" + msg + "\n" + "-"*35)

    msg  = fromstring(msg)

    data = msg.find('data')
    msgType = data.attrib['class']
    
    t1 = time()
    xmlState = data.find('state')
    turn = int(xmlState.attrib['turn'])

    startTeam, board, nextDirection, players = parseMementoStart(xmlState)
    state = State("TWO", turn, startTeam, board, nextDirection, players)

    move = computeMove(state)

    t2 = time()
    print(f"Zeit: {t2-t1}   Zug: {turn}")
    state.printState()
    print(move)