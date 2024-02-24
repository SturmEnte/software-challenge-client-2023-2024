from a_star import AStar
from xml.etree.ElementTree import fromstring
from parse_xml import parseBoard
from field import Field

with open("../test/memento1.xml", "r") as msg:
    msg = msg.read()
    print("\nNEW MESSAGE:\n" + msg + "\n" + "-"*35)

    msg  = fromstring(msg)

    data = msg.find('data')
    state = data.find('state')

    boardTag = state.find('board')
    nextDirection = boardTag.attrib['nextDirection']

    board = parseBoard(boardTag, nextDirection)

    path = AStar.run(board, (0, 0, 0), (16, -26, 10))

    # visualize path
    for field in path:
        board.setField(field[0], field[1], field[2], Field("path"))
    
    board_2d = {}

    x_min = 999999
    y_min = 999999
    x_max = -999999
    y_max = -999999

    for q in board.board:
        for r in board.board[q]:
            for s in board.board[q][r]:
                x, y = board.axialToDoubleheight(q, r, s)

                if y not in board_2d:
                    board_2d[y] = {}
                board_2d[y][x] = board.board[q][r][s]

                if x > x_max:
                    x_max = x
                elif x < x_min:
                    x_min = x
                
                if y > y_max:
                    y_max = y
                elif y < y_min:
                    y_min = y
    
    out = "----------Board-----------\n"

    for y in range(y_min, y_max+1):
        for x in range(x_min, x_max+1):
            if y in board_2d:
                if x in board_2d[y]:
                    out += str(board_2d[y][x])
                    continue
            out += "  "
        out += "\n"
    
    print(out)

    print(path)