import sys
import random
if(len(sys.argv)==3):
    n = int(sys.argv[1])
    m = int(sys.argv[2])
    # print(n,m)
else:
    print("Program Name n m\n")
    exit(0)

doneAlready = dict()
i = 0
if(n*(n-1)<m):
    print("No solution")
    exit(0)
f = open("edges.txt","w")
f. write("%d,%d\n"%(n,m))
while(i<m):
    a = random.randint(1,n)
    b = random.randint(1,n)
    # print(a,b)
    if a==b:
        continue
    if (a,b) in doneAlready.keys(): #or (b,a) in doneAlready.keys():
        continue
    doneAlready[a,b]=1
    f.write("%d,%d\n"%(a,b))
    i+=1
