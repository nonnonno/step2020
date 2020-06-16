#!/usr/bin/env python3

import sys
import math

from common import print_tour, read_input, format_tour 


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)


def solve(cities):
    N = len(cities)

    dist = [[0] * N for i in range(N)]#地点の数(N個)ぶん([0]*Nとは?)？？distの配列を準備??
    for i in range(N):
        for j in range(i, N):#二点間の距離を格納
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])

    current_city = 0#現在地
    unvisited_cities = set(range(1, N))#(set:重複を避ける),1~Nまでの値を重複なく格納???(unvisitedの中身が分からない)
    tour = [current_city]#すでに通った地点のリストに現在地をセットして初期化

    while unvisited_cities:#unvisitedcitiesのリストの中身がある間?
        next_city = min(unvisited_cities,#distの値を基準として昇順に並べ替えて、最小値をnextcityに格納
                        key=lambda city: dist[current_city][city])
        unvisited_cities.remove(next_city)#すでに通ったので除去
        tour.append(next_city)#通った履歴としてtourに追加
        current_city = next_city#現在地の更新


    return tour


if __name__ == '__main__':
    assert len(sys.argv) > 1
    tour = solve(read_input(sys.argv[1]))
    with open(f'output_{sys.argv[1]}.csv', 'w') as f:#outputファイルにそれぞれ書き出し
                f.write(format_tour(tour) + '\n')
    print_tour(tour)
