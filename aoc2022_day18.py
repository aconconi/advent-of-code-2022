"""
    Advent of Code 2022
    Day 18:
"""

import pytest


def parse_input(file_name):
    with open(file_name, "r", encoding="ascii") as data_file:
        return set(
            tuple(map(int, line.split(","))) for line in data_file.read().splitlines()
        )


def neighbors(cube):
    x, y, z = cube
    return {
        (x + 1, y, z),
        (x - 1, y, z),
        (x, y + 1, z),
        (x, y - 1, z),
        (x, y, z + 1),
        (x, y, z - 1),
    }


def get_bounding_box(cubes):
    return tuple(min(cube[i] for cube in cubes) for i in range(3)), tuple(
        max(cube[i] for cube in cubes) for i in range(3)
    )


def in_bounding_box(bounding_box, cube, expand=0):
    box_min, box_max = bounding_box
    return all(box_min[i] - expand <= cube[i] <= box_max[i] + expand for i in range(3))


def day18_part1(cubes):
    return sum(6 - len(cubes.intersection(neighbors(cube))) for cube in cubes)


def day18_part2(cubes):
    box = (box_min, _) = get_bounding_box(cubes)
    outside = set()
    queue = [tuple(c - 1 for c in box_min)]
    while queue:
        cube = queue.pop()
        outside.add(cube)
        queue.extend(
            neigh
            for neigh in neighbors(cube) - cubes - outside
            if in_bounding_box(box, neigh, expand=1)
        )
    return sum(neigh in outside for cube in cubes for neigh in neighbors(cube))


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day18_test.txt")


def test_day18_part1(test_data):
    assert day18_part1(test_data) == 64


def test_day18_part2(test_data):
    assert day18_part2(test_data) == 58


if __name__ == "__main__":
    input_data = parse_input("data/day18.txt")

    print("Day 18 Part 1:")
    print(day18_part1(input_data))  # Correct answer is 4474

    print("Day 18 Part 2:")
    print(day18_part2(input_data))  # Correct answer is 2518
