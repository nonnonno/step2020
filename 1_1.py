import csv
import pprint
#同じ単語を入力して実験したときの実行時間について、
# #二分探索した場合と、前から順に見ていった場合では、
# #それぞれ実行時間にばらつきがあったものの、
# 二分探索の方では、異常に実行時間が長くなるということは観測されなかった。
def anagram_basic(random_word):
    sorted_random_word = ''.join(sorted(random_word.lower()))#入力された単語をソート
    new_dictionary = []

    # 以下で一つ目の要素についてabc順ソートされたファイルの読み込み
    input_file = open('/Users/AHiroe/Desktop/STEP/anagram_sorted_dictionary2.csv','r')
    f = csv.reader(input_file)

    for x in f:
        new_dictionary.append(x)
    #二分探索の結果を返す
    return binary_search(new_dictionary,sorted_random_word) #二分探索実行

def binary_search(lst,item):#以下二分探索のアルゴリズム
    length = len(lst)
    low = 0
    high = length - 1
    while low <= high:
        mid = int((low+high)/2)
        if lst[mid][0] == item:#もし一致したら二つ目の要素を返す
            return lst[mid][1]
            break
        elif lst[mid][0] > item:
            high = mid - 1
        elif item > lst[mid][0]:
            low = mid + 1
            
print(anagram_basic(str(input())))#どんな入力もstr型に丸め込む事で想定外の入力に対応する
