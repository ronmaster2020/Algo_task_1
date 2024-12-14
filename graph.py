class Node:
    def __init__(self, value, weight):
        self.value = value
        self.weight = weight
        self.next = None

class Graph:
    def __init__(self, numVertices):
        self.adjList = [None] * numVertices

    def addEdge(self, src, dest, weight):
        newNode = Node(dest, weight)
        newNode.next = self.adjList[src]
        self.adjList[src] = newNode

        newNode = Node(src, weight)
        newNode.next = self.adjList[dest]
        self.adjList[dest] = newNode

    def weight(self, src, dest):
        temp = self.adjList[src]
        while temp:
            if temp.value == dest:
                return temp.weight
        return None

    def print(self):
        for i in range(len(self.adjList)):
            vertexLabel = chr(i + ord('a')) if 0 <= i < 26 else str(i)
            print(f"Adjacency list of vertex {vertexLabel}:", end="")
            temp = self.adjList[i]
            while temp:
                neighborLabel = chr(temp.value + ord('a')) if 0 <= temp.value < 26 else str(temp.value)
                print(f" -> {neighborLabel}(w: {temp.weight})", end="")
                temp = temp.next
            print()

    def MST_PRIM(self, r):
        pass