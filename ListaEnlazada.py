from Nodo import Nodo

class ListaEnlazada:
    """
    Implementación de una lista simple enlazada.
    Permite agregar elementos y obtenerlos por índice.
    """
    def __init__(self):
        self.cabeza = None
        self.tamano = 0

    def agregar(self, dato):
        """Agrega un nuevo elemento al final de la lista."""
        nuevo_nodo = Nodo(dato)
        if self.cabeza is None:
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente is not None:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo
        self.tamano += 1

    def obtener(self, indice):
        """
        Obtiene un elemento por su índice.
        Retorna el dato en el índice especificado o None si está fuera de rango.
        """
        if indice < 0 or indice >= self.tamano:
            return None
        actual = self.cabeza
        for i in range(indice):
            actual = actual.siguiente
        return actual.dato

    def obtener_tamano(self):
        """Retorna el tamaño actual de la lista."""
        return self.tamano
    
    def obtener_cabeza(self):
        """Retorna el nodo cabeza de la lista."""
        return self.cabeza