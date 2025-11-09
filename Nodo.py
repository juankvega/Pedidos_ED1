# Nodo para usar en las listas, pilas y colas.
class Nodo:
    """
    Clase que representa un nodo en una estructura de datos enlazada.
    Puede almacenar cualquier tipo de dato.
    """
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None