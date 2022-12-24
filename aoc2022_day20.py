"""
    Advent of Code 2022
    Day 20: Grove Positioning System
"""

from collections import deque

import pytest


def parse_input(file_name):
    with open(file_name, "r", encoding="ascii") as data_file:
        return list(map(int, data_file.read().splitlines()))


def move(dq, pair):
    _, number = pair
    if number == 0:
        return 0
    current_pos = dq.index(pair)
    dq.remove(pair)
    new_pos = (current_pos + number) % len(dq)
    if new_pos < 0:
        new_pos += len(dq)
    dq.insert(new_pos, pair)
    return new_pos


def decrypt(data, decryption_key=1, times=1):
    encrypted = tuple((pos, number * decryption_key) for pos, number in enumerate(data))
    dq = deque(encrypted)
    for k in range(times):
        for pair in encrypted:
            move(dq, pair)
        z = dq.index((data.index(0), 0))
    return sum(dq[(z + k * 1000) % len(dq)][1] for k in [1, 2, 3])


def day20_part1(data):
    return decrypt(data)


def day20_part2(data):
    return decrypt(data, decryption_key=811589153, times=10)


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day20_test.txt")


def test_day20_part1(test_data):
    assert day20_part1(test_data) == 3


def test_day20_part2(test_data):
    assert day20_part2(test_data) == 1623178306


if __name__ == "__main__":
    input_data = parse_input("data/day20.txt")

    print("Day 20 Part 1:")
    print(day20_part1(input_data))  # Correct answer is 8028

    print("Day 20 Part 2:")
    print(day20_part2(input_data))  # Correct answer is
