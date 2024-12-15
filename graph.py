import heapq
class Node:
    def __init__(self, value, weight):
        self.value = value
        self.weight = weight
        self.next = None

class AdjList:
    def __init__(self, numVertices):
        self.adjList = [None] * numVertices

    def addEdge(self, src, dest, weight):
        newNode = Node(dest, weight)
        newNode.next = self.adjList[src]
        self.adjList[src] = newNode

        newNode = Node(src, weight)
        newNode.next = self.adjList[dest]
        self.adjList[dest] = newNode

    def print(self):
        print("Graph is represented by Adjacency List:")
        for i in range(len(self.adjList)):
            vertexLabel = chr(i + ord('a')) if 0 <= i < 26 else str(i)
            print(f"{vertexLabel}:", end="")
            temp = self.adjList[i]
            while temp:
                neighborLabel = chr(temp.value + ord('a')) if 0 <= temp.value < 26 else str(temp.value)
                print(f" -> {neighborLabel}(w: {temp.weight})", end="")
                temp = temp.next
            print()

# Time complexities:
# init - O(n)
# addEdge - O(1)
# print - O(n + m)

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
# init - O(1)
# push - O(logn)
# pop - O(logn)
# decreaseKey - O(logn)
# isEmpty - O(1)
# exists - O(1)