"""
    Advent of Code 2022
    Day 25: Full of Hot Air
"""

import numpy as np
import pytest


def parse_input(file_name):
    with open(file_name, "r", encoding="ascii") as data_file:
        return data_file.read().splitlines()


def snafu_to_dec(s: str) -> int:
    base_five = [-1 if c == "-" else -2 if c == "=" else int(c) for c in reversed(s)]
    return sum(d * 5**i for i, d in enumerate(base_five))


def dec_to_snafu(n: int) -> str:
    DEC_TO_SNAFU = "012=-0"
    carry = 0
    ans = []
    for d in map(int, reversed(np.base_repr(n, base=5))):
        d += carry
        carry = 1 if d >= 3 else 0
        ans.append(DEC_TO_SNAFU[d])
    return (dec_to_snafu(carry) if carry else "") + "".join(reversed(ans))


def day25_part1(data):
    assert dec_to_snafu(12345) == "1-0---0"
    assert dec_to_snafu(314159265) == "1121-1110-1=0"

    return dec_to_snafu(sum(snafu_to_dec(s) for s in data))


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_part1():
    return parse_input("data/day25_test.txt")


@pytest.fixture(autouse=True, name="test_pairs")
def fixture_test_pairs():
    return [
        (1, "1"),
        (2, "2"),
        (3, "1="),
        (4, "1-"),
        (5, "10"),
        (6, "11"),
        (7, "12"),
        (8, "2="),
        (9, "2-"),
        (10, "20"),
        (15, "1=0"),
        (20, "1-0"),
        (2022, "1=11-2"),
        (12345, "1-0---0"),
        (314159265, "1121-1110-1=0"),
    ]


def test_day25_part1(test_data):
    assert day25_part1(test_data) == "2=-1=0"


def test_day25_dec_to_snafu(test_pairs):
    for dec, snafu in test_pairs:
        assert dec_to_snafu(dec) == snafu


def test_day25_snafu_to_dec(test_pairs):
    for dec, snafu in test_pairs:
        assert snafu_to_dec(snafu) == dec


if __name__ == "__main__":
    input_data = parse_input("data/day25.txt")

    print("Day 25 Part 1:")
    print(day25_part1(input_data))  # Correct answer is 2-0==21--=0==2201==2

    # There is no puzzle to solve in Part 2
