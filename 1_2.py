import csv
import pprint
from math import sqrt

def anagram_basic(random_word):
    sorted_random_word = ''.join(sorted(random_word.lower()))#入力された単語をソート
    new_dictionary = []
    ok_word = []
    tokuten = []
    a=0
    b=0
    # 以下で一つ目の要素についてabc順ソートされたファイルの読み込み
    input_file = open('/Users/AHiroe/Desktop/STEP/anagram_sorted_dictionary2.csv','r')
    f = csv.reader(input_file)

    for x in f:
        new_dictionary.append(x)

    for word in new_dictionary:#前から順にanagramになりうるものを探す
        if new_dictionary[a][0] in sorted_random_word:
            ok_word.append(new_dictionary[a][1].lower())#ok_wordに追加
        a+=1

    #ok_wordの点数をそれぞれ求めたい
    for w in ok_word:
        print(ok_word)
        tokuten.append(tennsu(w))#ok_wordの点数をtennsuという関数を用いて計算し、tokutenというリストにいれる
        print(tennsu(w))
    label = tokuten.index(max(tokuten))#最大得点を持つワードのindexを受け取る
    return ok_word[label]

def tennsu(word):
    tennsu=0
    for i in range(len(word)):
        if word[i] in ['a', 'b', 'd', 'e', 'g', 'i', 'n', 'o', 'r', 's', 't', 'u']:
            tennsu+=1
            if word[i-1] == 'q' and word[i] == 'u':#もしquの入力があったら
                                                    #uがダブルカウントになってしまうので、得点を1減らす
                tennsu -=1
        elif word[i] in ['c', 'f', 'h', 'l', 'm', 'p', 'v', 'w', 'y']:
            tennsu+=2
        else:
            tennsu+=3
    tennsu = (tennsu+1) ** 2
    return tennsu
      
ans = anagram_basic(str(input()))#どんな入力もstr型に丸め込む事で想定外の入力に対応する
print(ans)
