import sys

RESET_CHAR = "\033[0m"


def print_block(color: str) -> None:
    """Prints a colored block based on the color string."""
    # Simplified for testing: just print first letter of color
    print(color[0].upper(), end="")


class Node:
    """
    Represents a node in a singly linked list.

    Instance Variables:
        data: The value or data stored in the node.
        next: The reference to the next node in the linked list (None by default).
    """

    def __init__(self, data, link=None):
        self.data = data
        self.next = link
        if link is not None and not isinstance(link, Node):
            raise ValueError("Next must be a Node instance or None.")


class StackError(Exception):
    """An Exception raised when the Stack class performs an illegal operation"""


class Stack:
    """
    A class that implements a stack using a singly linked list.

    Instance Variables:
        _top: The top node of the stack.
        _size: The number of elements in the stack.
    """

    def __init__(self):
        """Initializes an empty stack with no elements."""
        self._top = None
        self._size = 0

    def peek(self):
        if self.is_empty():
            raise StackError("Peek from empty stack.")
        return self._top.data

    def push(self, item):
        new_node = Node(item, self._top)
        self._top = new_node
        self._size += 1

    def pop(self):
        if self.is_empty():
            raise StackError("Pop from empty stack.")
        data = self._top.data
        self._top = self._top.next
        self._size -= 1
        return data

    def is_empty(self):
        return self._size == 0

    def size(self):
        return self._size


class QueueError(Exception):
    """An Exception raised when the Queue class performs an illegal operation"""


class Queue:
    """
    A class that implements a queue using a singly linked list.

    Instance Variables:
        _front: The front node of the queue.
        _rear: The rear node of the queue.
        _size: The number of elements in the queue.
    """

    def __init__(self):
        """Initializes an empty queue with no elements."""
        self._front = None
        self._rear = None
        self._size = 0

    def peek(self):
        if self.is_empty():
            raise QueueError("Peek from empty queue.")
        return self._front.data

    def enqueue(self, item):
        new_node = Node(item)
        if self.is_empty():
            self._front = new_node
            self._rear = new_node
        else:
            self._rear.next = new_node
            self._rear = new_node
        self._size += 1

    def dequeue(self):
        if self.is_empty():
            raise QueueError("Dequeue from empty queue.")
        data = self._front.data
        self._front = self._front.next
        if self._front is None:
            self._rear = None
        self._size -= 1
        return data

    def is_empty(self):
        return self._size == 0

    def size(self):
        return self._size


class ColoredVertex:
    """Class for a graph vertex."""

    def __init__(self, index, x, y, color):
        self.index = index
        self.color = color
        self.prev_color = color
        self.x = x
        self.y = y
        self.edges = []
        self.visited = False

    def add_edge(self, vertex_index):
        """Add an edge to another vertex."""
        self.edges.append(vertex_index)

    def visit_and_set_color(self, color):
        """Set the color of the vertex and mark it visited."""
        self.visited = True
        self.prev_color = self.color
        self.color = color
        print("Visited vertex " + str(self.index))

    def __str__(self):
        return f"index: {self.index}, color: {self.color}, x: {self.x}, y: {self.y}"


class ImageGraph:
    """Class for the graph."""

    def __init__(self, image_size):
        self.vertices = []
        self.image_size = image_size

    def print_image(self):
        """Print the image formed by the vertices."""
        img = [["black" for _ in range(self.image_size)] for _ in range(self.image_size)]
        for vertex in self.vertices:
            img[vertex.y][vertex.x] = vertex.color
        for line in img:
            for pixel in line:
                print_block(pixel)
            print()
        print(RESET_CHAR)

    def reset_visited(self):
        """Reset the visited flag for all vertices."""
        for vertex in self.vertices:
            vertex.visited = False

    def create_adjacency_matrix(self):
        """Creates and returns the adjacency matrix for the graph."""
        n = len(self.vertices)
        matrix = [[0 for _ in range(n)] for _ in range(n)]
        for v in self.vertices:
            for nbr in v.edges:
                matrix[v.index][nbr] = 1
        return matrix

    def bfs(self, start_index, color):
        """Performs BFS bucket fill using a queue."""
        self.reset_visited()
        print("Starting BFS; initial state:")
        self.print_image()
        orig_color = self.vertices[start_index].color
        q = Queue()
        q.enqueue(start_index)
        self.vertices[start_index].visit_and_set_color(color)
        while not q.is_empty():
            current = q.dequeue()
            for nbr_idx in self.vertices[current].edges:
                nbr = self.vertices[nbr_idx]
                if not nbr.visited and nbr.color == orig_color:
                    q.enqueue(nbr_idx)
                    nbr.visit_and_set_color(color)
        print("BFS complete. Final state:")
        self.print_image()

    def dfs(self, start_index, color):
        """Performs DFS bucket fill using a stack without recursion."""
        self.reset_visited()
        print("Starting DFS; initial state:")
        self.print_image()
        orig_color = self.vertices[start_index].color
        s = Stack()
        s.push(start_index)
        self.vertices[start_index].visit_and_set_color(color)
        while not s.is_empty():
            current = s.pop()
            for nbr_idx in self.vertices[current].edges:
                nbr = self.vertices[nbr_idx]
                if not nbr.visited and nbr.color == orig_color:
                    s.push(nbr_idx)
                    nbr.visit_and_set_color(color)
        print("DFS complete. Final state:")
        self.print_image()


def create_graph(data: str):
    """Creates an ImageGraph from input data."""
    lines = [line.strip() for line in data.strip().splitlines() if line.strip()]
    idx = 0
    image_size = int(lines[idx]); idx += 1
    num_vertices = int(lines[idx]); idx += 1
    graph = ImageGraph(image_size)
    for i in range(num_vertices):
        x_str, y_str, col = lines[idx].split(', ')
        x, y = int(x_str), int(y_str)
        graph.vertices.append(ColoredVertex(i, x, y, col))
        idx += 1
    num_edges = int(lines[idx]); idx += 1
    for _ in range(num_edges):
        u_str, v_str = lines[idx].split(', ')
        u, v = int(u_str), int(v_str)
        graph.vertices[u].add_edge(v)
        graph.vertices[v].add_edge(u)
        idx += 1
    start_str, color = lines[idx].split(', ')
    start_index = int(start_str)
    return graph, start_index, color


def main():
    data = sys.stdin.read()
    graph, start, color = create_graph(data)
    matrix = graph.create_adjacency_matrix()
    print(matrix)
    graph.bfs(start, color)
    print()
    graph, start, color = create_graph(data)
    graph.dfs(start, color)


if __name__ == "__main__":
    main()
