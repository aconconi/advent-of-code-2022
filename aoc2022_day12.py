"""
    Advent of Code 2022
    Day 12:
"""

from collections import deque

import pytest

DELTA = {(0, 1), (0, -1), (-1, 0), (1, 0)}

TRANS_ELEV = str.maketrans("SE", "az")


def neighbors(grid, current):
    r, c = current
    yield from ((nr, nc) for dr, dc in DELTA if (nr := r + dr, nc := c + dc) in grid)


def can_step_uphill(current_h, neigh_h):
    return (
        ord(neigh_h.translate(TRANS_ELEV)) - ord(current_h.translate(TRANS_ELEV)) <= 1
    )


def can_step_downhill(current_h, neigh_h):
    return (
        ord(neigh_h.translate(TRANS_ELEV)) - ord(current_h.translate(TRANS_ELEV)) >= -1
    )


def parse_input(file_name):
    with open(file_name, "r", encoding="ascii") as data_file:
        data = data_file.read().splitlines()
        start = None
        goal = None
        elev = {}
        for i, row in enumerate(data):
            for j, square in enumerate(row):
                if square == "S":
                    start = (i, j)
                elif square == "E":
                    goal = (i, j)
                elev[(i, j)] = square
    return elev, start, goal


def shortest_path_bfs(elev, start, target_elevations, can_step):
    queue = deque([start])
    dist = {start: 0}
    while queue:
        current = queue.popleft()
        if elev[current] in target_elevations:
            return dist[current]
        for neigh in neighbors(elev, current):
            if neigh in dist:
                continue
            if not can_step(elev[current], elev[neigh]):
                continue
            dist[neigh] = dist[current] + 1
            queue.append(neigh)
    return None


def day12_part1(data, start, _):
    return shortest_path_bfs(data, start, "E", can_step_uphill)


def day12_part2(data, _, goal):
    return shortest_path_bfs(data, goal, "Sa", can_step_downhill)


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day12_test.txt")


def test_day12_part1(test_data):
    assert day12_part1(*test_data) == 31


def test_day12_part2(test_data):
    assert day12_part2(*test_data) == 29


if __name__ == "__main__":
    input_data = parse_input("data/day12.txt")

    print("Day 12 Part 1:")
    print(day12_part1(*input_data))  # Correct answer is 534

    print("Day 12 Part 2:")
    print(day12_part2(*input_data))  # Correct answer is 525
