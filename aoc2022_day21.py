"""
    Advent of Code 2022
    Day 21:
"""

import operator

import pytest

OPS = {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.floordiv}

INVERSE_OPS = {
    ("+", True): operator.sub,
    ("+", False): operator.sub,
    ("*", True): operator.floordiv,
    ("*", False): operator.floordiv,
    ("-", True): operator.add,
    ("-", False): lambda x, y: y - x,
    ("/", True): operator.mul,
    ("/", False): lambda x, y: y // x,
}


def parse_input(file_name):
    with open(file_name, "r", encoding="ascii") as data_file:
        lines = data_file.read().splitlines()
    table = {}
    for line in lines:
        tokens = line.replace(":", "").split(" ")
        if len(tokens) == 2:
            name, number = tokens
            table[name] = int(number)
        else:
            name, a, op, b = tokens
            table[name] = [op, a, b]
    return table


def evaluate(table, monkey):
    tokens = table[monkey]
    if isinstance(tokens, int):
        return tokens
    if tokens is None:
        return None
    op, a, b = tokens
    left = evaluate(table, a)
    right = evaluate(table, b)
    if left is None or right is None:
        return None
    return OPS[op](left, right)


def find_value(table, node, expected):
    if node == "humn":
        return expected
    op, a, b = table[node]
    left = evaluate(table, a)
    right = evaluate(table, b)
    if left is None:
        return find_value(table, a, INVERSE_OPS[op, True](expected, right))
    return find_value(table, b, INVERSE_OPS[op, False](expected, left))


def day21_part1(table):
    return evaluate(table, "root")


def day21_part2(table):
    modified_table = dict(table)
    modified_table["humn"] = None
    modified_table["root"][0] = "-"
    return find_value(modified_table, "root", 0)


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day21_test.txt")


def test_day21_part1(test_data):
    assert day21_part1(test_data) == 152


def test_day21_part2(test_data):
    assert day21_part2(test_data) == 301


if __name__ == "__main__":
    input_data = parse_input("data/day21.txt")

    print("Day 21 Part 1:")
    print(day21_part1(input_data))  # Correct answer is 299983725663456

    print("Day 21 Part 2:")
    print(day21_part2(input_data))  # Correct answer is 3093175982595
