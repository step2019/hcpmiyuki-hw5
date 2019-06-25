#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pickle
from collections import deque

station_graph = pickle.load(open("station_graph.pickle", "rb"))

def memorize(memo, pointed):
    for station_dic in station_graph[pointed["name"]]:
        if not station_dic["name"] in memo:
            memo[station_dic["name"]] = memo[pointed["name"]] + [pointed]
    return memo


def search_norikae(from_station, to_station):
    search_deque = deque()
    search_deque += station_graph[from_station]
    searched = []
    memo = {}

    while search_deque:
        pointed = search_deque.popleft()
        if memo == {}:
            memo[from_station] = []

        if not pointed in searched:
            searched += pointed
            memo = memorize(memo, pointed)
            if pointed["name"] == to_station:
                memo[pointed["name"]] += [pointed]
                del memo[pointed["name"]][0]
                return memo[pointed["name"]]
            else:
                search_deque += station_graph[pointed["name"]]

    return False

