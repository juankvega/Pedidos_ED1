class Nodo():
    def __init__(self, dato):
        self.dato = dato
        self.siguiente:Nodo = None

class Cola():
    def __init__(self):
        self.head:Nodo = None
        self.tail:Nodo = None
        self.size = 0
    def enqueue(self, dato):
        nuevo_nodo = Nodo(dato)
        if self.head is None:
            self.head = self.tail = nuevo_nodo
        else:
            self.tail.siguiente = nuevo_nodo
            self.tail = nuevo_nodo
        self.size += 1
    def dequeue(self):
        if self.head is None:
            return None
        dato = self.head.dato
        self.head = self.head.siguiente
        if self.head is None:
            self.tail = None
        self.size -= 1
        return dato
    def show(self):
        tmp = self.head
        while tmp is not None:
            print(tmp.dato, end=" -> ")
            tmp = tmp.siguiente
        print("None", end="\n")