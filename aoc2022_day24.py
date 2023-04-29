"""
    Advent of Code 2022
    Day 24: Blizzard Basin
"""

import heapq
from dataclasses import dataclass

import pytest

DIR_DELTA = {"^": (-1, 0), "v": (1, 0), "<": (0, -1), ">": (0, 1)}
MOVES = list(DIR_DELTA.values()) + [(0, 0)]
memo = {}


@dataclass
class Valley:
    height: int
    width: int
    start: tuple
    goal: tuple
    blizzards: tuple


def parse_input(file_name):
    with open(file_name, "r", encoding="ascii") as data_file:
        rows = [row[1:-1] for row in data_file.read().splitlines()[1:-1]]
    blizzards = tuple(
        (i, j, DIR_DELTA[d][0], DIR_DELTA[d][1])
        for i, row in enumerate(rows)
        for j, d in enumerate(row)
        if d in DIR_DELTA
    )
    height, width = len(rows), len(rows[0])
    return Valley(
        height=height,
        width=width,
        start=(-1, 0),
        goal=(height, width - 1),
        blizzards=blizzards,
    )


def blizzards_at_time(valley, t):
    if t not in memo:
        memo[t] = {
            ((r + dr * t) % valley.height, (c + dc * t) % valley.width)
            for r, c, dr, dc in valley.blizzards
        }
    return memo[t]


def shortest_path(valley, start, goal, init_time):
    seen = set()
    queue = [(init_time, start)]
    while queue:
        t, pos = heapq.heappop(queue)
        if pos == goal:
            return t
        if (t, pos) in seen:
            continue
        seen.add((t, pos))
        r, c = pos
        for dr, dc in MOVES:
            new_pos = new_r, new_c = (r + dr, c + dc)
            if (t + 1, new_pos) in seen:
                continue
            if not (0 <= new_r < valley.height and 0 <= new_c < valley.width):
                if (new_r, new_c) not in [start, goal]:
                    continue
            if (new_r, new_c) in blizzards_at_time(valley, t + 1):
                continue
            heapq.heappush(queue, (t + 1, new_pos))


def day24_part1(valley):
    return shortest_path(valley, valley.start, valley.goal, 0)


def day24_part2(valley):
    start, goal = valley.start, valley.goal
    t = shortest_path(valley, start, goal, 0)
    t = shortest_path(valley, goal, start, t)
    t = shortest_path(valley, start, goal, t)
    return t


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day24_test.txt")


def test_day24_part1(test_data):
    assert day24_part1(test_data) == 18


def test_day24_part2(test_data):
    assert day24_part2(test_data) == 54


if __name__ == "__main__":
    input_data = parse_input("data/day24.txt")

    print("Day 24 Part 1:")
    print(day24_part1(input_data))  # Correct answer is 279

    print("Day 24 Part 2:")
    print(day24_part2(input_data))  # Correct answer is 762
