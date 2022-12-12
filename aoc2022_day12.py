"""
    Advent of Code 2022
    Day 12:
"""

from collections import deque

# pylint: skip-file
import pytest

DELTA = {(0, 1), (0, -1), (-1, 0), (1, 0)}

TRANSLATE_ELEV = str.maketrans("SE", "az")


"""
The elevation of the destination square can be at most one higher
than the elevation of your current square; that is, if your
current elevation is m, you could step to elevation n, but not
to elevation o. (This also means that the elevation of the destination
square can be much lower than the elevation of your current square.)
"""


def neighbors(r, c, n_rows, n_cols):
    yield from (
        (r + dr, c + dc)
        for dr, dc in DELTA
        if 0 <= r + dr < n_rows and 0 <= c + dc < n_cols
    )


def can_step_uphill(current_h, neigh_h):
    return (
        ord(neigh_h.translate(TRANSLATE_ELEV))
        - ord(current_h.translate(TRANSLATE_ELEV))
        <= 1
    )


def can_step_downhill(current_h, neigh_h):
    return (
        ord(neigh_h.translate(TRANSLATE_ELEV))
        - ord(current_h.translate(TRANSLATE_ELEV))
        >= -1
    )


def parse_input(file_name):
    with open(file_name, "r", encoding="ascii") as data_file:
        data = data_file.read().splitlines()
        start = None
        goal = None
        for i, row in enumerate(data):
            for j, current in enumerate(row):
                if current == "S":
                    start = (i, j)
                elif current == "E":
                    goal = (i, j)
    return data, start, goal


def shortest_path(data, start, target_elevations, can_step):
    num_rows, num_cols = len(data), len(data[0])
    queue = deque([start])
    dist = {start: 0}
    while queue:
        current = queue.popleft()
        r, c = current
        if data[r][c] in target_elevations:
            return dist[current]
        current_elevation = data[r][c]
        for neigh in neighbors(r, c, num_rows, num_cols):
            neigh_r, neigh_c = neigh
            neigh_elevation = data[neigh_r][neigh_c]
            if neigh in dist:
                continue
            if not can_step(current_elevation, neigh_elevation):
                continue
            dist[neigh] = dist[current] + 1
            queue.append(neigh)
    return None


def day12_part1(data, start, _):
    return shortest_path(data, start, "E", can_step_uphill)


def day12_part2(data, _, goal):
    return shortest_path(data, goal, "Sa", can_step_downhill)


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
