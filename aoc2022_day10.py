"""
    Advent of Code 2022
    Day 10: Cathode-Ray Tube
"""

import pytest

INTERESTING = [20, 60, 100, 140, 180, 220]
OPERATIONS = {"noop": (1, lambda: 0), "addx": (2, lambda v: v)}


def parse_input(file_name):
    with open(file_name, "r", encoding="ascii") as data_file:
        return data_file.read().splitlines()


def trace_execution(data):
    x = 1
    trace = []  # trace[i] is the value of register x during cycle i+1
    for line in data:
        op, *params = line.split()
        cycles, func = OPERATIONS[op]
        trace.extend([x] * cycles)  # *during* execution x is not modified
        x += func(*map(int, params))  # x is updated after all cycles are completed
    return trace


def chunker(seq, size):
    return (seq[pos : pos + size] for pos in range(0, len(seq), size))


def day10_part1(data):
    signal = trace_execution(data)
    return sum(i * signal[i - 1] for i in INTERESTING)


def day10_part2(data):
    signal = trace_execution(data)
    return "\n".join(
        "".join("#" if i in [x - 1, x, x + 1] else "." for i, x in enumerate(crt_row))
        for crt_row in chunker(signal, 40)
    )


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day10_test.txt")


def test_day10_part1(test_data):
    assert day10_part1(test_data) == 13140


def test_day10_part2(test_data):
    expected = "\n".join(
        [
            "##..##..##..##..##..##..##..##..##..##..",
            "###...###...###...###...###...###...###.",
            "####....####....####....####....####....",
            "#####.....#####.....#####.....#####.....",
            "######......######......######......####",
            "#######.......#######.......#######.....",
        ]
    )
    assert day10_part2(test_data) == expected


if __name__ == "__main__":
    input_data = parse_input("data/day10.txt")

    print("Day 10 Part 1:")
    print(day10_part1(input_data))  # Correct answer is 15680

    print("Day 10 Part 2:")
    print(day10_part2(input_data))  # Correct answer displays ZFBFHGUP
