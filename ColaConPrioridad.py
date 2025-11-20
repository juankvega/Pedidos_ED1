class ColaConPrioridad:
    def __init__(self, key_func=None):
        self.items = []
        self.key_func = key_func if key_func else lambda x: x[0] if isinstance(x, tuple) else x

    def encolar(self, item):
        """Encola un elemento manteniendo el orden de prioridad."""
        if self.estaVacia():
            self.items.append(item)
        else:
            prioridad_nueva = self.key_func(item)
            insertado = False
            
            for i in range(len(self.items)):
                prioridad_actual = self.key_func(self.items[i])
                if prioridad_nueva < prioridad_actual:
                    self.items.insert(i, item)
                    insertado = True
                    break
            
            if not insertado:
                self.items.append(item)

    def desencolar(self):
        """Desencola el elemento con mayor prioridad (menor valor)."""
        if not self.estaVacia():
            return self.items.pop(0)
        return None

    def imprimir(self):
        """Imprime todos los elementos de la cola."""
        if not self.estaVacia():
            print(self.items)

    def estaVacia(self):
        """Verifica si la cola esta vacia."""
        return len(self.items) == 0

    def ver_frente(self):
        """Retorna el elemento al frente sin eliminarlo."""
        return self.items[0] if not self.estaVacia() else None

    def tamano(self):
        """Retorna el tamaño de la cola."""
        return len(self.items)
