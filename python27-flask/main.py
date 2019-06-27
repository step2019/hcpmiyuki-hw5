#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.api import urlfetch
import json
from search_norikae import *
from flask import Flask, render_template, request

app = Flask(__name__)
app.debug = True

networkJson = urlfetch.fetch("http://tokyo.fantasy-transit.appspot.com/net?format=json").content  # ウェブサイトから電車の線路情報をJSON形式でダウンロードする
network = json.loads(networkJson.decode('utf-8'))  # JSONとしてパースする（stringからdictのlistに変換する）

@app.route('/')
# / のリクエスト（例えば http://localhost:8080/ ）をこの関数で処理する。
# ここでメニューを表示をしているだけです。
def root():
  return render_template('hello.html')

@app.route('/pata')
# /pata のリクエスト（例えば http://localhost:8080/pata ）をこの関数で処理する。
# これをパタトクカシーーを処理するようにしています。
def pata():
  # とりあえずAとaをつなぐだけで返事を作っていますけど、パタタコカシーーになるように自分で直してください！
  a_string_list = list(request.args.get('a', ''))
  b_string_list = list(request.args.get('b', ''))
  pata = ""
  if len(a_string_list) <= len(b_string_list):
      for i in range(len(a_string_list)):
          b_string_list.insert(i*2,a_string_list[i])
          pata = "".join(b_string_list)
  else:
      for i in range(len(b_string_list)):
          a_string_list.insert(i*2+1,b_string_list[i])
          pata = "".join(a_string_list)

  # pata.htmlのテンプレートの内容を埋め込んで、返事を返す。
  return render_template('pata.html', pata=pata)

@app.route('/norikae')
# /norikae のリクエスト（例えば http://localhost:8080/norikae ）をこの関数で処理する。
# ここで乗り換え案内をするように編集してください。
def norikae():
  station_list = []
  for line in network:
      for station in line["Stations"]:
          station_list.append(station)
  set_station_list = list(set(station_list))

  return render_template('norikae.html', stations=set_station_list)

@app.route('/search', methods=['POST'])
def search():
  if request.method == 'POST':
    from_station = request.form['from_station']
    to_station = request.form['to_station']
    norikae_route = search_norikae(from_station, to_station)
  return render_template('norikae_result.html', norikae_route=norikae_route)
