import graph

def PRIM_INIT(G):
    V = G['V']
    E = G['E']

    n = len(V)
    # init adj list
    Adj = graph.AdjList(n)
    for e in E:
        v = e[0]
        u = e[1]
        Adj.addEdge(v, u)

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

def BUILD_MST(P, n):
    MST = graph.AdjList(n)
    for v in range(0, n):
        if P[v] is not None:
            MST.addEdge(P[v], v)
    return MST