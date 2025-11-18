from typing import List, Set

from Cola import Cola, ColaConPrioridad

# Vértice o Nodo
class Vertice:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente: Vertice = None
        self.listaAdyacencia = ListaAdyacencia()

    def __str__(self):
        return str(self.dato)

# Arista o Arco
class Arista:
    def __init__(self, destino: Vertice, peso = None):
        self.peso = peso
        self.siguiente: Arista = None
        self.destino = destino


# Lista de Adyacencia
class ListaAdyacencia:
    def __init__(self):
        self.primera: Arista = None
        self.ultima: Arista = None

    def esVacia(self):
        return self.primera is None

    def buscarAdyacencia(self, destino: Vertice):
        temporal = self.primera
        while temporal is not None:
            if str(temporal.destino) == str(destino):
                return True
            temporal = temporal.siguiente
        return False

    def agregar(self, destino: Vertice, peso = None):
        if not self.buscarAdyacencia(destino):
            self.agregarArista(Arista(destino, peso))

    def agregarArista(self, nuevaArista: Arista):
        if self.esVacia():
            self.primera = nuevaArista
            self.ultima = nuevaArista
            return

        dato = str(nuevaArista.destino)

        if dato < str(self.primera.destino):
            nuevaArista.siguiente = self.primera
            self.primera = nuevaArista
            return

        if dato > str(self.primera.destino):
            self.ultima.siguiente = nuevaArista
            self.ultima = nuevaArista
            return

        temporal = self.primera
        while temporal.siguiente is not None and dato > str(temporal.destino):
            temporal = temporal.siguiente

        nuevaArista.siguiente = temporal.siguiente
        temporal.siguiente = nuevaArista

    def eliminar(self, destino: Vertice):
        if self.esVacia():
            return

        if str(self.primera.destino) == str(destino):
            self.primera = self.primera.siguiente
            if self.primera is None:
                self.ultima = None
            return

        temporal = self.primera
        
        while temporal.siguiente is not None and temporal.siguiente.destino.__str__() == str(destino):
            temporal = temporal.siguiente

        if temporal.siguiente is not None:
            temporal.siguiente = temporal.siguiente.siguiente
            if temporal.siguiente is None:
                self.ultima = temporal

