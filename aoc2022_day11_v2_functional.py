"""
    Advent of Code 2022
    Day 11: Monkey in the Middle
"""

from dataclasses import dataclass
from math import prod
from typing import Any, Callable, List, Optional

import pytest


@dataclass
class Monkey:
    initial_items: tuple
    operation: Callable
    divisor: int
    if_true: int
    if_false: int


def create_op(op: str, old: str) -> Callable:
    match (op, old):
        case ("*", old) if old.isnumeric():
            return lambda x: x * int(old)
        case ("*", "old"):
            return lambda x: x * x
        case ("+", old) if old.isnumeric():
            return lambda x: x + int(old)
        case _:
            raise ValueError("Unexpected operation: {op=} {old=}")


def read_monkey(section: Any) -> Monkey:
    _, items, operation, divisor, if_true, if_false = section.splitlines()
    return Monkey(
        initial_items=tuple(map(int, items[18:].strip().split(","))),
        operation=create_op(*operation.split()[-2:]),
        divisor=int(divisor[21:]),
        if_true=int(if_true[29:]),
        if_false=int(if_false[29:]),
    )


def inspect(monkey: Monkey, item: int, div: int, mod: Optional[int]) -> int:
    op_result = monkey.operation(item) // div
    return op_result % mod if mod else op_result


def throw_to(monkey: Monkey, item: int) -> int:
    return monkey.if_true if item % monkey.divisor == 0 else monkey.if_false


def parse_input(file_name: str) -> List[Monkey]:
    with open(file_name, "r", encoding="ascii") as data_file:
        return [read_monkey(section) for section in data_file.read().split("\n\n")]


def solve(monkeys: List[Monkey], rounds: int, div: int, mod: Optional[int]) -> int:
    inspections = [0] * len(monkeys)
    items = [list(monkey.initial_items) for monkey in monkeys]
    for _ in range(rounds):
        for i, monkey in enumerate(monkeys):
            for item in items[i]:
                updated_item = inspect(monkey, item, div, mod)
                inspections[i] += 1
                other = throw_to(monkey, updated_item)
                items[other].append(updated_item)
            items[i] = []
    inspections.sort(reverse=True)
    return inspections[0] * inspections[1]


def day11_part1(monkeys: List[Monkey]) -> int:
    return solve(monkeys, rounds=20, div=3, mod=None)


def day11_part2(monkeys: List[Monkey]) -> int:
    return solve(
        monkeys, rounds=10_000, div=1, mod=prod(monkey.divisor for monkey in monkeys)
    )


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day11_test.txt")


def test_day11_part1(test_data):
    assert day11_part1(test_data) == 10605


def test_day11_part2(test_data):
    assert day11_part2(test_data) == 2713310158


if __name__ == "__main__":
    input_data = parse_input("data/day11.txt")

    print("Day 11 Part 1:")
    print(day11_part1(input_data))  # Correct answer is 76728

    print("Day 11 Part 2:")
    print(day11_part2(input_data))  # Correct answer is 21553910156
