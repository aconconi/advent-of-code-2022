"""
    Advent of Code 2022
    Day 04: Camp Cleanup
"""

import pytest


def parse_input(file_name):
    with open(file_name, "r", encoding="ascii") as data_file:
        return [
            # this converts a line "a1-a2, b1-b2" into a tuple (a1, a2, b1, b2)
            tuple(map(int, line.replace("-", " ").replace(",", " ").split()))
            for line in data_file
        ]


def day04_part1(data):
    return sum(
        a1 >= a2 and b1 <= b2 or a2 >= a1 and b2 <= b1 for a1, b1, a2, b2 in data
    )


def day04_part2(data):
    return sum(
        a2 <= a1 <= b2 or a2 <= b1 <= b2 or a1 <= a2 <= b1 or a1 <= b2 <= b1
        for a1, b1, a2, b2 in data
    )


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day04_test.txt")


def test_day04_part1(test_data):
    assert day04_part1(test_data) == 2


def test_day04_part2(test_data):
    assert day04_part2(test_data) == 4


if __name__ == "__main__":
    input_data = parse_input("data/day04.txt")

    print("Day 04 Part 1:")
    print(day04_part1(input_data))  # Correct answer is 532

    print("Day 04 Part 2:")
    print(day04_part2(input_data))  # Correct answer is 854
