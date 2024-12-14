class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class Graph:
    def __init__(self, numVertices):
        self.adjList = [None] * numVertices

    def addEdge(self, src, dest):
        newNode = Node(dest)
        newNode.next = self.adjList[src]
        self.adjList[src] = newNode

        newNode = Node(src)
        newNode.next = self.adjList[dest]
        self.adjList[dest] = newNode

    def print(self):
        for i in range(len(self.adjList)):
            print(f"Adjacency list of vertex {i}:", end="")
            temp = self.adjList[i]
            while temp:
                print(f" -> {temp.value}", end="")
                temp = temp.next
            print()