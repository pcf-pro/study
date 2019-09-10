def sqa(i):
    def ta0():
        global r
        if ta[i][j] == 0 :                
            ta[i][j] = a1[r]
            r +=1
    global s, s1, a
    for i in range(a):
        for j in range(a):
            if ta[i][j] == 0:               
                if i == s and j == s:
                    while j!=s1:
                        ta0()
                        if j!=(a-1):
                            j+=1
                if i == s and j == s1:
                    while i!=s1:
                        ta0()
                        if i!=(a-1):
                            i+=1
                if i == s1 and j==s1:
                    while j!=s:
                        ta0()
                        j-=1
                if i == s1 and j== s:
                    while i!=s:
                        ta0()
                        i-=1
                if i==s1==s==j:
                    ta0()
                    return None
                if s!=a-1:
                    s+=1
                s1-=1

a = int(input())
a1 = [i for i in range(1,(a**2)+1)] # генератор числе
ta = [[0 for i in range(a)]for j in range(a)] # генератор матрицы
s, s1, r = 0, a-1, 0
sqa(a)
for re in ta:
    print(*re)