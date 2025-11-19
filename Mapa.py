from Grafos.Grafo import Grafo, Vertice
from Grafos.ColaConPrioridad import ColaConPrioridad

class Zona:
    """
    Representa una zona en el mapa de la ciudad.
    Cada zona tiene un nombre y puede almacenar información adicional.
    """
    def __init__(self, nombre):
        self.nombre = nombre
        self.restaurantes = []  # Lista de restaurantes en esta zona
        self.domiciliarios = []  # Lista de domiciliarios en esta zona
        
    def __str__(self):
        return self.nombre
    
    def agregar_restaurante(self, restaurante):
        """Agrega un restaurante a esta zona."""
        self.restaurantes.append(restaurante)
    
    def agregar_domiciliario(self, domiciliario):
        """Agrega un domiciliario a esta zona."""
        self.domiciliarios.append(domiciliario)
    
    def remover_domiciliario(self, domiciliario):
        """Remueve un domiciliario de esta zona."""
        if domiciliario in self.domiciliarios:
            self.domiciliarios.remove(domiciliario)


class Mapa:
    """
    Representa el mapa de la ciudad como un grafo de zonas.
    Las zonas están conectadas por vías con distancias (pesos).
    """
    def __init__(self):
        self.grafo = Grafo()
        self.zonas = {}  # Diccionario para acceso rápido a las zonas
    
    def agregar_zona(self, nombre_zona):
        """
        Agrega una nueva zona al mapa.
        """
        if nombre_zona not in self.zonas:
            zona = Zona(nombre_zona)
            self.zonas[nombre_zona] = zona
            self.grafo.agregarVertice(nombre_zona)
            print(f"✓ Zona '{nombre_zona}' agregada al mapa")
            return True
        else:
            print(f"✗ La zona '{nombre_zona}' ya existe")
            return False
    
    def conectar_zonas(self, zona_origen, zona_destino, distancia):
        """
        Conecta dos zonas con una vía bidireccional.
        La distancia representa el peso de la arista.
        """
        if zona_origen in self.zonas and zona_destino in self.zonas:
            # Conexión bidireccional (grafo no dirigido)
            self.grafo.agregarArista(zona_origen, zona_destino, distancia)
            self.grafo.agregarArista(zona_destino, zona_origen, distancia)
            print(f"✓ Zonas '{zona_origen}' y '{zona_destino}' conectadas (distancia: {distancia})")
            return True
        else:
            print(f"✗ Una o ambas zonas no existen en el mapa")
            return False
    
    def obtener_zona(self, nombre_zona):
        """Retorna el objeto Zona si existe."""
        return self.zonas.get(nombre_zona)
    
    def calcular_distancias_desde(self, zona_origen):
        """
        Calcula las distancias más cortas desde una zona origen a todas las demás
        usando el algoritmo de Dijkstra.
        Retorna un diccionario con las distancias.
        """
        if zona_origen not in self.zonas:
            print(f"✗ La zona '{zona_origen}' no existe")
            return None
        
        distancias_vertices = self.grafo.Dijkstra(zona_origen)
        
        # Convertir el resultado de vértices a nombres de zonas
        distancias = {}
        for vertice, distancia in distancias_vertices.items():
            distancias[vertice.dato] = distancia
        
        return distancias
    
    def encontrar_zona_mas_cercana(self, zona_origen, zonas_candidatas):
        """
        Encuentra la zona más cercana de una lista de zonas candidatas
        desde una zona origen.
        Retorna una tupla (zona_mas_cercana, distancia).
        """
        distancias = self.calcular_distancias_desde(zona_origen)
        
        if distancias is None:
            return None, float('inf')
        
        zona_mas_cercana = None
        distancia_minima = float('inf')
        
        for zona_candidata in zonas_candidatas:
            if zona_candidata in distancias:
                if distancias[zona_candidata] < distancia_minima:
                    distancia_minima = distancias[zona_candidata]
                    zona_mas_cercana = zona_candidata
        
        return zona_mas_cercana, distancia_minima
    
    def mostrar_mapa(self):
        """Muestra todas las zonas y sus conexiones."""
        print("\n" + "="*50)
        print("MAPA DE LA CIUDAD")
        print("="*50)
        
        if not self.zonas:
            print("El mapa está vacío")
            return
        
        for nombre_zona, zona in self.zonas.items():
            print(f"\n Zona: {nombre_zona}")
            
            # Obtener el vértice correspondiente
            vertice = self.grafo.buscarVertice(nombre_zona)
            if vertice:
                arista_actual = vertice.listaAdyacencia.primera
                if arista_actual:
                    print("   Conexiones:")
                    while arista_actual is not None:
                        print(f"   → {arista_actual.destino.dato} (distancia: {arista_actual.peso})")
                        arista_actual = arista_actual.siguiente
                else:
                    print("   Sin conexiones")
            
            # Mostrar restaurantes y domiciliarios
            if zona.restaurantes:
                print(f"      Restaurantes: {len(zona.restaurantes)}")
            if zona.domiciliarios:
                print(f"      Domiciliarios disponibles: {len(zona.domiciliarios)}")
        
        print("="*50 + "\n")
    
    def mostrar_matriz_distancias(self):
        """Muestra la matriz de distancias entre todas las zonas."""
        print("\n" + "="*50)
        print("MATRIZ DE DISTANCIAS (Floyd-Warshall)")
        print("="*50 + "\n")
        self.grafo.mostrarDistanciasFloydWarshall()
        print()


