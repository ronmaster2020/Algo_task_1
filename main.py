from scripts import PRIM_INIT, EXTRACT_MIN, BUILD_GRAPH_FROM_PARENTS_LIST, GENERATE_WEIGHTS, GET_AVAILABLE_EDGES, GET_SHORTEST_PATH, MAKE_ADJ
import random
import graph
import copy

# The main execution:
def main():
    # SAIF 1:
    G, W = GENERATE_GRAPH_WITH_WEIGHTS(20, 26)
    Adj = MAKE_ADJ(G)
    Adj.printAndWeights(W)

    # SAIF 2:
    MST = MST_PRIM(G, W)
    print("MST graph:")
    MST_Adj = MAKE_ADJ(MST)
    MST_Adj.printAndWeights(W)

    # SAIF 3:
    # 1. find an available edge to add, in the graph
    newEdge = None
    V = G['V']
    n = len(V)
    for v in range(n):
        availableEdges = GET_AVAILABLE_EDGES(Adj, v, V)
        if not availableEdges:
            continue
        newEdge = availableEdges.pop()
        break

    if not newEdge:
        raise Exception("The graph if full, no available edges to add.")

    # 2. get the shortest path
    shortestPath = GET_SHORTEST_PATH(MST, *newEdge)

    # 3. find the max in the shortest path
    maxWeight = max(W(*edge) for edge in shortestPath)

    # 4. the final step splits into two requests:

    # קשת הלא משנה את העץ הפורס המינימלי
    # for doesn't change the MST choose the weight for edge to be max plus 1 (more than max)
    newWeight = maxWeight + 1
    print(f"new edge that has NO effect on the MST: ({chr(newEdge[0] + 97)}, {chr(newEdge[1] + 97)}) w:", newWeight)
    Q3_NO = Q2_FIND_NEW_MST(MST, W, newEdge, newWeight)
    updatedW = W
    updatedW.addEdge(newEdge, newWeight)
    Q3_NO_Adj = MAKE_ADJ(Q3_NO)
    Q3_NO_Adj.printAndWeights(updatedW)

    # קשת המשנה את העץ הפורס המינימלי
    # for change the MST choose the weight for edge to be max minus 1 (less than max)
    newWeight = maxWeight - 1
    print(f"new edge that has effect on the MST: ({chr(newEdge[0] + 97)}, {chr(newEdge[1] + 97)}) w:", newWeight)
    Q3_YES = Q2_FIND_NEW_MST(MST, W, newEdge, newWeight)
    updatedW = W
    updatedW.addEdge(newEdge, newWeight)
    Q3_YES_Adj = MAKE_ADJ(Q3_YES)
    Q3_YES_Adj.printAndWeights(updatedW)


# |-------------------------------------------------------|
# |============= FUNCTION'S IMPLEMENTATION ===============|
# |-------------------------------------------------------|

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
    v = newEdge[0]
    u = newEdge[1]

    # 2. get the shortest path between u and v
    shortestPath = GET_SHORTEST_PATH(MST, u, v)

    # 3. find the edge with the highest weight in the circle 
    max = w
    edgeToRemove = newEdge
    for edge in shortestPath:
        weight = W(*edge)
        if weight > max:
            max = weight
            edgeToRemove = edge

    # 4. extract the edge with the highest weight in the circle
    if edgeToRemove == (u, v) or edgeToRemove == (v, u):
        return MST
    
    # 5. modify the new mst
    newMST = copy.deepcopy(MST)
    newMST['E'].add(newEdge)
    newMST['E'].remove(edgeToRemove)

    # 6. return the new MST
    return newMST

# Time Complexity: O(n^2)
# the Graph must be connected, and undirected (לא מכוון וקשיר)
def GENERATE_GRAPH_WITH_WEIGHTS(minN, maxN):
    # 1. init - O(n^2)
    n = random.randint(minN, maxN)
    maxM = random.randint(n-1, n*(n-1)//2)
    weightsList = GENERATE_WEIGHTS(maxM)
    assert len(weightsList) >= maxM, "Not enough weights for the edges"

    W = graph.WeightsFucntion()
    V = list(range(n))
    E = set()
    allEdges = set([(i, j) for i in range(n) for j in range(i + 1, n)])
    totalEdgesAdded = 0

    # 2. we generate a spanning tree
    # time complexity: O(n^2)
    connected = [random.choice(V)]
    remaining = list(set(V) - set(connected))

    while remaining:
        v = random.choice(remaining)
        u = random.choice(connected)
        newEdge = (u, v)
        if v < u:
            newEdge = (v, u)
        E.add(newEdge)
        W.addEdge(newEdge, weightsList.pop())
        allEdges.remove(newEdge)
        connected.append(v)
        remaining.remove(v)
        totalEdgesAdded += 1

    # 3. add the rest edges up to maxM - O(n^2)
    numberEdgesToAdd = maxM - totalEdgesAdded
    for _ in range(numberEdgesToAdd):
        newEdge = allEdges.pop()
        E.add(newEdge)
        W.addEdge(newEdge, weightsList.pop())

    # 4. and finally return the graph, with the weights fucntion
    G = {
        'V': V,
        'E': E
    }
    return G, W


if __name__ == '__main__':
    main()