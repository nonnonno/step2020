#!/usr/bin/env python3

import sys
import math

from common import print_tour, read_input, format_tour 


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

def intersection_judge(a,b,c,d): #線分交差判定      
    print("intersection")   
    xa,ya = a[0],a[1]#citiesにはx,yの順で座標が格納されている
    xb,yb = b[0],b[1]
    xc,yc = c[0],c[1]
    xd,yd = d[0],d[1]

    p = (xa-xb)*(yc-ya)-(ya-yb)*(xc-xa)
    q = (xa-xb)*(yd-ya)-(ya-yb)*(xd-xa)
    r = (xc-xd)*(ya-yc)-(yc-yd)*(xa-xc)
    s = (xc-xd)*(yb-yc)-(yc-yd)*(xb-xc)

    return p*q<0 and r*s<0

def intersection_remove(tour,cities,current_num,next_num,i):
    print("intersection_remove")
    print("before_tour:",tour)
    if i>current_num:
        first_start=current_num
        first_end=next_num
        second_start=i
        second_end=i+1
    elif i<current_num:
        first_start=i
        first_end=i+1
        second_start=current_num
        second_end=next_num

    tour[first_end],tour[second_start]=tour[second_start],tour[first_end]#交差回避のため回る順番をswapする
    #下の式でswapした二本の線分の間の経路の通過順番を、tourリストを逆順にすることによって更新する
    tmp = []
    reverse=tour[first_end:second_start+1]
    reverse.reverse()
    tmp=tour[0:first_end]+reverse+tour[second_start+1:len(tour)]
    reverse=[]
    tour=tmp
    tmp=[]
    print("removed_tour:",tour)
    #intersection(tour,cities,first_start,first_end,i)#新しい線分から先について交差判定を再帰
    return tour

def intersection(tour,cities,current_num,next_num):#交差の判定と除去を取り扱うための関数
    print("intersection")

    #while cnt<len(tour)-1:#前から探索していって交差がなければcntをインクリメントして、交差がなくなるまで続けるという方針の名残
    for i in range(len(tour)-1): 
        if intersection_judge(cities[tour[i]],cities[tour[i+1]],cities[tour[current_num]],cities[tour[next_num]]):#交差しているなら
            tour = intersection_remove(tour,cities,current_num,next_num,i)#交差を除去してtour更新

    return tour


def solve(cities):
    N = len(cities)

    dist = [[0] * N for i in range(N)]#それぞれの要素が 0 で初期化された N x N のサイズの2次元 List を作成
    for i in range(N):
        for j in range(i, N):#二点間の距離を格納
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])

    current_city = 0#現在地
    unvisited_cities = set(range(1, N))#1 ... N-1 が含まれた [1,2,...N-1]を作成
    tour = [current_city]#すでに通った地点のリストに現在地をセットして初期化

    while unvisited_cities:#unvisitedcitiesのリストの中身がある間(まだ通っていない都市がある間)
        next_city = min(unvisited_cities,#未訪問の都市(のid)をとって、現在訪問中の都市からの距離を返す
                        key=lambda city: dist[current_city][city])
        unvisited_cities.remove(next_city)#すでに通ったので除去
        tour.append(next_city)#通った履歴としてtourに追加
        current_city = next_city#現在地の更新

    #このあとは、作った線分について交差しているかintersection_judgeで判定
    #交差していなければそのままで、交差していればswap
    #swapした線分の間のグラフの向きを逆にtypeする
    #swapした線分の、二本目について、通る順番の記録を変える
    #交差がなくなるまで探索を続ける

        tour=intersection(tour,cities,len(tour)-2,len(tour)-1)#交差判定&除去
        current_city = tour[len(tour)-1]

    return tour


if __name__ == '__main__':
    assert len(sys.argv) > 1
    tour = solve(read_input(sys.argv[1]))
    print("version1")
    # with open(f'output_{sys.argv[1]}.csv', 'w') as f:#outputファイルにそれぞれ書き出し
    with open(f'output_3.csv', 'w') as f:#手動で変えて、引数と同じバージョンのファイルを渡しています
                f.write(format_tour(tour) + '\n')
    print_tour(tour)
    print("done")
