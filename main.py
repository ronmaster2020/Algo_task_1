from scripts import PRIM_INIT, EXTRACT_MIN, BUILD_MST, GENERATE_WEIGHTS, GET_AVAILABLE_EDGES
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

G, W = GENERATE_GRAPH_WITH_WEIGHTS(5, 8)
G.printAndWeights(W)
MST = MST_PRIM(G, W)
MST.printAndWeights(W)


# find vertex whose deg[v] < n-1, which means there could be another edge (u, v)
# go over the weights of edges (Ai, v)
# for 3.2. you add an edge (u,v) with weight > max of deg[v]
# for 3.3. you add an edge (u,v) with weight = min - 1, of deg[v]