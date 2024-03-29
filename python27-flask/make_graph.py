#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pickle

# jsonが長いのでpickleにしてしまう
def make_network_json_pickle():
    network_json = [{"Name":"山手線","Stations":["品川","大崎","五反田","目黒","恵比寿","渋谷","原宿","代々木","新宿","新大久保","高田馬場","目白","池袋","大塚","巣鴨","駒越","田端駅","西日暮里","日暮里","鶯谷","上野","御徒町","秋葉原","神田","東京","有楽町","新橋","浜松町","田町"]},{"Name":"東横線","Stations":["横浜","反町","東白楽","白楽","妙蓮寺","菊名","大倉山","綱島","日吉","元住吉","武蔵小杉","新丸子","多摩川","田園調布","自由が丘","都立大学","学芸大学","祐天寺","中目黒","代官山","渋谷"]},{"Name":"目黒線","Stations":["日吉","元住吉","武蔵小杉","新丸子","多摩川","田園調布","奥沢","大岡山","洗足","西小山","武蔵小山","不動前","目黒"]},{"Name":"池上線","Stations":["蒲田","蓮沼","池上","千鳥町","久が原","御嶽山","雪が谷大塚","石川台","洗足池","長原","旗の台","荏原中延","戸越銀座","大崎広小路","五反田"]},{"Name":"多摩川線","Stations":["多摩川","沼部","鵜の木","下丸子","武蔵新田","矢口渡","蒲田"]},{"Name":"大井町線","Stations":["二子玉川","上野毛","等々力","尾山台","九品仏","自由が丘","緑が丘","大岡山","北千束","旗の台","荏原町","中延","戸越公園","下神明","大井町"]},{"Name":"日比谷線","Stations":["中目黒","恵比寿","広尾","六本木","神谷町","霞ケ関","日比谷","銀座","東銀座","築地","八丁堀","茅場町","人形町","小伝馬町","秋葉原","仲御徒町","上野","入谷","三ノ輪","南千住","北千住"]}]
    savename = "network_json.pickle"
    pickle.dump(network_json, open(savename, "wb"))


# 駅名の一覧を作成["蒲田", "蓮沼", "沼部"・・・]
def make_station_name_list(network_json):
    station_list = []
    for line in network_json:
        for station in line["Stations"]:
              station_list.append(station)
    set_station_list = list(set(station_list))
    return set_station_list


# ある駅から行くことができる駅名を路線と一緒に記録する　例：蒲田　["蒲田":[{"name":"蓮沼", "line":"池上線"}, {"name":"沼部", "line":"多摩川線"}・・・]]
def make_station_graph(station_name_list, network_json):
    station_graph = {}
    for station_name in station_name_list:
        for network in network_json:
            station_line_list = []
            if station_name in network["Stations"]:
                for s in network["Stations"]:
                    station_line_list.append({"name":s, "line":network["Name"]})
                if not station_name in station_graph:
                    station_graph[station_name] = station_line_list
                else:
                    station_graph[station_name] += station_line_list

    return station_graph

# 実行すると3つのpickleファイルが作成される
if __name__ == "__main__":
    make_network_json_pickle()
    network_json = pickle.load(open("network_json.pickle", "rb"))
    station_name_list = make_station_name_list(network_json)
    station_graph = make_station_graph(station_name_list, network_json)
    savename_1 = "station_graph.pickle"
    savename_2 = "station_name_list.pickle"
    pickle.dump(station_graph, open(savename_1, "wb"))
    pickle.dump(station_name_list, open(savename_2, "wb"))
    print("finish")
