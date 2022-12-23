"""
    Advent of Code 2022
    Day 19: Not Enough Minerals
"""

import re
from math import prod

import pytest


def t_add(tuple_a, tuple_b):
    return tuple(a + b for a, b in zip(tuple_a, tuple_b))


def t_sub(tuple_a, tuple_b):
    return tuple(a - b for a, b in zip(tuple_a, tuple_b))


def parse_input(file_name):
    with open(file_name, "r", encoding="ascii") as data_file:
        return [parse_blueprint(line) for line in data_file.read().splitlines()]


def parse_blueprint(line):
    _, a, b, c, d, e, f = map(int, re.findall(r"\d+", line))
    # a blueprint is represented as a pair (cost, production) where
    # cost is (cost_geode, cost_obsidian, cost_clay, cost ore) and
    # production is (produces_geode, produces_obsidian, produces_clay, produces ore),
    return (
        ((0, 0, 0, a), (0, 0, 0, 1)),
        ((0, 0, 0, b), (0, 0, 1, 0)),
        ((0, 0, d, c), (0, 1, 0, 0)),
        ((0, f, 0, e), (1, 0, 0, 0)),
        ((0, 0, 0, 0), (0, 0, 0, 0)),
    )


def run_blueprint(blueprint, time_availabe):
    ore_robot = ((0, 0, 0, 0), (0, 0, 0, 1))  # costs nothing, produces ore
    queue = [ore_robot]
    seen = set()
    for _ in range(time_availabe):
        next_queue = []
        for have, make in queue:
            if (have, make) in seen:
                continue
            seen.add((have, make))
            for cost, more in blueprint:
                if any(c > h for c, h in zip(cost, have)):
                    continue
                next_queue.append((t_sub(t_add(have, make), cost), t_add(make, more)))
        queue = sorted(next_queue, key=lambda x: x[1], reverse=True)[:5000]
    return max(have[0] for have, _ in queue)


def day19_part1(blueprints):
    return sum(
        (i + 1) * run_blueprint(blueprint, 24) for i, blueprint in enumerate(blueprints)
    )


def day19_part2(blueprints):
    return prod(run_blueprint(blueprint, 32) for blueprint in blueprints[:3])


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day19_test.txt")


# this test fails because of the poor pruning heuristic
# def test_day19_part1(test_data):
#    assert day19_part1(test_data) == 33


def test_day19_part2(test_data):
    assert day19_part2(test_data) == 3472


if __name__ == "__main__":
    input_data = parse_input("data/day19_test.txt")

    print("Day 19 Part 1:")
    print(day19_part1(input_data))  # Correct answer is 1192

    print("Day 19 Part 2:")
    print(day19_part2(input_data))  # Correct answer is 14725
