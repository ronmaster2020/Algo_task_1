from scripts import PRIM_INIT, EXTRACT_MIN, BUILD_MST
import random
import graph
from collections import deque

# G = {
#     'V': list(range(12)),
#     'E': [
#         (0, 1),
#         (0, 2),
#         (0, 3),
#         (1, 5),
#         (2, 3),
#         (2, 4),
#         (3, 5),
#         (3, 6),
#         (4, 8),
#         (4, 9),
#         (5, 11),
#         (6, 7),
#         (6, 9),
#         (7, 11),
#         (8, 10),
#         (10, 11)
#     ]
# }

# W = {
#     (0, 1): 12,
#     (0, 2): 23,
#     (0, 3): 5,
#     (1, 5): 7,
#     (2, 3): 18,
#     (2, 4): 17,
#     (3, 5): 10,
#     (3, 6): 9,
#     (4, 8): 16,
#     (4, 9): 14,
#     (5, 11): 20,
#     (6, 7): 4,
#     (6, 9): 3,
#     (7, 11): 8,
#     (8, 10): 7,
#     (10, 11): 12
# }

# Time Complexity: O(m*logn)
def MST_PRIM(G, W):
    Adj, Q, key, P, n = PRIM_INIT(G)


    while not Q.isEmpty():
        u = EXTRACT_MIN(Q)

        node = Adj.adjList[u]
        while node:
            v = node.value
            # the graph is undirected (לא מכוון), so we check for both orders
            w = W.get((u, v), W.get((v, u)))

            if Q.exists(v) and w < key[v]:
                key[v] = w
                P[v] = u
                Q.decreaseKey(v, key[v])

            node = node.next

    MST = BUILD_MST(P, n)
    return MST

# Time Complexity: O(n) = 3O(n) + O(1)
def Q2_FIND_NEW_MST(MST, W, e, w):
    # O(1)
    max = w
    edge = e
    v = e[0]
    u = e[1]

    # O(n + m) = O(n)
    # explanation: m <= n-1, therefore the time complexity = O(n + m) <= O(2n -1), and O(2n - 1) = O(n)
    _,P = MST.BFS(v)
    if P[u] == None:
        raise ValueError("Invalid MST")
    
    # O(n)
    temp = u
    while temp != v:
        if P[temp] == None:
            raise ValueError("Invalid MST")
        weight = W.get((temp, P[temp]), W.get((P[temp], temp)))
        if weight > max:
            max = weight
            edge = (temp, P[temp])
        temp = P[temp]
    if edge == e:
        return MST
    MST.addEdge(v, u)

    # O(deg(edge[0]) + deg(edge[1])) <= O(n)
    MST.removeEdge(edge[0], edge[1])
    return MST

# the Graph must be connected, and undirected (לא מכוון וקשיר)
def GENERATE_GRAPH():
    n = random.randint(3, 10)
    maxM = n * (n - 1) // 2
    m = random.randint(2, maxM)

    # generate vertices - O(n)
    V = set(range(n))
    G = graph.AdjList(n)

    # time complexity: O(n)
    # firstly we generate a connected graph with n-1 edges
    s = random.choice(list(V))
    K = list({s})
    W = list(V - {s})

    # O(n)
    while W:
        w = random.choice(W)
        u = random.choice(K)
        G.addEdge(u, w)
        K.append(w)
        W.remove(w)

    # time complexity: O(n^2) = O(n*(n-3)/2 + 1)
    # m-(n-1) = n*(n-1)/2 - n + 1 = n*(n-3)/2 + 1
    # next we add the rest of the edges randomly
    # counter will track the number of edges we need to add
    counter = m - (n - 1) 
    while counter > 0:
        v = random.choice(list(V))
        t = list(V - {v})
        tcount = n

        node = G.adjList[v]
        while node:
            tcount = tcount - 1
            t.remove(node.value)
            node = node.next

        numEdgesToAdd = random.randint(1, min(tcount, counter))
        for _ in range(numEdgesToAdd):
            u = random.choice(t)
            tcount = tcount - 1
            G.addEdge(v, u)
            t.remove(u)
            counter = counter - 1
            if counter == 0:
                return G
    return G

# MST = MST_PRIM(G, W)
# MST.print()
# Q2_FIND_NEW_MST(MST, W, (5, 7), 3)
# MST.print()

G = GENERATE_GRAPH()
G.print()