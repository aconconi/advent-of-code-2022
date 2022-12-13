"""
    Advent of Code 2022
    Day 13: Distress Signal
"""

from functools import cmp_to_key

# pylint: skip-file
import pytest

# Parse the input


# Helper function to compare two values
def compare(left, right):
    # both values are integers
    if isinstance(left, int) and isinstance(right, int):
        return left - right
    # Exactly one value is an integer
    if isinstance(left, int):
        return compare([left], right)
    if isinstance(right, int):
        return compare(left, [right])
    # both values are lists
    for lval, rval in zip(left, right):
        if lst_comparison := compare(lval, rval):
            return lst_comparison
    # consider longer list
    return len(left) - len(right)


def parse_input(file_name):
    with open(file_name, "r", encoding="ascii") as data_file:
        lines = data_file.read().split("\n\n")
        pairs = [line.split("\n") for line in lines]
        pairs = [(eval(pair[0]), eval(pair[1])) for pair in pairs]
        return pairs


def day13_part1(pairs):
    return sum(i + 1 for i, pair in enumerate(pairs) if compare(*pair) < 0)


def day13_part2(pairs):
    DIV1, DIV2 = [[2]], [[6]]
    all_packets = sorted(
        [left for left, _ in pairs] + [right for _, right in pairs] + [DIV1] + [DIV2],
        key=cmp_to_key(compare),
    )
    return (all_packets.index(DIV1) + 1) * (all_packets.index(DIV2) + 1)


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day13_test.txt")


def test_day13_part1(test_data):
    assert day13_part1(test_data) == 13


def test_day13_part2(test_data):
    assert day13_part2(test_data) == 140


if __name__ == "__main__":
    input_data = parse_input("data/day13.txt")

    print("Day 13 Part 1:")
    print(day13_part1(input_data))  # Correct answer is 5393

    print("Day 13 Part 2:")
    print(day13_part2(input_data))  # Correct answer is 26712
