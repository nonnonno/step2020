import csv
from operator import itemgetter
def dictionary_sort(dictionary):
    new_dictionary = []

    for word in dictionary:#new_dictionaryに、小文字・ソート済のものを加えていく
        new_dictionary.append([''.join(sorted(word.lower())),word])

    sorted_new_dictionary = []
    sorted_new_dictionary = new_dictionary.sort(key=itemgetter(0))
    with open('/Users/AHiroe/Desktop/STEP/anagram_sorted_dictionary2.csv','w') as f:
        writer = csv.writer(f)#new_dictionaryの中身を書き出す
        for x in new_dictionary:
            writer.writerow(x)
            
    return 0

f = open('/Users/AHiroe/Desktop/STEP/dictionary.words.txt',"r")
list_row = []
for x in f:
    list_row.append(x.rstrip("\n"))#list_rowに辞書の中身を書き込み
f.close()

dictionary_sort(list_row)
