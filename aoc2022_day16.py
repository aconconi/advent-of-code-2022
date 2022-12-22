"""
    Advent of Code 2022
    Day 16: Proboscidea Volcanium
"""

import re
from collections import defaultdict
from itertools import combinations, product

import pytest


def parse_input(file_name):
    with open(file_name, "r", encoding="ascii") as data_file:
        data = re.findall(
            r"Valve ([A-Z][A-Z]) has flow rate=(\d{1,2}); tunnels? leads? to valves? (.+)",
            data_file.read(),
        )
    rates = {}
    graph = defaultdict(list)
    for valve, rate, neighbors in data:
        rates[valve] = int(rate)
        graph[valve] = neighbors.split(", ")
    distance = all_pair_shortest_path(graph)
    targets = frozenset(valve for valve, rate in rates.items() if rate > 0)
    return distance, rates, targets


def all_pair_shortest_path(graph):
    # Floyd-Warshall algorithm
    distance = defaultdict(lambda: float("inf"))
    for a, bs in graph.items():
        distance[a, a] = 0
        for b in bs:
            distance[a, b] = 1
            distance[b, b] = 0
    for a, b, c in product(graph, graph, graph):
        bc, ba, ac = distance[b, c], distance[b, a], distance[a, c]
        if ba + ac < bc:
            distance[b, c] = ba + ac
    return distance


def evaluate_path(rates, opening_seq):
    return sum(
        rates[valve] * time_while_open for valve, time_while_open in opening_seq.items()
    )


def solve(distance, targets, time=30, current="AA", chosen=None):
    if chosen is None:
        chosen = {}
    for other in targets:
        new_time = time - distance[current, other] - 1
        if new_time < 1:
            # no time left to move to another valve
            continue
        new_chosen = chosen | {other: new_time}
        yield from solve(distance, targets - {other}, new_time, other, new_chosen)
    yield chosen


def day16_part1(distance, rates, targets):
    return max(evaluate_path(rates, sequence) for sequence in solve(distance, targets))


def day16_part2(distance, rates, targets):
    max_score = defaultdict(int)
    for solution in solve(distance, targets, 26):
        k = frozenset(solution)
        max_score[k] = max(max_score[k], evaluate_path(rates, solution))
    return max(
        sa + sb for (a, sa), (b, sb) in combinations(max_score.items(), 2) if not a & b
    )


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day16_test.txt")


def test_day16_part1(test_data):
    assert day16_part1(*test_data) == 1651


def test_day16_part2(test_data):
    assert day16_part2(*test_data) == 1707


if __name__ == "__main__":
    input_data = parse_input("data/day16.txt")

    print("Day 16 Part 1:")
    print(day16_part1(*input_data))  # Correct answer is 1986

    print("Day 16 Part 2:")
    print(day16_part2(*input_data))  # Correct answer is 2464
