"""
    Advent of Code 2022
    Day 08: Treetop Tree House
"""

from math import prod

import pytest


def parse_input(file_name):
    with open(file_name, "r", encoding="ascii") as data_file:
        return data_file.read().splitlines()


def build_grid_and_beams(lines):
    raw_grid = [list(map(int, line)) for line in lines]
    rows = range(len(raw_grid))
    cols = range(len(raw_grid[0]))
    grid = {(i, j): raw_grid[i][j] for j in cols for i in rows}
    beams = [[(r, c) for r in rows] for c in cols]
    beams += [[(r, c) for c in reversed(cols)] for r in rows]
    beams += [[(r, c) for r in reversed(rows)] for c in reversed(cols)]
    beams += [[(r, c) for c in cols] for r in reversed(rows)]
    return grid, beams


def visible_in_beam(grid, beam):
    return set(
        pos
        for k, pos in enumerate(beam)
        if grid[pos] > (max(grid[other] for other in beam[:k]) if beam[:k] else -1)
    )


def count_visible_from_tree(grid, beam):
    current = grid[beam[0]]
    score = 0
    for other in beam[1:]:
        score += 1
        if grid[other] >= current:
            break
    return score


def scenic_score(pos, grid, beams):
    return prod(
        count_visible_from_tree(grid, beam[beam.index(pos) :])
        for beam in filter(lambda x: pos in x, beams)
    )


def day08_part1(data):
    grid, beams = build_grid_and_beams(data)
    visible_from_outside = set.union(*(visible_in_beam(grid, beam) for beam in beams))
    return len(visible_from_outside)


def day08_part2(data):
    grid, beams = build_grid_and_beams(data)
    return max(scenic_score(pos, grid, beams) for pos in grid)


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day08_test.txt")


def test_day08_part1(test_data):
    assert day08_part1(test_data) == 21


def test_day08_part2(test_data):
    assert day08_part2(test_data) == 8


if __name__ == "__main__":
    input_data = parse_input("data/day08.txt")

    print("Day 08 Part 1:")
    print(day08_part1(input_data))  # Correct answer is 1801

    print("Day 08 Part 2:")
    print(day08_part2(input_data))  # Correct answer is 209880
