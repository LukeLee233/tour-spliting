#!/home/luke/anaconda3/envs/tensorflow1.15/bin/python
# coding=utf-8

from dataclasses import dataclass
from collections import defaultdict
import pytest

INF = 100000
distance = defaultdict(dict)


@dataclass
class TimeWindow:
    start: int
    end: int


@dataclass
class Task:
    demand: int
    cost: int
    time_window: TimeWindow


def get_distance(i_, j_):
    if i_ == j_:
        return 0
    try:
        return distance[i_][j_]
    except KeyError:
        return INF


def tour_spliting(tasks_, Q_):
    tau = len(tasks_)

    W = [0] * tau
    P = [0] * tau
    for i in range(1, tau):
        W[i] = INF

    for i in range(1, tau):
        j = i
        load = 0
        length = 0
        DepartureTime = 0
        u = 0
        while True:
            v = j
            load += tasks_[v].demand
            length = length - get_distance(u, 0) + get_distance(u, v) + tasks_[v].cost + get_distance(v, 0)
            ArrivalTime = DepartureTime + get_distance(u, v)
            DepartureTime = ArrivalTime + max(0, tasks_[v].time_window.start - ArrivalTime) + tasks_[v].cost
            if load <= Q_ and W[i - 1] + length < W[j] and ArrivalTime <= tasks_[v].time_window.end:
                W[j] = W[i - 1] + length
                P[j] = i - 1

            j += 1
            u = v
            if j >= tau or load > Q_ or ArrivalTime > tasks_[u].time_window.end:
                break

    return W, P


def test():
    tasks = [
        Task(0, 0, TimeWindow(0, 250)),
        Task(5, 5, TimeWindow(0, 25)),
        Task(4, 10, TimeWindow(10, 25)),
        Task(4, 10, TimeWindow(20, 60)),
        Task(2, 15, TimeWindow(20, 80)),
        Task(7, 5, TimeWindow(10, 95))
    ]

    distance[0][1] = 20
    distance[0][2] = 25
    distance[0][3] = 45
    distance[0][4] = 25
    distance[0][5] = 15

    distance[1][0] = 10
    distance[1][2] = 10

    distance[2][0] = 5
    distance[2][3] = 15

    distance[3][0] = 30
    distance[3][4] = 25

    distance[4][0] = 40
    distance[4][5] = 55

    distance[5][0] = 5

    Q = 9

    W, P = tour_spliting(tasks, Q)
    assert W == [0, 35, 75, 125, 205, 230]
    assert P == [0, 0, 1, 1, 3, 3]


if __name__ == '__main__':
    pytest.main()
