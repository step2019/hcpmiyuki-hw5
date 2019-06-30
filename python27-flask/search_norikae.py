#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pickle
from collections import deque
import logging
from google.appengine.api import urlfetch
import json
from make_graph import *

networkJson = urlfetch.fetch("http://tokyo.fantasy-transit.appspot.com/net?format=json").content  # ウェブサイトから電車の線路情報をJSON形式でダウンロードする
network = json.loads(networkJson.decode('utf-8'))  # JSONとしてパースする（stringから
station_graph = make_station_graph(make_station_name_list(network), network)

def memorize(memo, pointed):
    for station_dic in station_graph[pointed["name"]]:
        if not station_dic["name"] in memo:
          logging.info("add to memo: memo[%s] = memo[%s] + [%s]" % (station_dic["name"], pointed["name"], pointed))
          logging.info("memo contains: %s" % (" ".join(memo.keys())))
          memo[station_dic["name"]] = memo[pointed["name"]] + [pointed]
    return memo


def search_norikae(from_station, to_station):
    search_deque = deque()
    logging.info("search from=%s to=%s" % (from_station, to_station))
    logging.info("station graph contains: %s" % " ".join(sorted(station_graph.keys())))
    logging.info("contains from (%s)? %s" % (from_station, from_station in station_graph))
    logging.info("contains to (%s)? %s" % (to_station, to_station in station_graph))
    logging.info(u"contains 東京? %s" % (u"東京" in station_graph))
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
