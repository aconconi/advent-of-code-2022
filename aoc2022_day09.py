"""
    Advent of Code 2022
    Day 09:
"""

DELTA = {"U": (0, +1), "D": (0, -1), "L": (-1, 0), "R": (+1, 0)}
ROPE_LENGTH = 10


def parse_input(file_name):
    with open(file_name, "r", encoding="ascii") as data_file:
        steps = []
        for line in data_file.read().splitlines():
            direction, amount = line.split()
            steps.extend([DELTA[direction]] * int(amount))
        return steps


def sign(x):
    return 1 if x >= 0 else -1


def adjacent(a, b):
    return abs(b[0] - a[0]) <= 1 and abs(b[1] - a[1]) <= 1


def move(pos, step):
    return (pos[0] + step[0], pos[1] + step[1])


def update_coord(leader_coord, follower_coord):
    delta = leader_coord - follower_coord
    match abs(delta):
        case 0:
            return follower_coord
        case 1:
            return leader_coord
        case 2:
            return follower_coord + sign(delta)


def follow(leader, follower):
    return (
        follower
        if adjacent(leader, follower)
        else tuple(
            update_coord(leader_coord, follower_coord)
            for leader_coord, follower_coord in zip(leader, follower)
        )
    )


def day09_part1(steps):
    head = (0, 0)
    tail = (0, 0)
    visited = {tail}
    for step in steps:
        prev_head = head
        head = move(head, step)
        tail = prev_head if not adjacent(head, tail) else tail
        visited.add(tail)
    return len(visited)


def day09_part2(steps):
    rope = [(0, 0)] * ROPE_LENGTH
    visited = {rope[-1]}
    for step in steps:
        prev_rope = rope.copy()
        rope = [move(prev_rope[0], step)]
        rope.extend(follow(rope[i - 1], prev_rope[i]) for i in range(1, ROPE_LENGTH))
        visited.add(rope[-1])
    return len(visited)


def test_day09_part1():
    assert day09_part1(parse_input("data/day09_test.txt")) == 13


def test_day09_part2():
    assert day09_part2(parse_input("data/day09_test2.txt")) == 36


if __name__ == "__main__":
    input_data = parse_input("data/day09.txt")

    print("Day 09 Part 1:")
    print(day09_part1(input_data))  # Correct answer is 6406

    print("Day 09 Part 2:")
    print(day09_part2(input_data))  # Correct answer is 2643
