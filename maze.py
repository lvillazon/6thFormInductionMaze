import turtle
import random


# ---------------------------
# Maze generation
# ---------------------------

def generate_maze(n, seed=None):
    if seed is not None:
        random.seed(seed)

    # Each cell stores walls: [top, right, bottom, left]
    maze = [[[True, True, True, True] for _ in range(n)] for _ in range(n)]
    visited = [[False] * n for _ in range(n)]

    directions = [
        (-1, 0, 0, 2),  # up
        (0, 1, 1, 3),  # right
        (1, 0, 2, 0),  # down
        (0, -1, 3, 1)  # left
    ]

    # recursively carve a route through the maze
    def carve(row, col):
        visited[row][col] = True

        dirs = directions[:]
        random.shuffle(dirs)

        for dr, dc, wall, opposite in dirs:
            new_row, new_col = row + dr, col + dc

            if 0 <= new_row < n and 0 <= new_col < n and not visited[new_row][new_col]:
                maze[row][col][wall] = False
                maze[new_row][new_col][opposite] = False
                carve(new_row, new_col)

    carve(0, 0)

    # Create entrance and exit
    maze[0][0][3] = False  # left wall of start
    maze[n - 1][n - 1][1] = False  # right wall of end

    return maze


def draw_maze(maze, cell_size=25, fast=False):
    n = len(maze)

    screen = turtle.Screen()
    screen.setup(width=600, height=400, startx=0, starty=0)
    screen.title(f"{n}x{n} Random Maze")

    t = turtle.Turtle()
    t.speed(0)
    if fast:
        screen.tracer(0)

    t.hideturtle()
    t.pensize(2)

    offset = (n + 1) % 2
    start_x = -((n + offset) * cell_size) / 2
    start_y = ((n + offset) * cell_size) / 2

    def draw_line(x1, y1, x2, y2):
        t.penup()
        t.goto(x1, y1)
        t.pendown()
        t.goto(x2, y2)

    for r in range(n):
        for c in range(n):
            x = start_x + c * cell_size
            y = start_y - r * cell_size

            top, right, bottom, left = maze[r][c]

            if top:
                draw_line(x, y, x + cell_size, y)

            if right:
                draw_line(x + cell_size, y,
                          x + cell_size, y - cell_size)

            if bottom:
                draw_line(x, y - cell_size,
                          x + cell_size, y - cell_size)

            if left:
                draw_line(x, y, x, y - cell_size)

    if fast:
        screen.tracer(1)
        screen.update()


def wall_ahead():
    x, y = turtle.position()
    heading = turtle.heading() % 360

    offset = (SIZE + 1) % 2
    start_x = -((SIZE + offset) * STEP) / 2
    start_y = ((SIZE + offset) * STEP) / 2

    # Convert turtle coordinates to maze cell
    col = round((x - start_x - STEP / 2) / STEP)
    row = round((start_y - STEP / 2 - y) / STEP)

    # Determine which wall we're facing
    if heading == 0:  # east
        wall = 1
    elif heading == 90:  # north
        wall = 0
    elif heading == 180:  # west
        wall = 3
    elif heading == 270:  # south
        wall = 2
    else:
        raise ValueError("Turtle must face a cardinal direction")

    return maze[row][col][wall]


def at_exit():
    x, y = turtle.position()

    offset = (SIZE + 1) % 2
    start_x = -((SIZE + offset) * STEP) / 2
    start_y = ((SIZE + offset) * STEP) / 2

    # Start cell exit (left side)
    if (start_y - STEP <= y <= start_y and
            x < start_x):
        return True

    # End cell exit (right side)
    end_x = start_x + SIZE * STEP
    end_y = start_y - (SIZE - 1) * STEP

    if (end_y - STEP <= y <= end_y and
            x > end_x):
        return True

    return False


# ===========================================================================================
# ---------------------------
# Main
# ---------------------------
SIZE = 5  # change this to make a more complicated maze
LEVEL = 1  # change this number to get a different maze
STEP = 25  # change this to make each grid square bigger
maze = generate_maze(SIZE, LEVEL)
draw_maze(maze, cell_size=STEP, fast=True)

turtle.color("red")
turtle.pensize(3)
turtle.penup()
turtle.goto(0, 0)
turtle.pendown()

# --------------------------
# Add your code here to solve the maze


# ----------------------------
# Finish the drawing
turtle.done()
