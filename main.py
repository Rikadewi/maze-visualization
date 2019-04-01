# Nama / NIM    : Lukas Kurnia Jonathan / 13517006
#               : Rika Dewi / 13517147
# Tugas Kecil Strategi Algoritma, "Maze Solver"

from copy import deepcopy
from sys import platform

def printX(skk): print("\033[1;35;47m{}\033[00m".format(skk), end="")
def print1(skk): print("\033[1;34;40m{}\033[00m".format(skk), end="")
def print0(skk): print("\033[1;37;47m{}\033[00m".format(skk), end="")
def printExit(skk): print("\033[1;31;41m{}\033[00m".format(skk), end="")
def printEntrance(skk): print("\033[1;32;42m{}\033[00m".format(skk), end="")

#Main Program
print('===========================')
print('Welcome to Maze Solver !')
print('===========================')
print('Please input your maze file (.txt) : ')
print('*NOTE: Pastikan file eksternal tidak memiliki newline di akhir file* ')
namaFile = input('>> ')

#Membaca file eksternal berisi map
with open(namaFile, 'r') as f:
    map = [list(line) for line in f]
for i in range(len(map)-1):  #Menghilangkan '\n' yang ikut terbaca
    map[i].pop()

#cek pintu masuk dan keluar
count  = 0
door =[]
i = 0
row = len(map)
col = len(map[0])
while (count<2 and i<row):
    j = 0
    while(count<2 and j<col):
        if(i == 0 and map[i][j] == '0'):
            door.append([i,j])
            count+=1
        elif(j == 0 and map[i][j] == '0'):
            door.append([i,j])
            count+=1
        elif(i == row-1 and map[i][j] == '0'):
            door.append([i,j])
            count+=1
        elif(j == col-1 and map[i][j] == '0'):
            door.append([i,j])
            count+=1
        j+=1
    i+=1


copyMap = deepcopy(map)

arrNode = []

#Fungi yang mengembalikan manhattan distance dari 2 buah titik
def getManhattan(x1,y1,x2,y2):
    return (abs(y2-y1)+abs(x2-x1))

class Node:
    #ctor
    def __init__(self, x, y, addlist):
        self.id = len(arrNode)
        self.x = x
        self.y = y
        self.list = [] + addlist
        self.g = 0 #nilai dari start ke node bersangkutan
        self.h = getManhattan(door[1][0],door[1][1],self.x,self.y) #nilai dari node bersangkutan ke titik end (Manhattan)
        self.f = 0 #evaluation total cost , g+h
    #menambah list
    def add(self, x):
        self.list.append(x)
    def setG(self,newG):
        self.g =newG
    def setF(self,g,h):
        self.f = g+h

#catatan semua node pada map
arrNode = [
    Node(door[0][0], door[0][1], [0]), #pintu masuk
]
arrNode[0].setF(arrNode[0].g,arrNode[0].h)

#menyimpan antrian id simpul hidup
queueIdNode = [0]

#mengembalikan jumlah jalan yang belum dieksplor
def cekSekitar(x, y):
    count  = 0
    if(x != row-1): #down
        if(map[x+1][y] == '0'): count+=1
    if(x != 0): #up
        if(map[x-1][y] == '0'): count+=1
    if(y != col-1): #right 
        if(map[x][y+1] == '0'): count+=1
    if(y != 0): #left
        if(map[x][y-1] == '0'): count+=1
    return count

#mengembalikan posisi jalan yang belum dieksplor
def cekJalan(x,y):
    if(x != row-1): #down menjadi X
        if(map[x+1][y] == '0'): 
            map[x+1][y] = 'X'
            return x+1, y
    if(x != 0): #up menjadi X
        if(map[x-1][y] == '0'): 
            map[x-1][y] = 'X'
            return x-1, y
    if(y != col-1): #right menjadi X 
        if(map[x][y+1] == '0'): 
            map[x][y+1] = 'X'
            return x, y+1
    if(y != 0): #left menjadi X
        if(map[x][y-1] == '0'): 
            map[x][y-1] = 'X'
            return x, y-1


#boolean untuk menyimpan pintu keluar ditemukan
global found
found = False

#menyimpan path menuju pintu keluar
listOutput = []

