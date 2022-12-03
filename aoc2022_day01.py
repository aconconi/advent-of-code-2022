"""
    Advent of Code 2022
    Day 01: Calorie Counting
"""

import pytest


def parse_input(file_name):
    with open(file_name, "r", encoding="ascii") as data_file:
        elves = []
        inside_block = False
        for line in data_file.read().splitlines():
            if line:
                if inside_block:
                    elves[-1] += int(line)
                else:
                    elves.append(int(line))
                    inside_block = True
            else:
                inside_block = False
        return elves


def day01_part1(data):
    return max(elf for elf in data)


def day01_part2(data):
    return sum(sorted(elf for elf in data)[-3:])


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day01_test.txt")


def test_day01_part1(test_data):
    assert day01_part1(test_data) == 24000


def test_day01_part2(test_data):
    print(test_data)
    assert day01_part2(test_data) == 45000


if __name__ == "__main__":
    input_data = parse_input("data/day01.txt")

    print("Day 01 Part 1:")
    print(day01_part1(input_data))  # Correct answer is 71023

    print("Day 01 Part 2:")
    print(day01_part2(input_data))  # Correct answer is 206289
