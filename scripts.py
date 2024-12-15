import graph

def PRIM_INIT(G, W):
    V = G['V']
    E = G['E']

    n = len(V)
    # init adj list
    Adj = graph.AdjList(n)
    for e in E:
        src = e[0]
        dest = e[1]
        weight = W(e)
        Adj.addEdge(src, dest, weight)

    # init min heap
    minHeap = graph.MinHeap()
    # Initialize key values to infinity for all vertices.
    key = [float('inf')] * len(V)
    # the first vertex intialized to 0
    key[0] = 0

    for v in V:
        minHeap.push(v, key[v])
    P = [None] * n
    
    return Adj, minHeap, key, P, n

def EXTRACT_MIN(Q):
    return (Q.pop())[1]

def BUILD_MST(P, key, n):
    MST = graph.AdjList(n)
    for v in range(0, n):
        if P[v] is not None:
            MST.addEdge(P[v], v, key[v])
    return MST