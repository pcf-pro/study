n = int(input())
l = []
z = 0
for i in range(1,(n**2)+1):
    l.append(i)
sq = [[0 for i in range(n)] for j in range(n)]
for i in range(n):
    for j in range(n):
        sq[i][j]=l[z]
        z+=1
print(l)
print(sq)
for i in sq:
    print(*i)
