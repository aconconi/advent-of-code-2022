"""
    Advent of Code 2022
    Day 14:
"""

from itertools import pairwise

# pylint: skip-file
import pytest

START = (500, 0)


def parse_input(file_name):
    rock_paths = set()
    with open(file_name, "r", encoding="ascii") as data_file:
        lines = data_file.read().splitlines()
    for line in lines:
        vertices = [
            tuple(int(coord) for coord in pair.split(","))
            for pair in line.split(" -> ")
        ]
        for (x1, y1), (x2, y2) in pairwise(vertices):
            if x1 == x2:
                rock_paths.update((x1, y) for y in range(min(y1, y2), max(y1, y2) + 1))
            elif y1 == y2:
                rock_paths.update((x, y1) for x in range(min(x1, x2), max(x1, x2) + 1))
    return rock_paths


def percolate(pos):
    x, y = pos
    yield from (pos2 for pos2 in [(x, y + 1), (x - 1, y + 1), (x + 1, y + 1)])


def day14_part1(paths):
    occupied = paths.copy()
    pos = START
    count = 0
    bottom = max(y for _, y in occupied)

    def is_free(z):
        return z not in occupied

    while pos[1] != bottom:
        next_pos = next((z for z in percolate(pos) if is_free(z)), pos)
        if next_pos == pos:
            occupied.add(pos)
            count += 1
            pos = START
        else:
            pos = next_pos
    return count


def day14_part2(paths):
    occupied = paths.copy()
    pos = START
    count = 0
    bottom = max(y for _, y in occupied)

    def is_free(z):
        return z not in occupied and z[1] < bottom + 2

    while START not in occupied:
        next_pos = next((z for z in percolate(pos) if is_free(z)), pos)
        if next_pos == pos:
            occupied.add(pos)
            count += 1
            pos = START
        else:
            pos = next_pos
    return count


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day14_test.txt")


def test_day14_part1(test_data):
    assert day14_part1(test_data) == 24


def test_day14_part2(test_data):
    assert day14_part2(test_data) == 93


if __name__ == "__main__":
    input_data = parse_input("data/day14.txt")

    print("Day 14 Part 1:")
    print(day14_part1(input_data))  # Correct answer is 913

    print("Day 14 Part 2:")
    print(day14_part2(input_data))  # Correct answer is 30762
