#indexを介して中身を返す関数nakamiを使って、3_1.pyをモジュール化できた
#kakko_naka_keisanを利用して、test関数と、最後のwhile文の中の計算をモジュール化した

def readNumber(line, index):
  number = 0
  while index < len(line) and line[index].isdigit():
    number = number * 10 + int(line[index])
    index += 1
  if index < len(line) and line[index] == '.':
    index += 1
    keta = 0.1
    while index < len(line) and line[index].isdigit():
      number += int(line[index]) * keta
      keta /= 10
      index += 1
  token = {'type': 'NUMBER', 'number': number}
  return token, index


def readPlus(line, index):
  token = {'type': 'PLUS'}
  return token, index + 1


def readMinus(line, index):
  token = {'type': 'MINUS'}
  return token, index + 1

def readMultiple(line, index):
  token = {'type': 'MULTIPLE'}
  return token, index + 1

def readDivide(line, index):
  token = {'type': 'DIVIDE'}
  return token, index + 1

def readStart(line, index):
  token = {'type': 'START'}
  return token, index + 1

def readFinish(line, index):
    token = {'type': 'FINISH'}
    return token, index + 1

def tokenize(line):
  tokens = []
  index = 0
  while index < len(line):
    if line[index].isdigit():
      (token, index) = readNumber(line, index)
    elif line[index] == '+':
      (token, index) = readPlus(line, index)
    elif line[index] == '-':
      (token, index) = readMinus(line, index)
    elif line[index] == '*':
      (token, index) = readMultiple(line, index)
    elif line[index] == '/':
      (token, index) = readDivide(line, index)  
    elif line[index] == '(':
      (token, index) = readStart(line, index)
    elif line[index] == ')':
      (token, index) = readFinish(line, index)    
    else:
      print('Invalid character found: ' + line[index])
      exit(1)
    tokens.append(token)
  return tokens


def multi_div(tokens):#掛け算と割り算を演算
    index = 0
    nikome = ''
    while index < len(tokens):
        if len(tokens) == index+1:
          nikome+=nakami(tokens[index])
          break
        if tokens[index+1]['type'] != 'DIVIDE' and tokens[index+1]['type'] != 'MULTIPLE' :#次が積や商でなければ
          nikome+=nakami(tokens[index])
          index+=1#indexを1つ進める
          #和積を計算するための配列であるnikomeに追加
        else:
            if tokens[index]['type'] == 'NUMBER' and tokens[index+2]['type'] == 'NUMBER':#両脇が数字なら
              if tokens[index+1]['type'] == 'MULTIPLE':#積
                kekka = tokens[index]['number'] * tokens[index+2]['number']
              elif tokens[index+1]['type'] == 'DIVIDE':#商
                kekka = tokens[index]['number'] / tokens[index+2]['number']
              else: 
                print('Invalid syntax_multi_div')
                exit(1)
            else :
              print('Invalid syntax_multi_div')
              exit(1)
            #以上、まずは積商の計算
            if index+3<len(tokens) :#まだ次に調べるべき演算がある
              if tokens[index+3]['type'] == 'MULTIPLE' or tokens[index+3]['type'] == 'DIVIDE':#次が積商
                tokens[index+2]['number'] = kekka#積商の結果を次の演算のひとつ前に格納
                index+=2
              else : #次が積商以外
                nikome+=str(kekka)
                index+=3
            else :#もう調べる演算ない＝式の中で最後の和積
              nikome+=str(kekka)
              return nikome
    return nikome


def evaluate(tokens):#和積の計算
  answer = 0
  tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
  index = 1
  while index < len(tokens):
    if tokens[index]['type'] == 'NUMBER':
      if tokens[index - 1]['type'] == 'PLUS':
        answer += tokens[index]['number']
      elif tokens[index - 1]['type'] == 'MINUS':
        answer -= tokens[index]['number']
      else:
        print('Invalid syntax_eval')
        exit(1)
    index += 1
  return answer

