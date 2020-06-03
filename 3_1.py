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
    else:
      print('Invalid character found: ' + line[index])
      exit(1)
    tokens.append(token)
  return tokens


def multi_div(tokens):#掛け算と割り算を演算
    index = 0
    nikome = ''
    while index+2 < len(tokens):
        print(tokens[index])
        if tokens[index+1]['type'] != 'DIVIDE' and tokens[index+1]['type'] != 'MULTIPLE':#次が積や商でなければ
            if tokens[index]['type'] == 'PLUS':
                nikome+='+'
            elif tokens[index]['type'] == 'MINUS':
                nikome+='-'
            else:
                nikome+=str(tokens[index]['number'])
            index+=1#indexを1つ進める
            #和積を計算するための配列であるnikomeに追加
        else:
            if tokens[index]['type'] == 'NUMBER' and tokens[index+2]['type'] == 'NUMBER':#次が積や商で数字なら
                if tokens[index + 1]['type'] == 'MULTIPLE':#積なら
                    multi = tokens[index]['number'] * tokens[index+2]['number']
                    nikome+=str(multi)#掛け算
                    index+=3#indexを3余分に進める
                else: # tokens[index + 1]['type'] == 'DIVIDE':#商なら
                    divide = tokens[index]['number'] / tokens[index+2]['number']
                    nikome+=str(divide)#割り算
                    index+=3#indexを3余分に進める

            else:#積商の前後が数字じゃない例外なら
                print('Invalid syntax_multi_div')
                exit(1)            

    if index+1<=len(tokens):#最後から二文字目は和積記号、最後の１文字は数字
        if tokens[index]['type'] == 'PLUS':#まずは最後から二文字目をnikomeに追加
            nikome+='+'
        elif tokens[index]['type'] == 'MINUS':
            nikome+='-'
        else:
            print('Invalid syntax')
            exit(1) 
           
        nikome+=str(tokens[index+1]['number'])#最後の１文字をnikomeに追加
    return nikome


def evaluate(tokens):
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
        print('Invalid syntax')
        exit(1)
    index += 1
  return answer

def test(line):
  tokens = tokenize(line)
  secondtokens = multi_div(tokens)
  tokens2 = tokenize(secondtokens)
  actualAnswer = evaluate(tokens2)
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
  test("4/2+2/4")#小数含み
  test("3*4+2/4+5*6")#積商複数
  test("2+4*5-6+3/2")#四則演算すべて含む
  print("==== Test finished! ====\n")

runTest()

while True:
  print('> ', end = '')
  line = input()
  tokens = tokenize(line)
  secondtokens = multi_div(tokens)
  tokens2 = tokenize(secondtokens)
  answer = evaluate(tokens2)
  print("answer = %f\n" % answer)
