import heapq
from collections import deque
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class AdjList:
    def __init__(self, numVertices):
        self.adjList = [None] * numVertices
        self.numVertices = numVertices

    def addEdge(self, src, dest):
        newNode = Node(dest)
        newNode.next = self.adjList[src]
        self.adjList[src] = newNode

        newNode = Node(src)
        newNode.next = self.adjList[dest]
        self.adjList[dest] = newNode

    def removeEdge(self, src, dest):
        self.adjList[src] = self._removeNode(self.adjList[src], dest)
        self.adjList[dest] = self._removeNode(self.adjList[dest], src)
        
    def _removeNode(self, head, value):
        # Helper function to remove a node with the given value from the linked list
        dummy = Node(0)
        dummy.next = head
        prev, curr = dummy, head
        while curr:
            if curr.value == value:
                prev.next = curr.next
                break
            prev, curr = curr, curr.next
        return dummy.next

    def print(self):
        print("Graph is represented by Adjacency List:")
        for i in range(len(self.adjList)):
            vertexLabel = chr(i + ord('a')) if 0 <= i < 26 else str(i)
            print(f"{vertexLabel}:", end="")
            temp = self.adjList[i]
            while temp:
                neighborLabel = chr(temp.value + ord('a')) if 0 <= temp.value < 26 else str(temp.value)
                print(f" -> {neighborLabel}", end="")
                temp = temp.next
            print()

    def printAndWeights(self, W):
        print("Graph is represented by Adjacency List And Weights:")
        for i in range(len(self.adjList)):
            vertexLabel = chr(i + ord('a')) if 0 <= i < 26 else str(i)
            print(f"{vertexLabel}:", end="")
            temp = self.adjList[i]
            while temp:
                neighborLabel = chr(temp.value + ord('a')) if 0 <= temp.value < 26 else str(temp.value)
                weight = W(i, temp.value)
                print(f" -> {neighborLabel} (w:{weight})", end="")
                temp = temp.next
            print()
    
    def BFS(self, s):
        # init
        n = len(self.adjList)
        visited = [False] * n
        d = [float('inf')] * n
        p = [None] * n
        visited[s] = True
        d[s] = 0
        Q = deque()
        Q.append(s)
        # end of init

        while len(Q) != 0:
            u = Q.popleft()
            node = self.adjList[u]
            while node:
                v = node.value
                if not visited[v]:
                    visited[v] = True
                    d[v] = d[u] + 1
                    p[v] = u
                    Q.append(v)
                node = node.next
        return d, p
    
    @staticmethod
    def BFS_PRINT(d, p):
        # for the rest
        for parent in range(1,len(p)):
            if p[parent] == None:
                print(f"{chr(parent + ord('a'))} (0) <- None")
            else:
                print(f"{chr(parent + ord('a'))} ({d[parent]}) <- {chr(p[parent] + ord('a'))}")

# Time complexities:
# *** we assume that n = |V|, and m = |E|
# init - O(n)
# addEdge - O(1)
# removeEdge - O(deg(vertex)) <= O(n)
# _removeEdge - O(deg(vertex)) <= O(n)
# print - O(n + m)
# printAndWeights - O(n + m)
# BFS - O(n + m)
# BFS_PRINT - O(n)

class MinHeap:
    def __init__(self):
        self.heap = []
        self.position = {}

    def push(self, vertex, key):
        heapq.heappush(self.heap, (key, vertex))
        self.position[vertex] = key

    def pop(self):
        while self.heap:
            key, vertex = heapq.heappop(self.heap)
            if self.position.get(vertex) == key:
                del self.position[vertex]
                return key, vertex
        raise KeyError("pop from empty queue")

    def decreaseKey(self, vertex, new_key):
        if vertex in self.position and new_key < self.position[vertex]:
            self.position[vertex] = new_key
            heapq.heappush(self.heap, (new_key, vertex))

    def isEmpty(self):
        return not self.position
    
    def exists(self, vertex):
        return vertex in self.position

# Time complexities:
# *** we assume that n = |V|, and m = |E|
# init - O(1)
# push - O(logn)
# pop - O(logn)
# decreaseKey - O(logn)
# isEmpty - O(1)
# exists - O(1)

class WeightsFucntion:
    def __init__(self):
        self.W = {}
    
    def addEdge(self, u, v, w):
        self.W[(u, v)] = w
        self.W[(v, u)] = w
    
    def removeEdge(self, u, v):
        if (u, v) in self.W:
            del self.W[(u, v)]
        if (v, u) in self.W:
            del self.W[(v, u)]
    
    def __call__(self, u, v):
        return self.W.get((u, v), self.W.get((v, u)))
    
    def copy(self):
        newWeights = WeightsFucntion()
        newWeights.W = self.W.copy()
        return newWeights