class ColaConPrioridad:
    def __init__(self):
        self.items = []

    def encolar(self, item):
        # Suponiendo que item es una tupla (prioridad, valor)
        if self.esta_vacia():
            self.items.append(item)
        else:
            insertado = False
            for i in range(len(self.items)):
                if item[0] < self.items[i][0]:
                    self.items.insert(i, item)
                    insertado = True
                    break
            if not insertado:
                self.items.append(item)

    def desencolar(self):
        if not self.esta_vacia():
            return self.items.pop(0)
        return None

    def imprimir(self):
        if not self.esta_vacia():
            print(self.items)

    def esta_vacia(self):
        return len(self.items) == 0

    def ver_frente(self):
        return self.items[0] if not self.esta_vacia() else None

    def tamano(self):
        return len(self.items)
