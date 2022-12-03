"""
    Advent of Code 2022
    Day 03: Rucksack Reorganization
"""

import pytest


def parse_input(file_name):
    with open(file_name, "r", encoding="ascii") as data_file:
        return data_file.read().splitlines()


def chunker(seq, size):
    return (seq[pos : pos + size] for pos in range(0, len(seq), size))


def priority(char):
    if char.islower():
        # Lowercase item types a through z have priorities 1 through 26.
        return ord(char) - ord("a") + 1
    else:
        # Uppercase item types A through Z have priorities 27 through 52.
        return ord(char) - ord("A") + 27


def day03_part1(data):
    return sum(
        priority(set(line[: len(line) // 2]).intersection(line[len(line) // 2 :]).pop())
        for line in data
    )


def day03_part2(data):
    return sum(
        priority(set(line1).intersection(line2).intersection(line3).pop())
        for line1, line2, line3 in chunker(data, 3)
    )


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day03_test.txt")


def test_day03_part1(test_data):
    assert day03_part1(test_data) == 157


def test_day03_part2(test_data):
    assert day03_part2(test_data) == 70


if __name__ == "__main__":
    input_data = parse_input("data/day03.txt")

    print("Day 03 Part 1:")
    print(day03_part1(input_data))  # Correct answer is 7716

    print("Day 03 Part 2:")
    print(day03_part2(input_data))  # Correct answer is
