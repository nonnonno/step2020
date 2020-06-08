def text_to_list(file) : #nickname.txtのファイルをリストとして読み込み
    with open(file) as f:
        l_strip = [s.strip() for s in f.readlines()]#一行ずつ読み込み、改行文字を除去
    length = len(l_strip)
    i=0
    namelist = []
    while length > i:#タブを除去して一人ずつのリストにする[番号,nickname]
        namelist.append(l_strip[i].split())
        i+=1
    return namelist

def links_combine(list) : #同じ人の繋がりをまとめる
    length = len(list)
    i=0
    link_list = []
    person_list = []
    friend_list = []
    person_list.append(list[i][0])#最初のデータを入れておく
    friend_list.append(list[i][1])
    i+=1
    while i<length:
        if list[i-1][0] == list[i][0]:#ひとつ前と同じ人のデータなら
            friend_list.append(list[i][1])
        else:
            person_list.append(friend_list)#前と違う人のデータが始まったので、今までのを処理
            link_list.append(person_list)
            friend_list = []#データを初期化
            person_list =[]
            person_list.append(list[i][0])
            friend_list.append(list[i][1])

        if i==length-1:#最後のデータの時
            person_list.append(friend_list)#データを戻り値に追加して処理を終了
            link_list.append(person_list)
            break
        i+=1
    return link_list


def name_to_num(name,list) : #nicknameに該当するnumberを返す 
    length = len(list)
    i=0
    while length > i:
        if list[i][1] == name:
            return list[i][0]
        i+=1
    print("No such registered name\n")
    exit(1)

def num_to_name(num,list) : #nicknameに該当するnumberを返す 
    length = len(list)
    i=0
    while length > i:
        if list[i][0] == num:
            return list[i][1]
        i+=1
    print("No such registered number\n")
    exit(1)

def child(source,data_lst) : #子ノードを探してリストとして返す
    length = len(data_lst)
    i=0
    while i < length:
        if data_lst[i][0] == source:
            return self_remove(source,data_lst[i][1]) #sourceを除いた子ノードリスト
        i+=1
    return []


def child_search(source,dest,data_lst) : #子ノードのリストに目的地が含まれるか判断
    child_lst = []
    child_lst = child(source,data_lst)#子ノードのリストを求める
    i=0
    length = len(child_lst)
    flag=False#見つかったらTrue,見つからなかったらFalse
    while i < length:
        if child_lst[i] == dest:
            flag = True
            return flag
        i+=1
    return flag

def bfs(source,dest,data_lst):
    if source == dest :
        print("You to you??") #二つの名前が同じ時のエラー処理
        exit(1)
    max_depth = len(data_lst)
    depth = 0
    index = 0
    parent_lst = []
    tmp_lst = []
    parent_lst.append(source)
    parent_lst_len = 0
    while depth < max_depth:
        parent_lst_len = len(parent_lst)
        while index < parent_lst_len:
            if child_search(parent_lst[index],dest,data_lst):
                print("count:",+depth)
                return True
            tmp_lst+=child(parent_lst[index],data_lst)
            index+=1
        parent_lst = [] #リストを世代交代させる
        parent_lst+=tmp_lst
        tmp_lst = []
        depth+=1
        index = 0
    return False

def self_remove(source,lst):#sourceを取り除いたリストを返す
    new_lst = []
    length = len(lst)
    i=0
    while i < length:
        if source != lst[i]:
            new_lst.append(lst[i])
        i+=1
    return new_lst

#今回使用するテキストデータ
namefile = "nicknames.txt"
linkfile = "links.txt"
nickname_list = text_to_list(namefile) #nicknamefileとlinkfileを、リストに格納
link_list = text_to_list(linkfile)
combined_link_list = links_combine(link_list)
print("Put your nickname>")
source_name_num = name_to_num(input(),nickname_list)
print("Put your friend's nickname>")
destination_name_num = name_to_num(input(),nickname_list)
if bfs(source_name_num,destination_name_num,combined_link_list):#幅優先探索
    print("You are friends!!")
else:
    print("You are not connected...")
