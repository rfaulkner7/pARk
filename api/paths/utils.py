import numpy as np
from PIL import Image


def getDist(tup1, tup2):
    result = (tup1[0] - tup2[0])**2 + (tup1[1] - tup2[1]) ** 2
    return result


class Node:

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def return_path(current_node, maze):
    path = []
    no_rows, no_columns = np.shape(maze)
    result = [[-1 for i in range(no_columns)] for j in range(no_rows)]
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent
    path = path[::-1]
    start_value = 0
    for i in range(len(path)):
        result[path[i][0]][path[i][1]] = start_value
        start_value += 1
    return result


def search(maze, cost, start, end):

    start_node = Node(None, tuple(start))
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, tuple(end))
    end_node.g = end_node.h = end_node.f = 0

    yet_to_visit_list = []
    visited_list = []

    yet_to_visit_list.append(start_node)

    outer_iterations = 0
    max_iterations = (len(maze) // 2) ** 10

    move = [[-1, 0],  # go up
            [1, 0],  # go down
            [0, -1],  # go left
            [0, 1]]  # go right

    no_rows, no_columns = np.shape(maze)

    while len(yet_to_visit_list) > 0:

        outer_iterations += 1

        current_node = yet_to_visit_list[0]
        current_index = 0
        for index, item in enumerate(yet_to_visit_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        if outer_iterations > max_iterations:
            return return_path(current_node, maze)

        yet_to_visit_list.pop(current_index)
        visited_list.append(current_node)

        if current_node == end_node:
            return return_path(current_node, maze)

        children = []

        for new_position in move:

            node_position = (
                current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            if (node_position[0] > (no_rows - 1) or
                node_position[0] < 0 or
                node_position[1] > (no_columns - 1) or
                    node_position[1] < 0):
                continue

            if maze[node_position[0]][node_position[1]] != 0:
                continue

            new_node = Node(current_node, node_position)

            children.append(new_node)

        for child in children:

            if len([visited_child for visited_child in visited_list if visited_child == child]) > 0:
                continue

            child.g = current_node.g + cost
            child.h = (((child.position[0] - end_node.position[0]) ** 2) +
                       ((child.position[1] - end_node.position[1]) ** 2))

            child.f = child.g + child.h

            if len([i for i in yet_to_visit_list if child == i and child.g > i.g]) > 0:
                continue

            yet_to_visit_list.append(child)


def convert(arr):
    start = 0
    startCount = 0
    endlist = []
    mazeList = np.zeros(arr.shape[:2])
    end = 0
    currDist = 0
    for i in range(0, len(arr)):
        # print("")
        for j in range(0, len(arr[0])):
            if arr[i][j][1] < arr[i][j][2] and arr[i][j][0] < arr[i][j][2]:
                # print("w", end=" ")
                mazeList[i][j] = 1
                if(i > 0):
                    mazeList[i-1][j] = 1
                if(i + 1 < len(mazeList)):
                    mazeList[i+1][j] = 1
                if(j > 0):
                    mazeList[i][j-1] = 1
                if(j + 1 < len(mazeList[0])):
                    mazeList[i][j+1] = 1
                # if(i-1 > 0):
                #     mazeList[i-2][j] = 1
                # if(i + 2 < len(mazeList)):
                #     mazeList[i+2][j] = 1
                # if(j-1 > 0):
                #     mazeList[i][j-2] = 1
                # if(j + 2 < len(mazeList[0])):
                #     mazeList[i][j+2] = 1
            elif arr[i][j][2] < 50 and arr[i][j][0] < 50 and arr[i][j][1] < 50:
                if (startCount % 2 == 1):
                    start = (i, j)
                startCount += 1
                # print("s", end=" ")
            elif arr[i][j][2] < 100 and arr[i][j][0] > 200 and arr[i][j][1] < 100:
                # print("e", end=" ")
                endlist.append((i, j))
            else:
                # print(" ", end=" ")
                continue
    # print("")
    # print("")
    # print("")
    for i in endlist:
        if (currDist == 0 or getDist(start, i) < currDist):
            end = i
            currDist = getDist(start, i)
    # print(start)
    # print(end)
    path = search(mazeList, 1, start, end)
    # print(path)
    # for i in range(0, len(path)):
    #     print("")
    #     for j in range(0, len(path[0])):
    #         if(path[i][j] != -1):
    #             print("1", end="")
    #         else:
    #             print("0", end="")
    curr = start
    directions = ""
    running = True
    while(running):
        x = curr[0]
        y = curr[1]
        currVal = path[x][y]
        if(path[x+1][y] == currVal + 1):
            directions = directions+"S"
            curr = (x+1, y)
        elif(path[x-1][y] == currVal + 1):
            directions = directions + "N"
            curr = (x-1, y)
        elif(path[x][y-1] == currVal + 1):
            directions = directions + "W"
            curr = (x, y-1)
        elif(path[x][y+1] == currVal + 1):
            directions = directions + "E"
            curr = (x, y+1)
        else:
            running = False
    return(directions)
