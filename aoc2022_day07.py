"""
    Advent of Code 2022
    Day 07:
"""

from collections import defaultdict

import pytest


def parse_input(file_name):
    seen_files = set()
    dir_sizes = defaultdict(int)
    path = []
    with open(file_name, "r", encoding="ascii") as data_file:
        for line in data_file:
            match line.split():
                case ["$", "cd", "/"]:
                    path = ["/"]
                case ["$", "cd", ".."]:
                    path.pop()
                case ["$", "cd", name]:
                    path.append(name)
                case ["$", "ls"]:
                    continue
                case ["dir", _]:
                    continue
                case [size, filename]:
                    full_path = " ".join(path + [filename])
                    if full_path not in seen_files:
                        seen_files.add(full_path)
                        for i in range(len(path)):
                            dir_sizes[" ".join(path[: i + 1])] += int(size)
        return dir_sizes.values()


def day07_part1(dir_sizes):
    return sum(size for size in dir_sizes if size <= 100000)


def day07_part2(dir_sizes):
    unused = 70_000_000 - max(dir_sizes)
    required = 30_000_000 - unused
    return min(size for size in dir_sizes if size >= required)


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day07_test.txt")


def test_day07_part1(test_data):
    assert day07_part1(test_data) == 95_437


def test_day07_part2(test_data):
    assert day07_part2(test_data) == 24_933_642


if __name__ == "__main__":
    input_data = parse_input("data/day07.txt")

    print("Day 07 Part 1:")
    print(day07_part1(input_data))  # Correct answer is 1501149

    print("Day 07 Part 2:")
    print(day07_part2(input_data))  # Correct answer is 10096985