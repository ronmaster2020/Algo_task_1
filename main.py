from scripts import PRIM_INIT, EXTRACT_MIN, BUILD_GRAPH_FROM_PARENTS_LIST, GENERATE_WEIGHTS, GET_AVAILABLE_EDGES, GET_SHORTEST_PATH, MAKE_ADJ
import random
import graph

# Time Complexity: O((n+m)*logn) = O(m*logn) (because the graph is connected so m >= n-1)
def MST_PRIM(G, W):
    # init
    V = G['V']
    n = len(V)
    Q, key, P = PRIM_INIT(n) # O(n*logn)
    Adj = MAKE_ADJ(G) # O(n + m)

    while not Q.isEmpty():
        u = EXTRACT_MIN(Q)

        node = Adj[u]
        while node:
            v = node.value
            # the graph is undirected (לא מכוון), so we check for both orders
            w = W(u, v)

            if Q.exists(v) and w < key[v]:
                key[v] = w
                P[v] = u
                Q.decreaseKey(v, key[v])

            node = node.next

    MST = BUILD_GRAPH_FROM_PARENTS_LIST(P, n)
    return MST

# Time Complexity: O(n)
# explanation:
# (u,v) in a MST completes a circle with the shortest path from u to v, therefore
# We want to extract from the circle the edge with the highest weight, in order to get the new MST
def Q2_FIND_NEW_MST(MST, W, newEdge, w):
    # 1. init
    # Time Complexity: O(1)
    v = newEdge[0]
    u = newEdge[1]

    # 2. get the shortest path between u and v
    # Time Complexity: O(n)
    # explanation: m = n-1 in MST, therefore the time complexity = O(n + m) = O(2n - 1) = O(n)
    MST_Adj = MAKE_ADJ(MST)
    shortestPath = GET_SHORTEST_PATH(MST_Adj, u, v)

    # 3. find the edge with the highest weight in the circle 
    # Time Complexity: O(n)
    # explanation: O(|shortestPath|) = O(n-1) = O(n)
    max = w
    edgeToRemove = newEdge
    for edge in shortestPath:
        weight = W(edge[0], edge[1])
        if weight > max:
            max = weight
            edgeToRemove = edge

    # 4. extract the edge with the highest weight in the circle
    # Time Complexity: O(1)
    # if edge to replace is the new edge then no change made to mst
    if edgeToRemove == (u, v) or edgeToRemove == (v, u):
        return MST
    
    # else we update the edge's set of the MST with those we found before
    V = MST['V']
    E = MST['E']
    
    updatedE = E.add(newEdge)
    updatedE = E.remove(edgeToRemove)
    updatedMST = {
        'V': V,
        'E': updatedE
    }

    # 5. return the updated MST
    return updatedMST

# the Graph must be connected, and undirected (לא מכוון וקשיר)
def GENERATE_GRAPH_WITH_WEIGHTS(minN, maxN):
    n = random.randint(minN, maxN)
    maxM = random.randint(n-1, n*(n-1)//2)
    weightsList = GENERATE_WEIGHTS(maxM)
    W = graph.WeightsFucntion()

    # generate vertices - O(n)
    V = list(range(n))
    Adj = graph.AdjList(n)

    # time complexity: O(n)
    # firstly we generate a connected graph with n-1 edges
    connected = [random.choice(V)]
    remaining = set(V) - set(connected)

    while remaining:
        u = random.choice(connected)
        v = random.choice(list(remaining))
        Adj.addEdge(u, v)
        W.addEdge(u, v, weightsList.pop())
        connected.append(v)
        remaining.remove(v)

    # add the rest edges randomly (up to maxM)
    totalEdgesAdded = n - 1
    fullV = set()
    while totalEdgesAdded < maxM:
        availableV = set(V) - fullV
        v = random.choice(list(availableV))

        # find list of available edges to connect to vertex v
        availableEdges = GET_AVAILABLE_EDGES(Adj, v, V)
        if not availableEdges:
            fullV.add(v)
            if fullV == set(V):
                break
            continue

        # add randomely availabe edges
        numEdgesToAdd = random.randint(1, min(len(availableEdges), maxM - totalEdgesAdded))
        for _ in range(numEdgesToAdd):
            e = random.choice(list(availableEdges))
            Adj.addEdge(*e) # unpack the tuple e
            W.addEdge(e[0], e[1], weightsList.pop())
            availableEdges.remove(e)
            totalEdgesAdded += 1
            if totalEdgesAdded == maxM:
                return Adj, W
    return Adj, W

G, W = GENERATE_GRAPH_WITH_WEIGHTS(3, 10)
G.printAndWeights(W)
print()
MST = MST_PRIM(G, W)
print("MST graph:")
MST.printAndWeights(W)
print()

# find an available edge in a graph
V = set(range(0, G.numVertices))
newEdge = None
fullV = set()
while len(fullV) < len(V):
    v = random.choice(list(V-fullV))
    availableEdges = GET_AVAILABLE_EDGES(G, v, V)
    if not availableEdges:
        fullV.add(v)
        if fullV == set(V):
            break
        continue
    else:
        newEdge = random.choice(list(availableEdges))
        break

if len(fullV) >= len(V):
    raise Exception("The graph has no available edges to add.")

# get the shortest path
path = GET_SHORTEST_PATH(MST, newEdge[0], newEdge[1])

# find the max in the shortest path
maxWeight = max(W(e[0], e[1]) for e in path)

# for doesn't change the MST choose the weight for edge to be max plus 1 (more than max)
print(f"new edge that has no effect on the MST: ({chr(newEdge[0] + 97)}, {chr(newEdge[1] + 97)}) w:", maxWeight + 1)
Q3_NO = Q2_FIND_NEW_MST(MST, W, newEdge, maxWeight + 1)
updatedW = W
updatedW.addEdge(newEdge[0], newEdge[1], maxWeight + 1)
Q3_NO.printAndWeights(updatedW)
print()
# for change the MST choose the weight for edge to be max minus 1 (less than max)
print(f"new edge that has effect on the MST: ({chr(newEdge[0] + 97)}, {chr(newEdge[1] + 97)}) w:", maxWeight - 1)
Q3_YES = Q2_FIND_NEW_MST(MST, W, newEdge, maxWeight - 1)
updatedW = W.copy()
updatedW.addEdge(newEdge[0], newEdge[1], maxWeight - 1)
Q3_YES.printAndWeights(updatedW)

# REPLACE ALL G with adj, and the G should be G=('V':[0,...,n],'E':{...})