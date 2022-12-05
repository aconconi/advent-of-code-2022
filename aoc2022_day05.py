"""
    Advent of Code 2022
    Day 05: Supply Stacks
"""

import re
import pytest


def parse_input(file_name):
    with open(file_name, "r", encoding="ascii") as data_file:
        crates = [[] for _ in range(9)]
        moves = []
        for line in data_file.read().splitlines():
            if line == "":
                continue
            if line[0] == "m":
                moves.append(tuple(map(int, re.findall(r"\d+", line))))
            else:
                for i in range(1, len(line), 4):
                    if line[i].isupper():
                        crates[i // 4].append(line[i])
    crates = [crate[::-1] for crate in crates if crate]
    return crates, moves


def day05_part1(data):
    crates = [list(crate) for crate in data[0]]
    moves = data[1]
    for (quantity, source, dest) in moves:
        for _ in range(quantity):
            crates[dest - 1].append(crates[source - 1].pop())
    return "".join(crate[-1] for crate in crates)


def day05_part2(data):
    crates = [list(crate) for crate in data[0]]
    moves = data[1]
    for (quantity, source, dest) in moves:
        crates[dest - 1].extend(crates[source - 1][-quantity:])
        del crates[source - 1][-quantity:]
    return "".join(crate[-1] for crate in crates)


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day05_test.txt")


def test_day05_part1(test_data):
    assert day05_part1(test_data) == "CMZ"


def test_day05_part2(test_data):
    assert day05_part2(test_data) == "MCD"


if __name__ == "__main__":
    input_data = parse_input("data/day05.txt")

    print("Day 05 Part 1:")
    print(day05_part1(input_data))  # Correct answer is JRVNHHCSJ

    print("Day 05 Part 2:")
    print(day05_part2(input_data))  # Correct answer is GNFBSBJLH
