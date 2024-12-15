from scripts import PRIM_INIT, EXTRACT_MIN, BUILD_MST
import graph

G = {
    'V': list(range(12)),
    'E': [
        (0, 1),
        (0, 2),
        (0, 3),
        (1, 5),
        (2, 3),
        (2, 4),
        (3, 5),
        (3, 6),
        (4, 8),
        (4, 9),
        (5, 11),
        (6, 7),
        (6, 9),
        (7, 11),
        (8, 10),
        (10, 11)
    ]
}

W = {
    (0, 1): 12,
    (0, 2): 23,
    (0, 3): 5,
    (1, 5): 7,
    (2, 3): 18,
    (2, 4): 17,
    (3, 5): 10,
    (3, 6): 9,
    (4, 8): 16,
    (4, 9): 14,
    (5, 11): 20,
    (6, 7): 4,
    (6, 9): 3,
    (7, 11): 8,
    (8, 10): 7,
    (10, 11): 12
}

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

MST = MST_PRIM(G, W)
# MST.print()

# def Q2_FIND_NEW_MST(MST, e, w):


#     src = e[0]
#     dest = e[1]
#     _,P = MST.BFS(src)
#     W = None
#     node = MST.adjList[P[dest]]
#     max = float('-inf')
#     while node:
#         v = node.value
#         w = node.weight
#         if node.weight > max:
#             max = node.weight
#         node = node.next

#     if W == None:
#         raise KeyError("Not an MST")

# Q2_FIND_NEW_MST(MST, (5, 7), 3)