f = open("edges.txt","r")
stack = []
adjList = {}
rev_graph = {}
n =0 
m =0
def dfs(visited,curr,rev):
    if(rev):
        print(curr,end=" ")
    visited[curr] = 1
    if rev==0:
        for x in adjList[curr]:
            # print(x)
            if not visited[x]:
                dfs(visited,x,rev)
        stack.append(curr)
    else:
        for x in rev_graph[curr]:
            if not visited[x]:
                dfs(visited,x,rev)        

if __name__ == '__main__':  
    first = 1  
    for x in f:
        a,b = x.split(',')
        a = int(a)
        b = int(b)
        if first:
            n = a
            m=b
            first=0
            continue
        # print(a,b)
        if a in adjList.keys():
            adjList[a].append(b)
        else:
            adjList[a]=[b]
        if b in rev_graph.keys():
            rev_graph[b].append(a)
        else:
            rev_graph[b]=[a]
    # print(adjList)
    # print(rev_graph)
    visited = [0]*(n+1)
    for i in range(1,n+1):
        if (i not in adjList.keys()):
            adjList[i]=[]
    for i in range(1,n+1):
        if (i not in rev_graph.keys()):
            rev_graph[i]=[]
    for i in range(1,n+1):
        if not visited[i]:
            dfs(visited,i,0)
    visited = [0]*(n+1)
    while len(stack):
        source = stack[len(stack)-1]
        stack.pop()
        if visited[source]:
            continue
        else:
            dfs(visited,source,1)
            print()