def kakko_naka_keisan(tokens):
    tokens = tokenize(tokens)
    secondtokens = multi_div(tokens)
    tokens2 = tokenize(secondtokens)
    answer = evaluate(tokens2)
    return str(answer)#かっこの中の計算結果を返す

def nakami(tokens):
    if tokens['type'] == 'NUMBER':
        nakami=str(tokens['number'])
    elif tokens['type'] == 'PLUS':
        nakami='+'
    elif tokens['type'] == 'MINUS':
        nakami='-'
    elif tokens['type'] == 'MULTIPLE':
        nakami='*'
    elif tokens['type'] == 'DIVIDE':
        nakami='/'
    elif tokens['type'] == 'START':
        nakami='('
    elif tokens['type'] == 'FINISH':
        nakami=')'
    else:
        print('Invalid syntax_nakami')
        exit(1)
    return nakami


def kakko_find(tokens):
    index=0
    naka = 0#括弧の中か外か判定
    kakkonaka = ''#括弧の中身を格納
    zentai = ''#括弧を除去したものを格納
    cnt=0
    while(index<len(tokens)):
        if tokens[index]['type'] == 'START':
            if naka == 1:#既に括弧の中なら既にある情報をzentaiに移す(入れ子の場合)
                zentai+="("
                zentai+=kakkonaka
                cnt+=1
            kakkonaka = ''#括弧の中身を初期化
            naka = 1#括弧の内部を表す
            
        elif tokens[index]['type'] == 'FINISH' and naka == 1:#今中身を計算したい括弧の閉じ括弧を見つけた場合
            kakko_naka_kekka = kakko_naka_keisan(kakkonaka)#括弧の中身を計算
            zentai += kakko_naka_kekka#全体に追加
            kakkonaka = ''#計算後は初期化
            naka = 0#括弧は終わり
        else :#括弧でないor調べてない括弧の終わりのとき
            cnt+=1#調査対象括弧以外の文字数をカウント
            if naka == 1:#括弧の中なら
                kakkonaka+=nakami(tokens[index])#nakamiという関数を用い、typeで判別して文字をkakkonakaに追加
    
            else :#括弧の外なら
                zentai+=nakami(tokens[index])#zentaiに追加
        index+=1 

    if cnt != len(tokens):#文字列の長さが、括弧を除いた文字列の長さと異なるとき(括弧がまだあるとき)
        zentai = kakko_find(tokenize(zentai))#zentaiにまだ括弧があるので再帰
    
    return zentai 
                

def test(line):
  tokens = tokenize(line)
  kakko_nasi = kakko_find(tokens)
  actualAnswer = float(kakko_naka_keisan(kakko_nasi)) 
  expectedAnswer = eval(line)
  if abs(actualAnswer - expectedAnswer) < 1e-8:
    print("PASS! (%s = %f)" % (line, expectedAnswer))
  else:
    print("FAIL! (%s should be %f but was %f)" % (line, expectedAnswer, actualAnswer))


# Add more tests to this function :)
def runTest():
  print("==== Test started! ====")
  test("1+2")
  test("1.0+2.1-3")
  test("2*5")#シンプルな積
  test("3*5+4*6")#積が複数
  test("8/2/2")#和積が連続する
  test("4/2+2/4")#小数含み
  test("3*4+2/4+5*6")#積商複数
  test("2+4*5-6+3/2")#四則演算すべて含む
  test("(2+1)*2")
  test("(3.0+4*(2-1))/5")#二重括弧
  test("(2+3*(2+(1+4)*3))*2")#三重括弧
  print("==== Test finished! ====\n")

runTest()

while True:
  print('> ', end = '')
  line = input()
  tokens = tokenize(line)
  kakko_nasi = kakko_find(tokens)
  answer = float(kakko_naka_keisan(kakko_nasi))
  print("answer = %f\n" % answer)
