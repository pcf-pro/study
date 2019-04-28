n = int(input())
r = 1 #счетчик тиков
r1 = 0
z = 1 # заполенение таблицы
def sqa(i=0,j=0): # функция для вопроизведения улитки
        global z
        global r
        global r1

        if i == r1 and n-r>=j>=r1:
        #while i == r1 and n-r>=j>=r1:
            sq[i][j]=z
            z+=1



        elif j==n-r and n-r>=i>=r1:
        #while j==n-r and n-r>=i>=r1:
            sq[i][j]=z
            z+=1


        elif i==n-r and n-r>=j>=r1:
        #while i==n-r and n-r>=j>=r1:
            sq[i][j]=z
            z+=1


        elif  j==r1 and n-r>=i>r1:
        #while j==r1 and n-r>=i>r1:
            sq[i][j]=z
            z+=1




sq = [[0 for i in range(n)] for j in range(n)]
#sq = sq1
#sqa()

for i in range(n):
    for j in range(n):
        sqa(i,j)
        #z+=1

'''        if i == r1 and n-r>=j>=r1:
            sq1[i][j]=z
            z+=1
        elif j==n-r and n-r>=i>=r1:
            sq1[i][j]=z
            z+=1
        elif i==n-r and n-r>=j>=r1:
            sq1[i][j]=z
            z+=1
        elif  j==r1 and n-r>=i>r1:
            sq1[i][j]=z
            z+=1
        else:
            r+=1
            r1+=1

z=0
for i in range(n):
    for j in range(n):
        sq[i][j]=z
        z+=1
'''
print(sq)
#print(sq1)
for i in sq:
    print(*i)
