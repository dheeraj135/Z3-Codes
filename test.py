import itertools

k = 5
arr = [0]*k
for i in range(k):
    arr[i]=i
for ele in itertools.combinations(arr,3):
    print(ele[0])