"""
    Advent of Code 2022
    Day 11: Monkey in the Middle
"""

from math import prod
from typing import Callable, List, Optional

import pytest


class Monkey:
    items: List
    operation: Callable
    divisor: int
    if_true: int
    if_false: int

    def __init__(self, section: str):
        monkey_id, items, operation, divisor, if_true, if_false = section.splitlines()
        op, old = operation.split()[-2:]
        match (op, old):
            case ("*", old) if old.isnumeric():
                self.operation = lambda x: x * int(old)
            case ("*", "old"):
                self.operation = lambda x: x * x
            case ("+", old) if old.isnumeric():
                self.operation = lambda x: x + int(old)
            case _:
                raise ValueError(f"Unexpected operation in {monkey_id[:-1].lower()}.")
        self.items = list(map(int, items[18:].strip().split(",")))
        self.divisor = int(divisor[21:])
        self.if_true = int(if_true[29:])
        self.if_false = int(if_false[29:])

    def inspect(self, item: int, div: int, mod: int) -> int:
        op_result = self.operation(item) // div
        return op_result % mod if mod else op_result

    def throw_to(self, item: int) -> int:
        return self.if_true if item % self.divisor == 0 else self.if_false


def parse_input(file_name: str) -> List[Monkey]:
    with open(file_name, "r", encoding="ascii") as data_file:
        sections = data_file.read().split("\n\n")
        return [Monkey(section) for section in sections]


def solve(monkeys: List, rounds: int, div: Optional[int], mod: Optional[int]) -> int:
    inspections = [0] * len(monkeys)
    for _ in range(rounds):
        for i, monkey in enumerate(monkeys):
            while monkey.items:
                item = monkey.inspect(monkey.items.pop(0), div, mod)
                inspections[i] += 1
                other = monkey.throw_to(item)
                monkeys[other].items.append(item)
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
    print("Day 11 Part 1:")
    input_data = parse_input("data/day11.txt")
    print(day11_part1(input_data))  # Correct answer is 76728

    print("Day 11 Part 2:")
    input_data = parse_input("data/day11.txt")
    print(day11_part2(input_data))  # Correct answer is 21553910156
