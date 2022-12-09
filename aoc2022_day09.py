"""
    Advent of Code 2022
    Day 09: Rope Bridge
"""

DELTA = {"U": (0, +1), "D": (0, -1), "L": (-1, 0), "R": (+1, 0)}


def parse_input(file_name):
    with open(file_name, "r", encoding="ascii") as data_file:
        steps = []
        for line in data_file.read().splitlines():
            direction, amount = line.split()
            steps.extend([DELTA[direction]] * int(amount))
        return steps


def adjacent(a, b):
    return abs(b[0] - a[0]) <= 1 and abs(b[1] - a[1]) <= 1


def move(pos, step):
    return (pos[0] + step[0], pos[1] + step[1])


def sign(n):
    return 1 if n > 0 else -1 if n < 0 else 0


def follow(leader, follower):
    return (
        follower
        if adjacent(leader, follower)
        else tuple(
            follower_coord + sign(leader_coord - follower_coord)
            for leader_coord, follower_coord in zip(leader, follower)
        )
    )


def solve(steps, rope_length):
    rope = [(0, 0)] * rope_length
    visited = {rope[-1]}
    for step in steps:
        rope[0] = move(rope[0], step)
        for i in range(1, rope_length):
            rope[i] = follow(rope[i - 1], rope[i])
        visited.add(rope[-1])
    return len(visited)


def day09_part1(steps):
    return solve(steps, 2)


def day09_part2(steps):
    return solve(steps, 10)


def test_day09_part1():
    assert day09_part1(parse_input("data/day09_test.txt")) == 13


def test_day09_part2():
    assert day09_part2(parse_input("data/day09_test.txt")) == 1
    assert day09_part2(parse_input("data/day09_test2.txt")) == 36


if __name__ == "__main__":
    input_data = parse_input("data/day09.txt")

    print("Day 09 Part 1:")
    print(day09_part1(input_data))  # Correct answer is 6406

    print("Day 09 Part 2:")
    print(day09_part2(input_data))  # Correct answer is 2643
