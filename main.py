from scripts import PRIM_INIT, EXTRACT_MIN, BUILD_MST, GENERATE_WEIGHTS
import random
import graph
from collections import deque

# Time Complexity: O(m*logn)
def MST_PRIM(G, W):
    n = G.numVertices
    Q, key, P= PRIM_INIT(n)


    while not Q.isEmpty():
        u = EXTRACT_MIN(Q)

        node = G.adjList[u]
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
def GENERATE_GRAPH_WITH_WEIGHTS(minN, maxN):
    n = random.randint(minN, maxN)
    maxM = random.randint(n-1, n*(n-1)//2)
    weightsList = GENERATE_WEIGHTS(maxM)
    W = {}

    # generate vertices - O(n)
    V = list(range(n))
    G = graph.AdjList(n)

    # time complexity: O(n)
    # firstly we generate a connected graph with n-1 edges
    connected = [random.choice(V)]
    remaining = set(V) - set(connected)

    while remaining:
        u = random.choice(connected)
        v = random.choice(list(remaining))
        G.addEdge(u, v)
        W[(u, v)] = weightsList.pop()
        connected.append(v)
        remaining.remove(v)

    # add the rest edges randomly (up to maxM)
    totalEdgesAdded = n - 1
    fullV = set()
    while totalEdgesAdded < maxM:
        v = random.choice(V)

        # find list of available edges to add to vertex v
        neighbors = set()
        node = G.adjList[v]
        while node:
            neighbors.add(node.value)
            node = node.next

        available = set(V) - {v} - neighbors

        if available:
            # add randomely availabe edges
            numEdgesToAdd = random.randint(1, min(len(available), maxM - totalEdgesAdded))
            for _ in range(numEdgesToAdd):
                u = random.choice(list(available))
                G.addEdge(u, v)
                W[(u, v)] = weightsList.pop()
                available.remove(u)
                totalEdgesAdded += 1
                if totalEdgesAdded == maxM:
                    return G, W
        else:
            fullV.add(v)
            if fullV == set(V):
                break
    return G, W

# MST = MST_PRIM(G, W)
# MST.print()
# Q2_FIND_NEW_MST(MST, W, (5, 7), 3)
# MST.print()

G, W = GENERATE_GRAPH_WITH_WEIGHTS(5, 8)
G.printAndWeights(W)
MST = MST_PRIM(G, W)
MST.printAndWeights(W)