#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pickle
from collections import deque
import logging

station_graph = pickle.load(open("station_graph.pickle", "rb"))

def memorize(memo, pointed):
    for station_dic in station_graph[pointed["name"]]:
        if not station_dic["name"] in memo:
            memo[station_dic["name"]] = memo[pointed["name"]] + [pointed]
    return memo


def search_norikae(from_station, to_station):
    search_deque = deque()
    logging.info("search from=%s to=%s" % (from_station, to_station))
    logging.info("station graph contains: %s" % " ".join(sorted(station_graph.keys())))
    logging.info("contains from (%s)? %s" % (from_station, from_station in station_graph))
    logging.info("contains to (%s)? %s" % (to_station, to_station in station_graph))
    logging.info("contains 東京? %s" % ("東京" in station_graph))
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