class Grafo:
    def __init__(self):
        self.primero: Vertice = None
        self.ultimo: Vertice = None

    def agregarArista(self, origen, destino, peso = None):
        verticeOrigen = self.buscarVertice(origen)
        verticeDestino = self.buscarVertice(destino)
        if verticeOrigen is not None and verticeDestino is not None:
            verticeOrigen.listaAdyacencia.agregar(verticeDestino, peso)

    def eliminarArista(self, origen, destino):
        verticeOrigen = self.buscarVertice(origen)
        verticeDestino = self.buscarVertice(destino)
        if verticeOrigen is not None and verticeDestino is not None:
            verticeOrigen.listaAdyacencia.eliminar(verticeDestino)

    def agregarVertice(self, dato):
        if self.buscarVertice(dato) is not None:
            return

        nuevoVertice = Vertice(dato)
        if self.esVacio():
            self.primero = nuevoVertice
            self.ultimo = nuevoVertice
            return

        nuevoDato = str(dato)
        if nuevoDato < str(self.primero):
            nuevoVertice.siguiente = self.primero
            self.primero = nuevoVertice
            return

        if nuevoDato > str(self.primero):
            self.ultimo.siguiente = nuevoVertice
            self.ultimo = nuevoVertice
            return

        temporal = self.primero
        while temporal.siguiente is not None and nuevoDato > str(temporal):
            temporal = temporal.siguiente

        nuevoVertice.siguiente = temporal.siguiente
        temporal.siguiente = nuevoVertice

    def eliminarVertice(self, dato):
        if self.esVacio():
            return

        verticeBorrar: Vertice = None

        if str(self.primero) == str(dato):
            verticeBorrar = self.primero
            self.primero = self.primero.siguiente
            if self.primero is None:
                self.ultimo = None
        else:
            temporal = self.primero
            while temporal.siguiente is not None and temporal.siguiente.__str__() == str(dato):
                temporal = temporal.siguiente

            if temporal.siguiente is not None:
                verticeBorrar = temporal.siguiente
                temporal.siguiente = temporal.siguiente.siguiente
                if temporal.siguiente is None:
                    self.ultimo = temporal

        if verticeBorrar is not None:
            temporal = self.primero
            while temporal is not None:
                temporal.listaAdyacencia.eliminar(verticeBorrar)
                temporal = temporal.siguiente

    def esVacio(self):
        return self.primero is None

    def buscarVertice(self, dato):
        temporal = self.primero
        while temporal is not None:
            if str(temporal) == str(dato):
                return temporal
            temporal = temporal.siguiente
        return None

    def recorridoAnchura(self, dato):
        vertice = self.buscarVertice(dato)
        if vertice is None:
            return

        visitados = set()
        visitados.add(vertice)
        cola = Cola()
        cola.enqueue(vertice)

        while cola.getSize() > 0:
            verticeActual = cola.dequeue()
            print(f"{verticeActual},", end='')
            temporal = verticeActual.listaAdyacencia.primera
            while temporal is not None:
                if temporal.destino not in visitados:
                    visitados.add(temporal.destino)
                    cola.enqueue(temporal.destino)
                temporal = temporal.siguiente
        print()

    def recorridoProfundidad(self, dato):
        vertice = self.buscarVertice(dato)
        if vertice is None:
            return

        visitados = set()
        self._recorridoProfundidad(vertice, visitados)
        print()

    def _recorridoProfundidad(self, vertice: Vertice, visitados: Set[Vertice]):
        print(f"{vertice}", end=' ')
        visitados.add(vertice)

        aristaActual = vertice.listaAdyacencia.primera
        while aristaActual is not None:
            if aristaActual.destino not in visitados:
                self._recorridoProfundidad(aristaActual.destino, visitados)
            aristaActual = aristaActual.siguiente

    def Dijkstra(self, origen):
        verticeOrigen = self.buscarVertice(origen)
        if verticeOrigen is None:
            return None

        visitados = {}
        distancias = {}

        temporal = self.primero
        while temporal is not None:
            distancias[temporal] = float('inf')
            visitados[temporal] = False
            temporal = temporal.siguiente

        distancias[verticeOrigen] = 0.0

        cola = ColaConPrioridad(lambda v: distancias[v])
        cola.encolar(verticeOrigen)

        while not cola.estaVacia():
            actual = cola.desencolar()

            if visitados.get(actual, False):
                continue

            visitados[actual] = True

            aristaActual = actual.listaAdyacencia.primera
            while aristaActual is not None:
                if not visitados.get(aristaActual.destino, False):
                    nuevaDistancia = distancias[actual] + float(aristaActual.peso)
                    if nuevaDistancia < distancias[aristaActual.destino]:
                        distancias[aristaActual.destino] = nuevaDistancia
                        cola.encolar(aristaActual.destino)
                aristaActual = aristaActual.siguiente

        return distancias

    def mostrarDistanciasDijkstra(self, origen):
        distancias = self.Dijkstra(origen)
        if distancias is not None:
            print(f"Distancias desde: {origen}")
            for k, v in distancias.items():
                print(f"{k.dato}:{v}")

    def bellman_ford(self, origen):
        vertice_origen = self.__buscar_vertice__(origen)
        if vertice_origen is None:
            return None

        # Inicializar distancias
        distancias = {}
        actual = self.primer
        while actual is not None:
            distancias[actual] = float('inf')
            actual = actual.siguiente
        distancias[vertice_origen] = 0.0

        # Relajación de aristas
        for _ in range(len(distancias) - 1):
            for vertice in distancias.keys():
                arista_actual = vertice.lista_adyacencia.primera
                while arista_actual is not None:
                    if distancias[vertice] + arista_actual.peso < distancias[arista_actual.destino]:
                        distancias[arista_actual.destino] = distancias[vertice] + arista_actual.peso
                    arista_actual = arista_actual.siguiente

        # Verificación de ciclos negativos
        for vertice in distancias.keys():
            arista_actual = vertice.lista_adyacencia.primera
            while arista_actual is not None:
                if distancias[vertice] + arista_actual.peso < distancias[arista_actual.destino]:
                    return "El grafo contiene un ciclo negativo."
                arista_actual = arista_actual.siguiente

        return distancias

    def mostrarDistanciaBellmanFord(self, origen):
        distancias = self.bellman_ford(origen)
        if distancias is not None:
            print(f"Distancias desde: {origen}")
            for k, v in distancias.items():
                print(f"{k.dato}:{v}")

    def FloydWarshall(self):
        vertices = []
        actual = self.primero
        while actual is not None:
            vertices.append(actual)
            actual = actual.siguiente

        n = len(vertices)
        distancias = [[float('inf')] * n for _ in range(n)]

        for i in range(n):
            distancias[i][i] = 0.0

        for i in range(n):
            aristaActual = vertices[i].listaAdyacencia.primera
            while aristaActual is not None:
                j = vertices.index(aristaActual.destino)
                distancias[i][j] = float(aristaActual.peso)
                aristaActual = aristaActual.siguiente

        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if distancias[i][k] != float('inf') and distancias[k][j] != float('inf'):
                        nuevo = distancias[i][k] + distancias[k][j]
                        if nuevo < distancias[i][j]:
                            distancias[i][j] = nuevo

        return distancias

    def mostrarDistanciasFloydWarshall(self):
        distancias = self.FloydWarshall()
        vertices: List[Vertice] = []
        temp = self.primero
        while temp is not None:
            vertices.append(temp)
            temp = temp.siguiente

        n = len(vertices)

        print("\t", end='')
        for v in vertices:
            print(f"{v.dato}\t", end='')
        print()

        for i in range(n):
            print(f"{vertices[i].dato}\t", end='')
            for j in range(n):
                valor = distancias[i][j]
                if valor == float('inf'):
                    print("INF\t", end='')
                else:
                    print(f"{valor}\t", end='')
            print()