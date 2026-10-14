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

    def size(self):
        return self.ukuran

    def __len__(self):
        return self.ukuran


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

    def dequeue(self):
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

    def size(self):
        return self.ukuran

    def __len__(self):
        return self.ukuran


# Antrean naif: antrean di atas list biasa, geser elemen ke kiri saat dequeue O(n)
class AntreanNaif:
    def __init__(self):
        self.data = []
        self.total_geseran = 0
        self.geseran_terakhir = 0

    def enqueue(self, pesanan):
        self.data.append(pesanan)

    def dequeue(self):
        if len(self.data) == 0:
            return None
        pesanan_keluar = self.data[0]
        geseran = len(self.data) - 1
        self.total_geseran += geseran
        self.geseran_terakhir = geseran
        for i in range(len(self.data) - 1):
            self.data[i] = self.data[i + 1]
        self.data.pop()
        return pesanan_keluar

    def peek(self):
        if len(self.data) == 0:
            return None
        return self.data[0]

    def is_empty(self):
        return len(self.data) == 0

    def size(self):
        return len(self.data)

    def __len__(self):
        return len(self.data)


# Antrean melingkar: circular queue pakai pointer front, rear, count O(1)
class AntreanMelingkar:
    def __init__(self, kapasitas=32768):
        self.kapasitas = kapasitas
        self.data = [None] * self.kapasitas
        self.front = 0
        self.rear = 0
        self.count = 0
        self.total_geseran = 0
        self.geseran_terakhir = 0

    def enqueue(self, pesanan):
        if self.count == self.kapasitas:
            self._resize()
        self.data[self.rear] = pesanan
        self.rear = (self.rear + 1) % self.kapasitas
        self.count += 1

    def dequeue(self):
        if self.count == 0:
            return None
        pesanan_keluar = self.data[self.front]
        self.data[self.front] = None
        self.front = (self.front + 1) % self.kapasitas
        self.count -= 1
        self.geseran_terakhir = 0
        return pesanan_keluar

    def _resize(self):
        kapasitas_baru = self.kapasitas * 2
        data_baru = [None] * kapasitas_baru
        for i in range(self.count):
            data_baru[i] = self.data[(self.front + i) % self.kapasitas]
        self.data = data_baru
        self.front = 0
        self.rear = self.count
        self.kapasitas = kapasitas_baru

    def peek(self):
        if self.count == 0:
            return None
        return self.data[self.front]

    def is_empty(self):
        return self.count == 0

    def size(self):
        return self.count

    def __len__(self):
        return self.count


# Mesin Kasir: konversi infix ke postfix dan evaluasi ekspresi
def pecah_token(ekspresi):
    tokens = []
    i = 0
    n = len(ekspresi)
    while i < n:
        c = ekspresi[i]
        if c == ' ' or c == '\t':
            i += 1
            continue
        if c in '0123456789':
            angka = ''
            while i < n and ekspresi[i] in '0123456789':
                angka += ekspresi[i]
                i += 1
            tokens.append(angka)
            continue
        if c in '+-*/()':
            tokens.append(c)
            i += 1
            continue
        i += 1
    return tokens


def prioritas_operator(op):
    if op == '*' or op == '/':
        return 2
    if op == '+' or op == '-':
        return 1
    return 0


def ke_postfix(ekspresi):
    if isinstance(ekspresi, str):
        tokens = pecah_token(ekspresi)
    else:
        tokens = ekspresi

    stack_op = Stack()
    output = []

    for token in tokens:
        if token.isdigit():
            output.append(token)
        elif token == '(':
            stack_op.push(token)
        elif token == ')':
            while not stack_op.is_empty() and stack_op.peek() != '(':
                output.append(stack_op.pop())
            if not stack_op.is_empty() and stack_op.peek() == '(':
                stack_op.pop()
        elif token in ['+', '-', '*', '/']:
            while (not stack_op.is_empty() and
                   stack_op.peek() != '(' and
                   prioritas_operator(stack_op.peek()) >= prioritas_operator(token)):
                output.append(stack_op.pop())
            stack_op.push(token)

    while not stack_op.is_empty():
        output.append(stack_op.pop())

    return " ".join(output)


def hitung(postfix):
    if isinstance(postfix, str):
        tokens = postfix.split()
    else:
        tokens = postfix

    stack_angka = Stack()

    for token in tokens:
        if token.isdigit():
            stack_angka.push(int(token))
        elif token in ['+', '-', '*', '/']:
            b = stack_angka.pop()
            a = stack_angka.pop()
            if a is None or b is None:
                continue
            if token == '+':
                hasil = a + b
            elif token == '-':
                hasil = a - b
            elif token == '*':
                hasil = a * b
            elif token == '/':
                hasil = a // b if b != 0 else 0
            stack_angka.push(hasil)

    return stack_angka.pop()


# Pengelola undo/redo untuk antrean
class PengelolaAntrean:
    def __init__(self, mode='circular'):
        if mode == 'circular':
            self.antrean = AntreanMelingkar()
        else:
            self.antrean = AntreanNaif()
        self.stack_undo = Stack()
        self.stack_redo = Stack()

    def enqueue(self, pesanan):
        self.antrean.enqueue(pesanan)
        self.stack_undo.push(('ENQUEUE', pesanan))
        while not self.stack_redo.is_empty():
            self.stack_redo.pop()

    def dequeue(self):
        pesanan = self.antrean.dequeue()
        if pesanan is not None:
            self.stack_undo.push(('DEQUEUE', pesanan))
            while not self.stack_redo.is_empty():
                self.stack_redo.pop()
        return pesanan

    def undo_last(self):
        if self.stack_undo.is_empty():
            return None
        aksi, pesanan = self.stack_undo.pop()
        self.stack_redo.push((aksi, pesanan))
        return aksi, pesanan

    def redo_last(self):
        if self.stack_redo.is_empty():
            return None
        aksi, pesanan = self.stack_redo.pop()
        self.stack_undo.push((aksi, pesanan))
        return aksi, pesanan