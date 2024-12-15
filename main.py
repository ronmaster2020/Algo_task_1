from scripts import PRIM_INIT, EXTRACT_MIN, BUILD_MST
from collections import deque

G = {
    'V': list(range(12)),
    'E': [
        (0, 1, 12),
        (0, 2, 23),
        (0, 3, 5),
        (1, 5, 7),
        (2, 3, 18),
        (2, 4, 17),
        (3, 5, 10),
        (3, 6, 9),
        (4, 8, 16),
        (4, 9, 14),
        (5, 11, 20),
        (6, 7, 4),
        (6, 9, 3),
        (7, 11, 8),
        (8, 10, 7),
        (10, 11, 12)
    ]
}

weightFunction = lambda e : e[2]

def MST_PRIM(G, W):
    Adj, Q, key, P, n = PRIM_INIT(G, W)


    while not Q.isEmpty():
        u = EXTRACT_MIN(Q)

        node = Adj.adjList[u]
        while node:
            v = node.value
            w = node.weight

            if Q.exists(v) and w < key[v]:
                key[v] = w
                P[v] = u
                Q.decreaseKey(v, key[v])

            node = node.next

    MST = BUILD_MST(P, key, n)
    return MST

def BFS(G, s):
    n = len(G.adjList)
    visited = [False] * n
    d = [float('inf')] * n
    p = [None] * n
    visited[s] = True
    d[s] = 0
    Q = deque()
    Q.append(s)
    while len(Q) != 0:
        u = Q.popleft()
        node = G.adjList[u]
        while node:
            v = node.value
            if not visited[v]:
                visited[v] = True
                d[v] = d[u] + 1
                p[v] = u
                Q.append(v)
            node = node.next
    return d, p

MST = MST_PRIM(G, weightFunction)
MST.print()

distances, parents = BFS(MST, 0)