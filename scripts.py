import graph
import random

def PRIM_INIT(n):
    # init min heap
    minHeap = graph.MinHeap()
    # Initialize key values to infinity for all vertices.
    key = [float('inf')] * n
    # the first vertex intialized to 0
    key[0] = 0

    for v in range(n):
        minHeap.push(v, key[v])
    P = [None] * n
    
    return minHeap, key, P

def EXTRACT_MIN(Q):
    return (Q.pop())[1]

def BUILD_MST(P, n):
    MST = graph.AdjList(n)
    for v in range(0, n):
        if P[v] is not None:
            MST.addEdge(P[v], v)
    return MST

def GENERATE_WEIGHTS(n):
    weights = [random.randint(-100, 100) for _ in range(n)]
    return weights