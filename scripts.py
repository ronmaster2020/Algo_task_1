import graph
import random

# O(nlogn)
def PRIM_INIT(n):
    # init min heap
    minHeap = graph.MinHeap()
    # Initialize key values to infinity for all vertices.
    key = [float('inf')] * n
    # the first vertex intialized to 0
    key[0] = 0

    # O(nlogn)
    for v in range(n):
        minHeap.push(v, key[v])
    P = [None] * n
    
    return minHeap, key, P

# O(log(n)) - we asume that O(|Q|) = O(n)
def EXTRACT_MIN(Q):
    return (Q.pop())[1]

# O(n)
def BUILD_MST(P, n):
    MST = graph.AdjList(n)
    for v in range(0, n):
        if P[v] is not None:
            MST.addEdge(P[v], v)
    return MST

# O(m)
def GENERATE_WEIGHTS(m):
    weights = [random.randint(-100, 100) for _ in range(m)]
    return weights

# O(n)
def GET_AVAILABLE_EDGES(G, v, V):
    # O(1)
    neighbors = set()
    node = G.adjList[v]
    # O(n-1) = O(n)
    while node:
        neighbors.add(node.value)
        node = node.next

    available = set(V) - {v} - neighbors

    if not available: return None
    # O(n-1) = O(n)
    availableEdges = set()
    for u in available:
        availableEdges.add((u, v))

    return availableEdges

# O(n + m)
def GET_SHORTEST_PATH(G, u, v):
    # O(n + m)
    _,P = G.BFS(v)
    if P[u] == None:
        return None
    
    path = list()
    temp = u
    # O(n)
    while temp != v:
        if P[temp] == None:
            raise ValueError("No path exists")
        path.append((temp, P[temp]))
        temp = P[temp]

    # O(n)
    path.reverse()
    return path

# O(n + m)
def MAKE_ADJ(G):
    E = G['E']
    V = G['V']

    m = len(E)
    n = len(V)
    maxE = (n * (n-1)) // 2
    if m > maxE:
        raise ValueError("invalid amount of edges (|E| > |V|*(|V|-1)/2)")

    if not V: return None

    Adj = graph.AdjList(len(V))
    for edge in E:
        u = edge[0]
        v = edge[1]
        Adj.addEdge(u, v)
    return Adj