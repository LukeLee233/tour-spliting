#!/home/luke/anaconda3/envs/tensorflow1.15/bin/python
# coding=utf-8

from dataclasses import dataclass
from collections import defaultdict
import pytest
from typing import List

INF = 100000
distance = defaultdict(dict)


@dataclass
class TimeWindow:
    start: int
    end: int


@dataclass
class Ends:
    first: int
    second: int


@dataclass
class Task:
    endpoint: Ends
    cost: int
    time_window: TimeWindow


def get_distance(i_, j_):
    if i_ == j_:
        return 0
    try:
        return distance[i_][j_]
    except KeyError:
        return INF


def argmin(sequence: List):
    index, val = -1, INF
    for i in range(len(sequence)):
        if sequence[i] < INF:
            index, val = i, sequence[i]
    return index, val


def vertibe(tasks_):
    W, P, ArriveTime = [], [], []
    for _ in range(len(tasks_)):
        W.append(list())
        P.append(list())
        ArriveTime.append(list())

    W[0].append(0)
    P[0].append(0)
    ArriveTime[0].append(0)

    for i in range(1, len(tasks_)):
        for j in range(len(tasks_[i])):
            distance_ = []
            ArriveTime_ = []
            for k in range(len(W[i - 1])):
                if W[i - 1][k] == INF or ArriveTime[i - 1][k] == INF or ArriveTime[i - 1][k] + tasks_[i - 1][
                    k].cost + get_distance(
                        tasks_[i - 1][k].endpoint.second, tasks_[i][j].endpoint.first) > tasks_[i][j].time_window.end:
                    distance_.append(INF)
                    ArriveTime_.append(INF)
                else:
                    distance_.append(
                        W[i - 1][k] + tasks_[i - 1][k].cost + get_distance(tasks_[i - 1][k].endpoint.second,
                                                                           tasks_[i][j].endpoint.first))
                    ArriveTime_.append(max(tasks_[i][j].time_window.start,
                                           ArriveTime[i - 1][k] + tasks_[i - 1][
                    k].cost+ get_distance(tasks_[i - 1][k].endpoint.second, tasks_[i][j].endpoint.first)))

            idx, val = argmin(distance_)

            P[i].append(idx)
            W[i].append(val)
            if idx == -1:
                ArriveTime[i].append(INF)
            else:
                ArriveTime[i].append(ArriveTime_[idx])

    if len(W) == 1 or len(W[-1]) == 0:
        W, P = [], []
    return W, P


def test():
    # construct demo graph based on 'vertibe.pdf'
    tasks = [
        [Task(Ends(0, 0), 0, TimeWindow(0, INF))],
        [Task(Ends(1, 2), 5, TimeWindow(3, 5)), Task(Ends(2, 1), 5, TimeWindow(3, 5))],
        [Task(Ends(3, 4), 4, TimeWindow(6, 10)), Task(Ends(4, 3), 4, TimeWindow(6, 10))],
        [Task(Ends(5, 6), 3, TimeWindow(15, 16))],
        [Task(Ends(7, 8), 4, TimeWindow(20, 28)), Task(Ends(8, 7), 4, TimeWindow(20, 28))],
        [Task(Ends(9, 9), 2, TimeWindow(29, 35))],
        [Task(Ends(0, 0), 0, TimeWindow(0, INF))]
    ]

    distance[0][1] = 3
    distance[0][2] = 4

    distance[1][3] = 3
    distance[1][4] = 4
    distance[2][3] = 2
    distance[2][4] = 1

    distance[3][5] = 1
    distance[3][6] = 3

    distance[6][7] = 6
    distance[6][8] = 5

    distance[7][9] = 3
    distance[8][9] = 4

    distance[9][0] = 1

    W, P = vertibe(tasks)
    assert P == [[0],
                 [0, 0],
                 [0, 0],
                 [1],
                 [0, 0],
                 [1],
                 [0]]

    assert W == [[0],
                 [3, 4],
                 [10, 9],
                 [14],
                 [23, 22],
                 [29],
                 [32]]


if __name__ == '__main__':
    pytest.main('-q main.py')