#mengunjungi jalan
def kunjungi(x, y, id, listG , code):
    count = cekSekitar(x, y) #menghitung nol disekitar
    if(count>0):
        if(count == 1): 
            i, j = cekJalan(x, y) #mengembalikan kordinat x dan y dari nol yang pertama ditemui secara
            listG.append(listG[0]+1)
            listG.pop(0)
            kunjungi(i, j, id, listG , code) #rekursif


        else:
            while(count>0): #kalau lebih dari 1
                i, j = cekJalan(x, y) #mengembalikan nol yang pertama dia temui lalu mengubah menjadi X
                idx = len(arrNode) #menyimpan id node baru
                newList = [] + arrNode[id].list #akses list parent nya
                newList.append(idx) 
                arrNode.append(Node(i, j, newList))
                arrNode[idx].setG(listG[0]+1)
                arrNode[idx].setF(arrNode[idx].g,arrNode[idx].h)
                if(code == 2):
                    if(len(queueIdNode)!=0):
                        i=0
                        lebihkecil = False
                        while(i<len(queueIdNode)):
                            if(arrNode[idx].f<=arrNode[queueIdNode[i]].f):
                                lebihkecil= True
                                break
                            else:
                                i+=1
                        if(len(queueIdNode)==1 and lebihkecil):
                            queueIdNode.insert(0,idx)
                        elif((len(queueIdNode)==1) and not(lebihkecil)): 
                            queueIdNode.append(idx)
                        elif(i == (len(queueIdNode)) and not(lebihkecil)):
                            queueIdNode.append(idx)
                        else:
                            queueIdNode.insert(i,idx) 
                else:
                    queueIdNode.append(idx) #append ke id node
                count-=1
            listG.append(listG[0]+1)
            listG.pop(0)
    else:
        if (x == door[1][0] and y == door[1][1]):
            found = True
            listOutput.append(arrNode[id].list)

#prosedur BFS
def BFS():
    map[door[0][0]][door[0][1]] = 'X'
    listG=[0]
    while len(queueIdNode) != 0 and not(found):
        idx = queueIdNode[0] #diambil
        kunjungi(arrNode[idx].x, arrNode[idx].y, idx, listG, 1) # kunjungi simpul hidup
        queueIdNode.pop(0)

def AStar():
    map[door[0][0]][door[0][1]] = 'X'
    listG=[0]
    while len(queueIdNode) != 0 and not(found):
        idx = queueIdNode[0] #diambil
        kunjungi(arrNode[idx].x, arrNode[idx].y, idx, listG, 2) # kunjungi simpul hidup
        queueIdNode.remove(idx)

#untuk print isi matriks
def printMap(matriks):
    langkah=0
    for x in range (0, row):
        for y in range (0, col):
            if platform == "linux" or platform == "linux2":
                if(x == door[0][0] and y == door[0][1]):
                    printEntrance("  ")
                    langkah+=1
                elif(x == door[1][0] and y == door[1][1]):
                    printExit("  ")
                    langkah+=1
                elif(matriks[x][y] == 'X'):
                    printX('x ')
                    langkah+=1
                elif(matriks[x][y] == '1'):
                    print1("  ")
                elif(matriks[x][y] == '0' or matriks[x][y] == '2'):
                    print0("  ")
            else:
                if(x == door[0][0] and y == door[0][1]):
                    print("X",end='')
                    langkah+=1
                elif(x == door[1][0] and y == door[1][1]):
                    print("X",end='')
                    langkah+=1
                elif(matriks[x][y] == 'X'):
                    print('x',end='')
                    langkah+=1
                elif(matriks[x][y] == '1'):
                    print("=",end='')
                elif(matriks[x][y] == '0' or matriks[x][y] == '2'):
                    print("0",end='')
        print()
    print('Jumlah langkah =',langkah)

print('Please choose solve method:')
print('1. BFS')
print('2. A* ')
print()

S = input('>> ')
S = int(S)
if(S == 1):
    BFS()
if(S == 2):
    AStar()

list = listOutput[0]
map = copyMap

x = door[0][0]
y = door[0][1]
count = cekSekitar(x,y)

while(count!= 0):
    map[x][y] = 'X'
    if(count > 1 and len(list)!=0): 
        list.pop(0) 
        if(len(list)!=0):
            if (S == 1):
                while(count>0):
                    i, j = cekJalan(x, y)
                    if(i != arrNode[list[0]].x or j != arrNode[list[0]].y):
                        map[i][j] = '2'
                    count -=1
            x = arrNode[list[0]].x
            y = arrNode[list[0]].y
    else:
        x, y = cekJalan(x, y)
    count = cekSekitar(x,y)

printMap(map)

