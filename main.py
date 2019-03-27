arrInput = [
    '11111111111',
    '00001000001',
    '11101011101',
    '10001010001',
    '10111010111',
    '10100010001',
    '10101010101',
    '10101010101',
    '10101010101',
    '10001010100',
    '11111111111']

#cek pintu masuk dan keluar
count  = 0
door =[]
i = 0
row = len(arrInput)
col = len(arrInput[0])
while (count<2 and i<row):
    j = 0
    while(count<2 and j<col):
        if(i == 0 and arrInput[i][j] == '0'):
            door.append([i,j])
            count+=1
        elif(j == 0 and arrInput[i][j] == '0'):
            door.append([i,j])
            count+=1
        elif(i == row-1 and arrInput[i][j] == '0'):
            door.append([i,j])
            count+=1
        elif(j == col-1 and arrInput[i][j] == '0'):
            door.append([i,j])
            count+=1
        j+=1
    i+=1

BFS()

def printMap():
    for row in arrInput:
        for col in row:
            print(col, end="")
        print()

def BFS():
    queue = []
    