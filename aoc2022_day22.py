"""
    Advent of Code 2022
    Day 22: Monkey Map
"""

DELTA = [(1, 0), (0, 1), (-1, 0), (0, -1)]
SIZE = 50  # unfortunately this is hard-coded


def parse_input(file_name):
    with open(file_name, "r", encoding="ascii") as data_file:
        lines = [line.rstrip("\n") for line in data_file.read().splitlines()]
    grid, path = lines[:-2], lines[-1]
    grid = [row + " " * (SIZE * 3 - len(row)) for row in grid]
    path = path.replace("R", " R ").replace("L", " L ").split()
    return grid, path


def turn(op, state):
    x, y, d = state
    match op:
        case "R":
            return x, y, (d + 1) % 4
        case "L":
            return x, y, (d + 3) % 4
        case _:
            raise ValueError


def forward(grid, move_func, state, num_steps):
    new_state = state
    while num_steps > 0:
        new_state = move_func(new_state)
        new_x, new_y, _ = new_state
        if grid[new_y][new_x] == ".":  # valid step
            state = new_state
            num_steps -= 1
        elif grid[new_y][new_x] == "#":  # wall hit
            break
    return state


def flat_wrap(state):
    x, y, d = state
    w, h = SIZE * 3, SIZE * 4
    dx, dy = DELTA[d]
    return (x + dx + w) % w, (y + dy + h) % h, d


def cube_wrap(state):
    x, y, d = state
    # see https://github.com/fogleman/AdventOfCode2022/blob/main/22.py

    FACES = [(1, 0), (2, 0), (1, 1), (0, 2), (1, 2), (0, 3)]
    # FACES layout is as follows:
    #    012
    # 0  _1_
    # 1  _23
    # 2  45_
    # 3  6

    def result(face, ij, d):
        face_x, face_y = FACES[face - 1]
        return face_x * SIZE + ij[0], face_y * SIZE + ij[1], d

    face = FACES.index((x // SIZE, y // SIZE)) + 1
    i, j = x % SIZE, y % SIZE

    ans = None

    if d == 0 and i == SIZE - 1:  # edge case right
        match face:
            case 2:  # right to left
                ans = result(5, (SIZE - 1, SIZE - j - 1), 2)
            case 3:  # right to up
                ans = result(2, (j, SIZE - 1), 3)
            case 5:  # right to left
                ans = result(2, (SIZE - 1, SIZE - j - 1), 2)
            case 6:  # right to up
                ans = result(5, (j, SIZE - 1), 3)

    if d == 1 and j == SIZE - 1:  # edge case down
        match face:
            case 2:  # down to left
                ans = result(3, (SIZE - 1, i), 2)
            case 5:  # down to left
                ans = result(6, (SIZE - 1, i), 2)
            case 6:  # down to down
                ans = result(2, (i, 0), 1)

    if d == 2 and i == 0:  # edge case left
        match face:
            case 1:  # left to right
                ans = result(4, (0, SIZE - j - 1), 0)
            case 3:  # left to down
                ans = result(4, (j, 0), 1)
            case 4:  # left to right
                ans = result(1, (0, SIZE - j - 1), 0)
            case 6:  # left to down
                ans = result(1, (j, 0), 1)

    if d == 3 and j == 0:  # edge case up
        match face:
            case 1:  # up to right
                ans = result(6, (0, i), 0)
            case 2:  # up to up
                ans = result(6, (i, SIZE - 1), 3)
            case 4:  # up to right
                ans = result(3, (0, i), 0)

    return ans if ans else (x + DELTA[d][0], y + DELTA[d][1], d)


def final_password(state):
    x, y, d = state
    return (y + 1) * 1000 + (x + 1) * 4 + d


def walk(grid, path, move_func):
    state = grid[0].index("."), 0, 0
    for op in path:
        state = (
            turn(op, state)
            if op.isupper()
            else forward(grid, move_func, state, num_steps=int(op))
        )
    return final_password(state)


def day22_part1(grid, path):
    return walk(grid, path, flat_wrap)


def day22_part2(grid, path):
    return walk(grid, path, cube_wrap)


if __name__ == "__main__":
    input_data = parse_input("data/day22.txt")

    print("Day 22 Part 1:")
    print(day22_part1(*input_data))  # Correct answer is 149250

    print("Day 22 Part 2:")
    print(day22_part2(*input_data))  # Correct answer is 12462
