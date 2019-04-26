d={}
r=''
def get(name, var):
    if var in name:
        return name
    else:
        return get(d, name)

for i in range(int(input())):
    i=input().split()
    if 'create' in i:
        if i[-2] in d:
            d[i[-2]].append(i[-1])
        #d = {i[-1]:i[-2]}
        print(d)
    elif 'add' in i:
        if i[-2] not in d:
            d = {i[-2]:i[-1]}
            print(d)
        else:
            #d[i[-2]]= [d[i[-2]]]
            d[i[-2]].append(i[-1])
        #    d.update({i[-2]:i[-1]})
            print(d)

    elif 'get' in i:
        print(get(i[-1], i[-2]))

'''
        for k , v in d.items():
            if i[-1]==v:
                print (k)
            else:
                print('None')
'''
            #    for j in v:
                #    if i[-1]==v:
                #        print (k)
                #    else:
                #        r = 'None'
        #if len(r)>0:
        #    print(r)
