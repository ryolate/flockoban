#!/usr/bin/env pypy3

from typing import List, Tuple, Dict, Set, FrozenSet
from enum import IntFlag, IntEnum, auto
from sortedcontainers import SortedSet, SortedDict
from collections import deque
import sys


class ActorType(IntFlag):
    PLAYER = auto()
    WHITE = auto()
    BROWN = auto()
    GRAY = auto()
    EMPTY = auto()
    SHEEP = WHITE | BROWN | GRAY


Pos = Tuple[int, int]
Actors = Dict[ActorType, Set[Pos]]


class BackgroundType(IntEnum):
    START = auto()
    BLOCK = auto()
    WHITE = auto()
    BROWN = auto()
    GRAY = auto()
    EMPTY = auto()


Background = List[List[BackgroundType]]


DIR = [
    (0, 1),
    (1, 0),
    (0, -1),
    (-1, 0)
]

# KEYS = "DSAW"
KEYS = "→↓←↑"


def get_actor(a: Actors, p: Pos) -> ActorType:
    for i in [ActorType.PLAYER, ActorType.WHITE, ActorType.BROWN, ActorType.GRAY]:
        if i in a and p in a[i]:
            return i
    return ActorType.EMPTY


def get_bg(b: Background, p: Pos) -> BackgroundType:
    if 0 <= p[0] < len(b) and 0 <= p[1] < len(b[0]):
        return b[p[0]][p[1]]
    return BackgroundType.BLOCK


def pos_add(p: Pos, q: Pos) -> Pos:
    return (p[0]+q[0], p[1]+q[1])


def pos_sub(p: Pos, q: Pos) -> Pos:
    return (p[0]-q[0], p[1]-q[1])


def advance_actor(a: Actors, p: Pos, empty_pos: Pos):
    assert get_actor(
        a, empty_pos) == ActorType.EMPTY, f'{empty_pos} contains {get_actor(a, empty_pos)}'
    t = get_actor(a, p)
    assert t != ActorType.EMPTY
    a[t].remove(p)
    a[t].add(empty_pos)


def move(b: Background, a: Actors, d: int):
    cur = a[ActorType.PLAYER][0]
    next = pos_add(cur, DIR[d])

    next_bg = get_bg(b, next)
    if next_bg == BackgroundType.BLOCK:
        return False

    next_ac = get_actor(a, next)
    if next_ac in ActorType.SHEEP and next_ac != ActorType.WHITE:
        return False

    # visited: 1: before move 2: after move
    def move_sheep(p: Pos, visited: Dict[Pos, int]) -> bool:
        assert get_actor(a, p) in ActorType.SHEEP
        visited[p] = 1

        nx = pos_add(p, DIR[d])
        if get_bg(b, nx) == BackgroundType.BLOCK:
            return False

        if get_actor(a, nx) in ActorType.SHEEP:
            if not move_sheep(nx, visited):
                return False

        # move self
        advance_actor(a, p, nx)
        visited[nx] = 2

        # move others
        for nd in range(len(DIR)):
            if nd == d:
                continue
            np = pos_add(p, DIR[nd])
            if get_actor(a, np) in ActorType.SHEEP and np not in visited:
                move_sheep(np, visited)

        return True

    if next_ac == ActorType.WHITE:
        moved = move_sheep(next, dict())
        if not moved:
            return False

    # Move self
    advance_actor(a, cur, next)

    prev = pos_sub(cur, DIR[d])
    if get_actor(a, prev) == ActorType.BROWN:
        # print("current state: ", a, file=sys.stderr)
        move_sheep(prev, dict())

    return True


def new_background(ss: List[str]) -> Background:
    res = []
    mapping = {
        'S': BackgroundType.START,
        '#': BackgroundType.BLOCK,
        'W': BackgroundType.WHITE,
        'B': BackgroundType.BROWN,
        'G': BackgroundType.GRAY,
    }
    for s in ss:
        row = []
        res.append(row)
        for c in s:
            if c in mapping:
                row.append(mapping[c])
            else:
                row.append(BackgroundType.EMPTY)
    return res


def new_actors(ss: List[str]) -> Actors:
    res = SortedDict()
    mapping = {
        'S': ActorType.PLAYER,
        'w': ActorType.WHITE,
        'b': ActorType.BROWN,
        'g': ActorType.GRAY,
    }
    for i in range(len(ss)):
        for j in range(len(ss[0])):
            c = ss[i][j]
            if c not in mapping:
                continue
            if mapping[c] not in res:
                res[mapping[c]] = SortedSet()
            res[mapping[c]].add((i, j))
    return res


def clone_actors(a: Actors) -> Actors:
    res = SortedDict()
    for k in a.keys():
        res[k] = a[k].copy()
    return res


def is_goal(b: Background, a: Actors) -> bool:
    mapping = {
        ActorType.PLAYER: BackgroundType.START,
        ActorType.WHITE: BackgroundType.WHITE,
        ActorType.BROWN: BackgroundType.BROWN,
        ActorType.GRAY: BackgroundType.GRAY,
    }
    for k in mapping.keys() & a.keys():
        for p in a[k]:
            if get_bg(b, p) != mapping[k]:
                return False
    return True


def freeze_actors(a: Actors) -> Tuple[Pos, FrozenSet[Pos], FrozenSet[Pos]]:
    return (
        a[ActorType.PLAYER][0],
        frozenset(a.get(ActorType.WHITE) or []),
        frozenset(a.get(ActorType.BROWN) or []),
        frozenset(a.get(ActorType.GRAY) or []),
    )


def solve(field: List[str]) -> List[str]:
    """Solves the problem.

    Args:
        field: list of strings represents the field.
            S start
            # block
            . empty
            w white sheep (push)
            b brown sheep (pull)
            g gray sheep
            W white goal
            B brown goal
            G gray goal
    Returns:
        keys to input.
    """
    b = new_background(field)
    a = new_actors(field)

    q = deque([a])
    prev = {freeze_actors(a): [None, -1]}  # [prev state, movement]
    goal = None
    while len(q):
        a = q.popleft()
        if is_goal(b, a):
            goal = a
            break
        for d in range(len(DIR)):
            na = clone_actors(a)
            if not move(b, na, d):
                continue
            f = freeze_actors(na)
            if f in prev:
                continue
            prev[f] = [a, d]
            q.append(na)

    if goal is None:
        raise 'Solution not found'

    res = []
    while goal is not None:
        [goal, d] = prev[freeze_actors(goal)]
        res.append(d)
    res.reverse()
    return "".join(list(map(lambda x: KEYS[x], res[1:])))


def main():
    import sys
    field = list(map(str.strip, sys.stdin.readlines()))
    print(solve(field))


if __name__ == '__main__':
    main()
