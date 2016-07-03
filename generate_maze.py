# Code taken from
# http://code.activestate.com/recipes/578356-random-maze-generator/

import numpy as np
import random
from PIL import Image

# Register image display with IPython
# http://nbviewer.ipython.org/gist/deeplook/5162445
from io import BytesIO
from IPython.core import display


def display_pil_image(im):
    b = BytesIO()
    im.save(b, format='png')
    data = b.getvalue()
    ip_img = display.Image(data=data, format='png', embed=True)
    return ip_img._repr_png_()


def display_maze_and_path(maze, start, end, path, displaySize=(500, 250)):
    r = g = b = (maze * 255).astype(np.uint8)
    remappedMaze = np.empty((maze.shape[0], maze.shape[1], 3), dtype=np.uint8)
    remappedMaze[..., 0] = r
    remappedMaze[..., 1] = g
    remappedMaze[..., 2] = b
    # Display the path
    if path:
        for coord in path:
            remappedMaze[coord[0], coord[1]] = [0, 150, 255]
    # Display the start
    remappedMaze[start[0], start[1]] = [0, 255, 0]
    # Display the end
    remappedMaze[end[0], end[1]] = [255, 0, 0]
    return Image.fromarray(remappedMaze, 'RGB').resize(displaySize)


def generate_maze(width=100, height=100):
    # Code taken from
    # http://code.activestate.com/recipes/578356-random-maze-generator/

    maze = np.zeros((height, width), dtype=np.uint8)
    dx = [0, 1, 0, -1]
    dy = [-1, 0, 1, 0]  # 4 directions to move in the maze
    # start the maze from a random cell
    cx = random.randint(1, width - 2)
    cy = random.randint(1, height - 2)
    start = (cx, cy)
    maze[cy][cx] = 1
    stack = [(cx, cy, 0)]  # stack element: (x, y, direction)

    # Generate an empty maze
#     maze[1:-1, 1:-1] = 1

    # Generate a populated maze
    while len(stack) > 0:
        (cx, cy, cd) = stack[-1]
        # to prevent zigzags:
        # if changed direction in the last move then cannot change again
        if len(stack) > 2:
            if cd != stack[-2][2]:
                dirRange = [cd]
            else:
                dirRange = range(4)
        else:
            dirRange = range(4)

        # find a new cell to add
        nlst = []  # list of available neighbors
        for i in dirRange:
            nx = cx + dx[i]
            ny = cy + dy[i]
            if nx > 0 and nx < width - 1 and ny > 0 and ny < height - 1:
                if maze[ny][nx] == 0:
                    ctr = 0  # of occupied neighbors must be 1
                    for j in range(4):
                        ex = nx + dx[j]
                        ey = ny + dy[j]
                        if ex >= 0 and ex < width and ey >= 0 and ey < height:
                            if maze[ey][ex] == 1:
                                ctr += 1
                    if ctr == 1:
                        nlst.append(i)

        # if 1 or more neighbors available then randomly select one and move
        if len(nlst) > 0:
            ir = nlst[random.randint(0, len(nlst) - 1)]
            cx += dx[ir]
            cy += dy[ir]
            maze[cy][cx] = 1
            stack.append((cx, cy, ir))
        else:
            stack.pop()

    # Randomly select an ending point
    ex = ey = 0
    while maze[ey][ex] == 0:
        ex = random.randint(1, width - 2)
        ey = random.randint(1, height - 2)

    return np.array(maze, dtype=np.uint8), list(start)[::-1], (ey, ex)
