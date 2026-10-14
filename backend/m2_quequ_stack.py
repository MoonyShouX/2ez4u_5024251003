class StackNode:
    def __init__(self, data):
        self.data = data
        self.next = None

class Stack:
    def __init__(self):
        self.top = None
        self.ukuran = 0

    def push(self, data):
        node_baru = StackNode(data)
        node_baru.next = self.top
        self.top = node_baru
        self.ukuran += 1

    def pop(self):
        if self.top is None:
            return None
        data_keluar = self.top.data
        self.top = self.top.next
        self.ukuran -= 1
        return data_keluar

    def peek(self):
        if self.top is None:
            return None
        return self.top.data

    def is_empty(self):
        return self.top is None


class QueueNode:
    def __init__(self, data):
        self.data = data
        self.next = None

class Queue:
    def __init__(self):
        self.front = None
        self.rear = None
        self.ukuran = 0

    def enqueue(self, data):
        node_baru = QueueNode(data)
        if self.rear is None:
            self.front = self.rear = node_baru
        else:
            self.rear.next = node_baru
            self.rear = node_baru
        self.ukuran += 1

    def dequeue(self, data):
        if self.front is None:
            return None
        data_keluar = self.front.data
        self.front = self.front.next
        if self.front is None:
            self.rear = None
        self.ukuran -= 1
        return data_keluar

    def peek(self):
        if self.front is None:
            return None
        return self.front.data

    def is_empty(self):
        return self.front is None