from datetime import datetime
from ListaEnlazada import ListaEnlazada
from enum import Enum

class EstadoPedido(Enum):
    """Estados posibles de un pedido."""
    PENDIENTE = "PENDIENTE"
    ASIGNADO = "ASIGNADO"
    ENTREGADO = "ENTREGADO"
    CANCELADO = "CANCELADO"


class Cliente:
    """Representa un cliente del sistema."""
    def __init__(self, codigo, nombre_completo, pedido_solicitado, zona_ubicacion):
        self.codigo = codigo
        self.nombre_completo = nombre_completo
        self.pedido_solicitado = pedido_solicitado
        self.zona_ubicacion = zona_ubicacion


class Restaurante:
    """Representa un restaurante en el sistema."""
    def __init__(self, codigo, nombre, zona_ubicacion):
        self.codigo = codigo
        self.nombre = nombre
        self.zona_ubicacion = zona_ubicacion
        self.menu = ListaEnlazada()  # Lista simple para los nombres de platos

    def agregar_plato_menu(self, plato):
        """Agrega un plato al menú del restaurante."""
        self.menu.agregar(plato)
    
    def tiene_plato(self, plato):
        """Verifica si el restaurante tiene un plato específico en su menú."""
        for i in range(self.menu.get_tamano()):
            if self.menu.obtener(i) == plato:
                return True
        return False


class Domiciliario:
    """Representa un domiciliario del sistema."""
    def __init__(self, codigo, nombre, ubicacion_actual):
        self.codigo = codigo
        self.nombre = nombre
        self.ubicacion_actual = ubicacion_actual
        self.disponible = True


class Pedido:
    """Representa un pedido en el sistema."""
    def __init__(self, cliente):
        self.cliente = cliente
        self.estado = EstadoPedido.PENDIENTE
        self.fecha_hora = datetime.now()
        self.restaurante = None
        self.domiciliario = None