# Ejemplo de uso y prueba
if __name__ == "__main__":
    # Crear el mapa
    mapa = Mapa()
    
    print("CREANDO MAPA DE LA CIUDAD\n")
    
    # Agregar zonas con nombres direccionales
    mapa.agregar_zona("Norte")
    mapa.agregar_zona("Sur")
    mapa.agregar_zona("Este")
    mapa.agregar_zona("Oeste")
    mapa.agregar_zona("Centro")
    mapa.agregar_zona("Noreste")
    mapa.agregar_zona("Noroeste")
    mapa.agregar_zona("Sureste")
    mapa.agregar_zona("Suroeste")
    
    print("\n CONECTANDO ZONAS\n")
    
    # Conectar zonas con distancias
    # Centro conecta con todos los puntos cardinales principales
    mapa.conectar_zonas("Centro", "Norte", 5)
    mapa.conectar_zonas("Centro", "Sur", 5)
    mapa.conectar_zonas("Centro", "Este", 5)
    mapa.conectar_zonas("Centro", "Oeste", 5)
    
    # Conexiones entre puntos cardinales
    mapa.conectar_zonas("Norte", "Noreste", 3)
    mapa.conectar_zonas("Norte", "Noroeste", 3)
    mapa.conectar_zonas("Sur", "Sureste", 3)
    mapa.conectar_zonas("Sur", "Suroeste", 3)
    mapa.conectar_zonas("Este", "Noreste", 3)
    mapa.conectar_zonas("Este", "Sureste", 3)
    mapa.conectar_zonas("Oeste", "Noroeste", 3)
    mapa.conectar_zonas("Oeste", "Suroeste", 3)
    
    # Conexiones adicionales para crear más caminos
    mapa.conectar_zonas("Noreste", "Sureste", 7)
    mapa.conectar_zonas("Noroeste", "Suroeste", 7)
    
    # Mostrar el mapa
    mapa.mostrar_mapa()
    
    # Probar cálculo de distancias
    print("\n CALCULANDO DISTANCIAS DESDE 'Centro'\n")
    distancias = mapa.calcular_distancias_desde("Centro")
    for zona, distancia in distancias.items():
        print(f"Centro → {zona}: {distancia}")
    
    # Mostrar matriz de distancias completa
    mapa.mostrar_matriz_distancias()
    
    # Probar búsqueda de zona más cercana
    print("\n ENCONTRAR ZONA MÁS CERCANA")
    zonas_disponibles = ["Noreste", "Sureste", "Suroeste"]
    zona_cercana, distancia = mapa.encontrar_zona_mas_cercana("Norte", zonas_disponibles)
    print(f"Desde 'Norte', la zona más cercana entre {zonas_disponibles}")
    print(f"es '{zona_cercana}' con distancia: {distancia}")