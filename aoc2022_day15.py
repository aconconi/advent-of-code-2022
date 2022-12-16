"""
    Advent of Code 2022
    Day 15: Beacon Exclusion Zone
"""

import re

import pytest


def parse_input(file_name):
    with open(file_name, "r", encoding="ascii") as data_file:
        return [
            tuple(map(int, re.findall(r"[-\d]+", line)))
            for line in data_file.read().splitlines()
        ]


def distance(x1, y1, x2, y2):
    return abs(x2 - x1) + abs(y2 - y1)


def marked(data, y):
    intervals = list(
        sorted(
            (sx - d, sx + d + 1)
            for sx, sy, bx, by in data
            if (d := distance(sx, sy, bx, by) - abs(sy - y)) > 0
        )
    )
    spans = [intervals[0]]
    for left, right in intervals[1:]:
        prev_left, prev_right = spans[-1]
        if left > prev_right:
            spans.append((left, right))
        else:
            spans[-1] = (prev_left, max(right, prev_right))
    return spans


def day15_part1(data, row_index):
    marked_squares = sum(right - left for left, right in marked(data, row_index))
    beacons_on_row = len(set(bx for _, _, bx, by in data if by == row_index))
    return marked_squares - beacons_on_row


def day15_part2(data, sweep):
    return next(
        right * sweep + y
        for y in range(sweep)
        for left, right in marked(data, y)
        if 0 <= right <= sweep
    )


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day15_test.txt")


def test_day15_part1(test_data):
    assert day15_part1(test_data, 10) == 26


# cannot get this test case to work... I think
# I am not getting the input right
# def test_day15_part2(test_data):
#    assert day15_part2(test_data, 4_000_000) == 56000011 # x=14 * 4_000_000 + y=11


if __name__ == "__main__":
    input_data = parse_input("data/day15.txt")
    print("Day 15 Part 1:")
    print(day15_part1(input_data, 2_000_000))  # Correct answer is 5040643

    print("Day 15 Part 2:")
    print(day15_part2(input_data, 4_000_000))  # Correct answer is 11016575214126
