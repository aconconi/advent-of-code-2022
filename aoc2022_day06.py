"""
    Advent of Code 2022
    Day 06: Tuning Trouble
"""

import pytest


def parse_input(file_name):
    with open(file_name, "r", encoding="ascii") as data_file:
        return data_file.read().strip()


def detect_marker(signal, window_size):
    return next(
        i
        for i in range(window_size, len(signal))
        if len(set(signal[i - window_size : i])) == window_size
    )


def day06_part1(data):
    return detect_marker(data, window_size=4)


def day06_part2(data):
    return detect_marker(data, window_size=14)


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return [
        ("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 7, 19),
        ("bvwbjplbgvbhsrlpgdmjqwftvncz", 5, 23),
        ("nppdvjthqldpwncqszvftbrmjlhg", 6, 23),
        ("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 10, 29),
        ("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 11, 26),
    ]


def test_day06_part1(test_data):
    assert all(day06_part1(signal) == marker1 for (signal, marker1, _) in test_data)


def test_day06_part2(test_data):
    assert all(day06_part2(signal) == marker2 for (signal, _, marker2) in test_data)


if __name__ == "__main__":
    input_data = parse_input("data/day06.txt")

    print("Day 06 Part 1:")
    print(day06_part1("abcdefd"))  # Correct answer is 1848

    print("Day 06 Part 2:")
    print(day06_part2(input_data))  # Correct answer is 2308
