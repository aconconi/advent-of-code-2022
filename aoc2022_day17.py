"""
    Advent of Code 2022
    Day 17: Pyroclastic Flow
"""

from itertools import cycle

import pytest


def parse_input(file_name):
    with open(file_name, "r", encoding="ascii") as data_file:
        return data_file.read().rstrip("\n")


# Each rock appears so that its left edge is two units away from the left wall
# and its bottom edge is three units above the highest rock in the room
# (or the floor, if there isn't one).
class Rock:
    SHAPES = {
        "-": {(0, 0), (1, 0), (2, 0), (3, 0)},
        "+": {(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)},
        "L": {(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)},
        "|": {(0, 0), (0, 1), (0, 2), (0, 3)},
        "o": {(0, 0), (1, 0), (0, 1), (1, 1)},
    }

    def __init__(self, shapes_generator, altitude):
        self.shape = next(shapes_generator)
        self.points = {(2 + x, altitude + 4 + y) for x, y in Rock.SHAPES[self.shape]}

    def push_aside(self, direction, occupied):
        match direction:
            case "<":
                moved = {(x - 1, y) for x, y in self.points}
                if not (moved & occupied or min(x for x, _ in moved) < 0):
                    self.points = moved
                    return True
            case ">":
                moved = {(x + 1, y) for x, y in self.points}
                if not (moved & occupied or max(x for x, _ in moved) > 6):
                    self.points = moved
                    return True
        return False

    def move_down(self, occupied):
        down = {(x, y - 1) for x, y in self.points}
        if down & occupied:
            # rock is blocked, cannot move down
            return False
        # rock could successfuly move down
        self.points = down
        return True


def solve(jet_pattern, total_rocks):
    occupied = {(x, 0) for x in range(7)}  # floor
    stopped = 0
    height_increase = 0
    altitude = 0
    shapes_generator = cycle(Rock.SHAPES)
    rock = Rock(shapes_generator, 0)
    cycle_found = False
    seen = {}
    for i, direction in enumerate(cycle(jet_pattern)):
        i = i % len(jet_pattern)
        rock.push_aside(direction, occupied)
        if rock.move_down(occupied):
            continue
        stopped += 1
        occupied |= rock.points
        altitude = max(y for _, y in occupied)
        roof = tuple(
            next(
                delta
                for delta in range(altitude + 1)
                if (x, altitude - delta) in occupied
            )
            for x in range(7)
        ) + (i, rock.shape)
        if not cycle_found:
            if roof in seen:
                cycle_found = True
                prev_stopped, prev_alt = seen[roof]
                stopped, height_increase = jump_ahead(
                    prev_stopped, prev_alt, stopped, altitude, total_rocks
                )
            else:
                seen[roof] = stopped, altitude
        if stopped == total_rocks:
            break
        rock = Rock(shapes_generator, altitude)
    return height_increase + altitude


def jump_ahead(prev_stopped, prev_alt, stopped, altitude, total_rocks):
    rocks_per_cycle = stopped - prev_stopped
    height_per_cycle = altitude - prev_alt
    remaining_rocks = total_rocks - stopped
    cycles_remaining, rock_remainder = divmod(remaining_rocks, rocks_per_cycle)
    height_increase = height_per_cycle * cycles_remaining
    new_stopped = total_rocks - rock_remainder
    return new_stopped, height_increase


def day17_part1(jet_pattern):
    return solve(jet_pattern, 2022)


def day17_part2(jet_pattern):
    return solve(jet_pattern, 1_000_000_000_000)


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day17_test.txt")


def test_day17_part1(test_data):
    assert day17_part1(test_data) == 3068


def test_day17_part2(test_data):
    assert day17_part2(test_data) == 1514285714288


if __name__ == "__main__":
    input_data = parse_input("data/day17.txt")

    print("Day 17 Part 1:")
    print(day17_part1(input_data))  # Correct answer is 3130

    print("Day 17 Part 2:")
    print(day17_part2(input_data))  # Correct answer is 1556521739139
