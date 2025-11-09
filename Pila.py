from Nodo import Nodo

class Pila:
    """
    Implementación de una pila (Stack) usando una lista enlazada.
    """
    def __init__(self):
        self.cima = None
        self.tamano = 0

    def apilar(self, dato):
        """Agrega un elemento a la cima de la pila."""
        nuevo_nodo = Nodo(dato)
        nuevo_nodo.siguiente = self.cima
        self.cima = nuevo_nodo
        self.tamano += 1

    def desapilar(self):
        """
        Elimina y retorna el elemento en la cima de la pila.
        Retorna None si la pila está vacía.
        """
        if self.esta_vacia():
            return None
        dato = self.cima.dato
        self.cima = self.cima.siguiente
        self.tamano -= 1
        return dato
    
    def esta_vacia(self):
        """Verifica si la pila está vacía."""
        return self.tamano == 0