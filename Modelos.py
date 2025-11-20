from datetime import datetime
from enum import Enum

class EstadoPedido(Enum):
    """Estados posibles de un pedido."""
    PENDIENTE = "PENDIENTE"      # Recien creado
    ASIGNADO = "ASIGNADO"        # Restaurante y domiciliario asignados
    ENTREGADO = "ENTREGADO"      # Ya entregado al cliente
    CANCELADO = "CANCELADO"      # Cancelado por el cliente


class Cliente:
    """Representa un cliente del sistema."""
    def __init__(self, codigo, nombre_completo, pedido_solicitado, zona_ubicacion):
        self.codigo = codigo
        self.nombre_completo = nombre_completo
        self.pedido_solicitado = pedido_solicitado
        self.zona_ubicacion = zona_ubicacion
        self.pedidos_realizados = 0  # Contador de pedidos


class CategoriaMenu:
    """Representa una categoria del menu con sus platos."""
    def __init__(self, nombre):
        self.nombre = nombre
        self.platos = []  # Lista de platos en esta categoría
    
    def agregar_plato(self, plato):
        """Agrega un plato a esta categoria."""
        if plato not in self.platos:
            self.platos.append(plato)
    
    def tiene_plato(self, plato):
        """Verifica si la categoria tiene un plato especifico."""
        return plato in self.platos


class Restaurante:
    """Representa un restaurante en el sistema."""
    def __init__(self, codigo, nombre, zona_ubicacion):
        self.codigo = codigo
        self.nombre = nombre
        self.zona_ubicacion = zona_ubicacion
        self.menu = {}  # {categoria: CategoriaMenu}
        self._inicializar_categorias()
    
    def _inicializar_categorias(self):
        """Inicializa las categorias del menu."""
        self.menu["Bebidas"] = CategoriaMenu("Bebidas")
        self.menu["Platos"] = CategoriaMenu("Platos")
        self.menu["Platos Fuertes"] = CategoriaMenu("Platos Fuertes")
    
    def agregar_plato_menu(self, categoria, plato):
        """Agrega un plato al menu en una categoria especifica."""
        if categoria not in self.menu:
            self.menu[categoria] = CategoriaMenu(categoria)
        
        self.menu[categoria].agregar_plato(plato)
    
    def tiene_plato(self, plato):
        """Verifica si el restaurante tiene un plato especifico en cualquier categoria."""
        for categoria in self.menu.values():
            if categoria.tiene_plato(plato):
                return True
        return False
    
    def mostrar_menu(self):
        """Muestra el menu completo del restaurante organizado por categorias."""
        if not self.menu:
            print(" El menu esta vacio")
            return
        
        for nombre_categoria, categoria in self.menu.items():
            if categoria.platos:
                print(f"\n  {nombre_categoria}:")
                for i, plato in enumerate(categoria.platos, 1):
                    print(f"    {i}. {plato}")
    
    def cargar_menu_predeterminado(self):
        """Carga un menu predeterminado con platos tipicos."""
        # Bebidas
        bebidas = [
            "Pony Malta",
            "Postobon Manzana",
            "Coca Cola",
            "Coca Cola Zero",
            "Sprite",
            "Agua",
            "Jugo Natural",
            "Limonada Natural",
            "Cerveza"
        ]
        
        for bebida in bebidas:
            self.agregar_plato_menu("Bebidas", bebida)
        
        # Platos
        platos = [
            "Pechuga a la Plancha",
            "Pasta Carbonara",
            "Pasta Boloñesa",
            "Pasta Alfredo",
            "Sopa de Pollo",
            "Sopa de Costilla",
            "Sancocho",
            "Ajiaco",
            "Ensalada Cesar",
            "Arroz con Pollo"
        ]
        
        for plato in platos:
            self.agregar_plato_menu("Platos", plato)
        
        # Platos Fuertes
        platos_fuertes = [
            "Bandeja Paisa",
            "Lechona",
            "Pescado Frito",
            "Mojarra Frita",
            "Churrasco",
            "Cazuela de Mariscos",
            "Arroz con Camarones",
            "Lomo de Cerdo",
            "Costillas BBQ"
        ]
        
        for plato_fuerte in platos_fuertes:
            self.agregar_plato_menu("Platos Fuertes", plato_fuerte)


class Domiciliario:
    """Representa un domiciliario del sistema."""
    def __init__(self, codigo, nombre, ubicacion_actual):
        self.codigo = codigo
        self.nombre = nombre
        self.ubicacion_actual = ubicacion_actual
        self.disponible = True
        self.pedidos_entregados = 0  # Contador de entregas


class Pedido:
    """Representa un pedido en el sistema."""
    def __init__(self, cliente):
        self.numero = 0  # Se asignará por el sistema
        self.cliente = cliente
        self.estado = EstadoPedido.PENDIENTE
        self.fecha_hora = datetime.now()
        self.fecha_hora_entrega = None
        self.fecha_hora_cancelacion = None
        self.restaurante = None
        self.domiciliario = None