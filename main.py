from scripts import PRIM_INIT, EXTRACT_MIN, BUILD_MST, GENERATE_WEIGHTS, GET_AVAILABLE_EDGES, GET_SHORTEST_PATH
import random
import graph
from collections import deque

# Time Complexity: O(mlogn)
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

# Time Complexity: O(n) (= 3O(n) + O(1))
# explanation:
# (u,v) in a MST completes a circle with the shortest path from u to v, therefore
# We want to extract from the circle the edge with the highest weight, in order to get the new MST
def Q2_FIND_NEW_MST(MST, W, e, w):
    # 1. init
    # Time Complexity: O(1)
    v = e[0]
    u = e[1]

    # 2. get the shortest path between u and v
    # Time Complexity: O(n)
    # explanation: m = n-1 in MST, therefore the time complexity = O(n + m) = O(2n - 1) = O(n)
    shortestPath = GET_SHORTEST_PATH(MST, u, v)

    # 3. find the edge with the highest weight in the circle 
    # Time Complexity: O(n)
    # explanation: O(|shortestPath|) = O(n-1) = O(n)
    max = w
    edge = e
    for e in shortestPath:
        weight = W.get((e[0], e[1]), W.get(e[0], e[1]))
        if weight > max:
            max = weight
            edge = e

    # 4. extract the edge with the highest weight in the circle
    # Time Complexity: O(deg(edge[0]) + deg(edge[1])) less or equal O(n)
    if (edge == (u, v)):
        return MST
    MST.addEdge(v, u)     # O(1)
    MST.removeEdge(edge[0], edge[1])    # O(deg(edge[0]) + deg(edge[1]))

    # 5. return the new MST
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
        availableV = set(V) - fullV
        v = random.choice(list(availableV))

        # find list of available edges to connect to vertex v
        availableEdges = GET_AVAILABLE_EDGES(G, v, V)
        if not availableEdges:
            fullV.add(v)
            if fullV == set(V):
                break
            continue

        # add randomely availabe edges
        numEdgesToAdd = random.randint(1, min(len(availableEdges), maxM - totalEdgesAdded))
        for _ in range(numEdgesToAdd):
            e = random.choice(list(availableEdges))
            G.addEdge(*e) # unpack the tuple e
            W[e] = weightsList.pop()
            availableEdges.remove(e)
            totalEdgesAdded += 1
            if totalEdgesAdded == maxM:
                return G, W
    return G, W

G, W = GENERATE_GRAPH_WITH_WEIGHTS(10, 16)
G.printAndWeights(W)
MST = MST_PRIM(G, W)
MST.printAndWeights(W)

# REPLACE ALL G with adj, and the G should be G=('V':[0,...,n],'E':{...})

# find vertex whose deg[v] < n-1, which means there could be another edge (u, v)
# go over the weights of edges (Ai, v)
# for 3.2. you add an edge (u,v) with weight > max of deg[v]
# for 3.3. you add an edge (u,v) with weight = min - 1, of deg[v]