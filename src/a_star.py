class Node():
    possibleNeighbours = [
        (1, 0, -1),
        (1, -1, 0),
        (0, -1, 1),
        (-1, 0, 1),
        (-1, 1, 0),
        (0, 1, -1)
    ]

    def __init__(self, h_cost: int, g_cost: int, position: tuple): # h: target to node, g: start to node
        self.h = h_cost
        self.g = g_cost
        self.f = h_cost + g_cost # f_cost
        self.position = position
        self.parent = None
        
    def getNeighbours(self, board):
        neighbours = []
        for relative_coords in self.possibleNeighbours:
            absolute_coords = (self.position[0] + relative_coords[0], self.position[1] + relative_coords[1], self.position[2] + relative_coords[2])
            neighbour = board.getField(absolute_coords[0], absolute_coords[1], absolute_coords[2])
            if neighbour != False:
                neighbours.append([absolute_coords, neighbour])
        return neighbours
    
    def __eq__(self, __value: object) -> bool:
        if type(__value) != type(self):
            return False
        if self.position[0] == __value.position[0] and self.position[1] == __value.position[1]: # s coordinate can be neglected
            return True
        return False
    
    def __repr__(self) -> str:
        return f"H: {self.h}, G: {self.g}, F: {self.f}, Pos: {self.position}"

class AStar():
    def positionInNodeList(position, node_list):
        contains_node = False
        for i, node in enumerate(node_list):
            if node.position == position:
                contains_node = i
                break
        if contains_node != False:
            return contains_node
        return False

    def getDistance(pos1, pos2):
        return int((abs(pos2[0] - pos1[0]) + abs(pos2[1] - pos1[1]) + abs(pos2[2] - pos1[2])) / 2)
    
    def getPath(node):
        path = []
        
        while True:
            path.append(node.position)
            if node.parent == None:
                break
            node = node.parent        
        path.reverse()
        
        return path


    def run(board, start, target):
        open_nodes = [Node(AStar.getDistance(start, target), 0, start)]
        closed_nodes = []

        while True:
            # get node with smallest f cost
            current_node = open_nodes[0]
            current_node_index = 0
            for i, node in enumerate(open_nodes):
                if node.f < current_node.f:
                    current_node = node
                    current_node_index = i
            
            # update open and closed nodes
            open_nodes.pop(current_node_index)
            closed_nodes.append(current_node)
            
            # target found break condition
            if current_node.position == target:
                break

            # check neighbours for new nodes
            for position, neighbour_field in current_node.getNeighbours(board):
                
                # if node is an obstacle skip
                if neighbour_field.type != "water" and neighbour_field.type != "goal":
                    continue

                # if node is already closed skip
                if AStar.positionInNodeList(position, closed_nodes):
                    continue

                # create new node object
                g_cost = AStar.getDistance(position, start)
                h_cost = current_node.h + 1 # distance from field to field

                # make h_cost greater, if it is a current field
                if neighbour_field.currentField:
                    h_cost += 1
                
                # make h_cost greater, if you need to turn
                # TODO: implement rotation

                node = Node(h_cost, g_cost, position)
                node.parent = current_node
                index = AStar.positionInNodeList(position, open_nodes)
                if index != False:
                    if node.f < open_nodes[index].f:
                        open_nodes.pop(index)
                    else:
                        continue
                open_nodes.append(node)
        return AStar.getPath(current_node)