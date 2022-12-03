"""
    Advent of Code 2022
    Day 02: Rock Paper Scissors
"""

import pytest


def parse_input(file_name):
    with open(file_name, "r", encoding="ascii") as data_file:
        return [
            ("ABC".find(pair[0]), "XYZ".find(pair[-1]))
            for pair in data_file.read().splitlines()
        ]


def round_score(elf, player):
    score = player + 1
    if elf == player:
        score += 3  # draw
    elif player - elf in [1, -2]:
        score += 6  # player won
    return score


def day02_part1(data):
    return sum(round_score(elf, player) for elf, player in data)


def day02_part2(data):
    return sum(round_score(elf, (elf + player - 1) % 3) for elf, player in data)


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day02_test.txt")


def test_day02_part1(test_data):
    assert day02_part1(test_data) == 15


def test_day02_part2(test_data):
    assert day02_part2(test_data) == 12


if __name__ == "__main__":
    input_data = parse_input("data/day02.txt")

    print("Day 02 Part 1:")
    print(day02_part1(input_data))  # Correct answer is 12586

    print("Day 02 Part 2:")
    print(day02_part2(input_data))  # Correct answer is 13193
