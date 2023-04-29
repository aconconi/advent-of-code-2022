"""
    Advent of Code 2022
    Day 23: Unstable Diffusion
"""

from collections import defaultdict
from itertools import count

import pytest


def parse_input(file_name):
    with open(file_name, "r", encoding="ascii") as data_file:
        return [
            (i, j)
            for i, row in enumerate(data_file.read().splitlines())
            for j, c in enumerate(row)
            if c == "#"
        ]


MOVE_DIRECTIONS = "N S W E".split()

SIDES = {
    "N": ["N", "NE", "NW"],
    "S": ["S", "SE", "SW"],
    "W": ["W", "NW", "SW"],
    "E": ["E", "NE", "SE"],
}

DELTA = {
    "NW": (-1, -1),
    "N": (-1, 0),
    "NE": (-1, 1),
    "E": (0, 1),
    "SE": (1, 1),
    "S": (1, 0),
    "SW": (1, -1),
    "W": (0, -1),
}


def move(elf, direction):
    r, c = elf
    dr, dc = DELTA[direction]
    # print(elf, direction,  (r + dr, c + dc))
    return r + dr, c + dc


def is_valid_direction(elves, elf, direction):
    return all(move(elf, d) not in elves for d in SIDES[direction])


def has_adjacent(current, elf):
    return any(move(elf, d) in current for d in DELTA)


def how_many_empty(elves):
    min_r = min(r for (r, _) in elves)
    min_c = min(c for (_, c) in elves)
    max_r = max(r for (r, _) in elves)
    max_c = max(c for (_, c) in elves)
    return abs(max_r - min_r + 1) * abs(max_c - min_c + 1) - len(elves)


def play_round(elves, tick):
    # first half of the round
    proposed = defaultdict(list)
    for elf in elves:
        # If no other Elves are in one of those eight positions,
        # the Elf does not do anything during this round.
        if not has_adjacent(elves, elf):
            continue
        # Otherwise, looks in each of four directions in rotating
        # order k and proposes moving one step in the first *valid direction*
        for k in range(4):
            direction = MOVE_DIRECTIONS[(tick + k) % 4]
            if is_valid_direction(elves, elf, direction):
                # track desired move for this Elf
                proposed[move(elf, direction)].append(elf)
                break

    # second half of the round
    moves = 0
    for pos in proposed:
        if len(proposed[pos]) == 1:
            # only 1 Elf proposed this position, therefore we update his position
            elf = proposed[pos][0]
            elves.add(pos)
            elves.remove(elf)
            moves += 1

    return moves


def day23_part1(data):
    elves = set(data)
    for tick in range(10):
        play_round(elves, tick)
    return how_many_empty(elves)


def day23_part2(data):
    elves = set(data)
    for tick in count():
        moves = play_round(elves, tick)
        if moves == 0:
            return tick + 1
    return None  # this can't be reached but keeps pylint happy


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day23_test.txt")


def test_day23_part1(test_data):
    assert day23_part1(test_data) == 110


def test_day23_part2(test_data):
    assert day23_part2(test_data) == 20


if __name__ == "__main__":
    input_data = parse_input("data/day23.txt")

    print("Day 23 Part 1:")
    print(day23_part1(input_data))  # Correct answer is 4114

    print("Day 23 Part 2:")
    print(day23_part2(input_data))  # Correct answer is 970
