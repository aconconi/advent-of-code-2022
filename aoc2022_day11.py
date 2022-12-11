"""
    Advent of Code 2022
    Day 11: Monkey in the Middle
"""

from dataclasses import dataclass
from math import prod
from typing import Callable, List

import pytest


@dataclass
class Monkey:
    items: List
    operation: Callable
    divisor: int
    if_true: int
    if_false: int
    count: int = 0

    def inspect(self, item: int, div, mod) -> int:
        self.count += 1
        op_result = self.operation(item) // div
        return op_result % mod if mod else op_result

    def throw_to(self, item) -> int:
        return self.if_true if item % self.divisor == 0 else self.if_false


def build_test_monkeys():
    return [
        Monkey(
            items=[79, 98],
            operation=lambda x: x * 19,
            divisor=23,
            if_true=2,
            if_false=3,
        ),
        Monkey(
            items=[54, 65, 75, 74],
            operation=lambda x: x + 6,
            divisor=19,
            if_true=2,
            if_false=0,
        ),
        Monkey(
            items=[79, 60, 97],
            operation=lambda x: x * x,
            divisor=13,
            if_true=1,
            if_false=3,
        ),
        Monkey(
            items=[74], operation=lambda x: x + 3, divisor=17, if_true=0, if_false=1
        ),
    ]


def build_input_monkeys():
    return [
        Monkey(
            items=[61], operation=lambda x: x * 11, divisor=5, if_true=7, if_false=4
        ),
        Monkey(
            items=[76, 92, 53, 93, 79, 86, 81],
            operation=lambda x: x + 4,
            divisor=2,
            if_true=2,
            if_false=6,
        ),
        Monkey(
            items=[91, 99],
            operation=lambda x: x * 19,
            divisor=13,
            if_true=5,
            if_false=0,
        ),
        Monkey(
            items=[58, 67, 66],
            operation=lambda x: x * x,
            divisor=7,
            if_true=6,
            if_false=1,
        ),
        Monkey(
            items=[94, 54, 62, 73],
            operation=lambda x: x + 1,
            divisor=19,
            if_true=3,
            if_false=7,
        ),
        Monkey(
            items=[59, 95, 51, 58, 58],
            operation=lambda x: x + 3,
            divisor=11,
            if_true=0,
            if_false=4,
        ),
        Monkey(
            items=[87, 69, 92, 56, 91, 93, 88, 73],
            operation=lambda x: x + 8,
            divisor=3,
            if_true=5,
            if_false=2,
        ),
        Monkey(
            items=[71, 57, 86, 67, 96, 95],
            operation=lambda x: x + 7,
            divisor=17,
            if_true=3,
            if_false=1,
        ),
    ]


def parse_input(file_name):
    with open(file_name, "r", encoding="ascii") as data_file:
        return data_file.read()


def solve(monkeys, rounds, div=3, mod=1):
    for _ in range(rounds):
        for monkey in monkeys:
            while monkey.items:
                item = monkey.inspect(monkey.items.pop(0), div, mod)
                other = monkey.throw_to(item)
                monkeys[other].items.append(item)
    inspections = sorted((monkey.count for monkey in monkeys), reverse=True)
    return inspections[0] * inspections[1]


def day11_part1(monkeys):
    return solve(monkeys, rounds=20, div=3, mod=None)


def day11_part2(monkeys):
    return solve(
        monkeys, rounds=10_000, div=1, mod=prod(monkey.divisor for monkey in monkeys)
    )


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return build_test_monkeys()


def test_day11_part1(test_data):
    assert day11_part1(test_data) == 10605


def test_day11_part2(test_data):
    assert day11_part2(test_data) == 2713310158


if __name__ == "__main__":
    # input_data = parse_input("data/day11_test.txt")

    print("Day 11 Part 1:")
    print(day11_part1(build_input_monkeys()))  # Correct answer is 76728

    print("Day 11 Part 2:")
    print(day11_part2(build_input_monkeys()))  # Correct answer is 21553910156
