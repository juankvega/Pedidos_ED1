from Mapa import Mapa
from Modelos import Cliente, Restaurante, Domiciliario, Pedido, EstadoPedido
from ListaEnlazada import ListaEnlazada
from Cola import Cola
from datetime import datetime

class Sistema:
    """Sistema principal de gestión de pedidos a domicilio."""
    
    def __init__(self):
        self.mapa = Mapa()
        self.clientes = {}  # {codigo: Cliente}
        self.restaurantes = {}  # {codigo: Restaurante}
        self.domiciliarios = {}  # {codigo: Domiciliario}
        self.pedidos_activos = Cola()
        self.pedidos_entregados = ListaEnlazada()
        self.pedidos_cancelados = ListaEnlazada()
        self.historial_pedidos = {}  # {codigo_cliente: [pedidos]}
        self.contador_pedidos = 0
    
    # REGISTRO DE ENTIDADES
    
    def registrar_cliente(self, codigo, nombre_completo, zona_ubicacion):
        """Registra un nuevo cliente en el sistema."""
        if codigo in self.clientes:
            print(f"El cliente con código {codigo} ya existe")
            return False
        
        if zona_ubicacion not in self.mapa.zonas:
            print(f"La zona '{zona_ubicacion}' no existe en el mapa")
            return False
        
        cliente = Cliente(codigo, nombre_completo, None, zona_ubicacion)
        cliente.pedidos_realizados = 0  # Contador de pedidos
        self.clientes[codigo] = cliente
        self.historial_pedidos[codigo] = []
        print(f"Cliente '{nombre_completo}' registrado exitosamente")
        return True
    
    def registrar_restaurante(self, codigo, nombre, zona_ubicacion):
        """Registra un nuevo restaurante en el sistema."""
        if codigo in self.restaurantes:
            print(f"El restaurante con código {codigo} ya existe")
            return False
        
        if zona_ubicacion not in self.mapa.zonas:
            print(f"La zona '{zona_ubicacion}' no existe en el mapa")
            return False
        
        restaurante = Restaurante(codigo, nombre, zona_ubicacion)
        self.restaurantes[codigo] = restaurante
        
        # Agregar restaurante a la zona
        zona = self.mapa.obtener_zona(zona_ubicacion)
        if zona:
            zona.agregar_restaurante(restaurante)
        
        print(f"Restaurante '{nombre}' registrado en zona '{zona_ubicacion}'")
        return True
    
    def registrar_domiciliario(self, codigo, nombre, ubicacion_actual):
        """Registra un nuevo domiciliario en el sistema."""
        if codigo in self.domiciliarios:
            print(f"El domiciliario con codigo {codigo} ya existe")
            return False
        
        if ubicacion_actual not in self.mapa.zonas:
            print(f"La zona '{ubicacion_actual}' no existe en el mapa")
            return False
        
        domiciliario = Domiciliario(codigo, nombre, ubicacion_actual)
        domiciliario.pedidos_entregados = 0  # Contador de entregas
        self.domiciliarios[codigo] = domiciliario
        
        # Agregar domiciliario a la zona
        zona = self.mapa.obtener_zona(ubicacion_actual)
        if zona:
            zona.agregar_domiciliario(domiciliario)
        
        print(f"Domiciliario '{nombre}' registrado en zona '{ubicacion_actual}'")
        return True
    
    # GESTION DE MENUS
    
    def agregar_plato_restaurante(self, codigo_restaurante, categoria, plato):
        """Agrega un plato al menu de un restaurante en una categoria especifica."""
        if codigo_restaurante not in self.restaurantes:
            print(f"El restaurante con codigo {codigo_restaurante} no existe")
            return False
        
        restaurante = self.restaurantes[codigo_restaurante]
        restaurante.agregar_plato_menu(categoria, plato)
        print(f"Plato '{plato}' agregado a categoria '{categoria}' en {restaurante.nombre}")
        return True
    
    # BUSQUEDA Y ASIGNACIÓN 
    
    def buscar_restaurante_con_producto(self, producto, zona_cliente):
        """
        Busca el restaurante mas cercano que tenga el producto solicitado.
        Usa el algoritmo de Dijkstra para encontrar distancias.
        """
        # Obtener distancias desde la zona del cliente
        distancias = self.mapa.calcular_distancias_desde(zona_cliente)
        
        if distancias is None:
            return None, float('inf')
        
        restaurante_mas_cercano = None
        distancia_minima = float('inf')
        
        # Buscar en todos los restaurantes
        for restaurante in self.restaurantes.values():
            if restaurante.tiene_plato(producto):
                zona_restaurante = restaurante.zona_ubicacion
                
                if zona_restaurante in distancias:
                    distancia = distancias[zona_restaurante]
                    
                    if distancia < distancia_minima:
                        distancia_minima = distancia
                        restaurante_mas_cercano = restaurante
        
        return restaurante_mas_cercano, distancia_minima
    
    def buscar_domiciliario_disponible(self, zona_restaurante):
        """
        Busca el domiciliario disponible mas cercano al restaurante.
        """
        # Obtener distancias desde la zona del restaurante
        distancias = self.mapa.calcular_distancias_desde(zona_restaurante)
        
        if distancias is None:
            return None, float('inf')
        
        domiciliario_mas_cercano = None
        distancia_minima = float('inf')
        
        # Buscar domiciliarios disponibles
        for domiciliario in self.domiciliarios.values():
            if domiciliario.disponible:
                zona_domiciliario = domiciliario.ubicacion_actual
                
                if zona_domiciliario in distancias:
                    distancia = distancias[zona_domiciliario]
                    
                    if distancia < distancia_minima:
                        distancia_minima = distancia
                        domiciliario_mas_cercano = domiciliario
        
        return domiciliario_mas_cercano, distancia_minima
    
    # GESTIÓN DE PEDIDOS 
    
    def crear_pedido(self, codigo_cliente, producto):
        """
        Crea un nuevo pedido para un cliente.
        ETAPA 1: Pedido recien creado (PENDIENTE)
        """
        if codigo_cliente not in self.clientes:
            print(f"El cliente con codigo {codigo_cliente} no existe")
            return None
        
        cliente = self.clientes[codigo_cliente]
        cliente.pedido_solicitado = producto
        
        # Crear el pedido
        pedido = Pedido(cliente)
        self.contador_pedidos += 1
        pedido.numero = self.contador_pedidos
        
        print(f"\n{'='*60}")
        print(f"  PEDIDO #{pedido.numero} CREADO")
        print(f"{'='*60}")
        print(f"Cliente: {cliente.nombre_completo}")
        print(f"Producto solicitado: {producto}")
        print(f"Zona del cliente: {cliente.zona_ubicacion}")
        print(f"Estado: {pedido.estado.value}")
        print(f"{'='*60}\n")
        
        return pedido
    
    def asignar_pedido(self, pedido):
        """
        Asigna restaurante y domiciliario al pedido.
        ETAPA 2: Pedido asignado (ASIGNADO)
        """
        if pedido.estado != EstadoPedido.PENDIENTE:
            print(f"El pedido ya no esta pendiente")
            return False
        
        cliente = pedido.cliente
        producto = cliente.pedido_solicitado
        
        print(f"\n Buscando restaurante con '{producto}'...")
        restaurante, dist_rest = self.buscar_restaurante_con_producto(
            producto, cliente.zona_ubicacion
        )
        
        if restaurante is None:
            print(f"No se encontro ningun restaurante con '{producto}'")
            return False
        
        print(f"Restaurante encontrado: {restaurante.nombre} (distancia: {dist_rest})")
        
        print(f"\n Buscando domiciliario disponible...")
        domiciliario, dist_dom = self.buscar_domiciliario_disponible(
            restaurante.zona_ubicacion
        )
        
        if domiciliario is None:
            print(f"No hay domiciliarios disponibles")
            return False
        
        print(f"Domiciliario encontrado: {domiciliario.nombre} (distancia: {dist_dom})")
        
        # Asignar al pedido
        pedido.restaurante = restaurante
        pedido.domiciliario = domiciliario
        pedido.estado = EstadoPedido.ASIGNADO
        domiciliario.disponible = False
        
        # Agregar a pedidos activos
        self.pedidos_activos.enqueue(pedido)
        
        print(f"\n{'='*60}")
        print(f"  PEDIDO #{pedido.numero} ASIGNADO")
        print(f"{'='*60}")
        print(f"Restaurante: {restaurante.nombre} (Zona: {restaurante.zona_ubicacion})")
        print(f"Domiciliario: {domiciliario.nombre} (Zona: {domiciliario.ubicacion_actual})")
        print(f"Estado: {pedido.estado.value}")
        print(f"{'='*60}\n")
        
        return True
    
    def entregar_pedido(self, pedido):
        """
        Marca el pedido como entregado.
        ETAPA 3: Pedido entregado (ENTREGADO)
        El domiciliario actualiza su ubicacion a la zona del cliente.
        """
        if pedido.estado != EstadoPedido.ASIGNADO:
            print(f"El pedido no esta en estado ASIGNADO")
            return False
        
        # Actualizar estado
        pedido.estado = EstadoPedido.ENTREGADO
        pedido.fecha_hora_entrega = datetime.now()
        
        # Actualizar ubicación del domiciliario a la zona del cliente
        zona_anterior = pedido.domiciliario.ubicacion_actual
        zona_nueva = pedido.cliente.zona_ubicacion
        
        # Remover de zona anterior
        zona_obj_anterior = self.mapa.obtener_zona(zona_anterior)
        if zona_obj_anterior:
            zona_obj_anterior.remover_domiciliario(pedido.domiciliario)
        
        # Actualizar ubicación
        pedido.domiciliario.ubicacion_actual = zona_nueva
        pedido.domiciliario.disponible = True
        pedido.domiciliario.pedidos_entregados += 1
        
        # Agregar a nueva zona
        zona_obj_nueva = self.mapa.obtener_zona(zona_nueva)
        if zona_obj_nueva:
            zona_obj_nueva.agregar_domiciliario(pedido.domiciliario)
        
        # Actualizar contador del cliente
        pedido.cliente.pedidos_realizados += 1
        
        # Mover a historial
        self.pedidos_entregados.agregar(pedido)
        self.historial_pedidos[pedido.cliente.codigo].append(pedido)
        
        print(f"\n{'='*60}")
        print(f"  PEDIDO #{pedido.numero} ENTREGADO")
        print(f"{'='*60}")
        print(f"Cliente: {pedido.cliente.nombre_completo}")
        print(f"Producto: {pedido.cliente.pedido_solicitado}")
        print(f"Domiciliario: {pedido.domiciliario.nombre}")
        print(f"Ubicacion actualizada: {zona_anterior} → {zona_nueva}")
        print(f"Estado: {pedido.estado.value}")
        print(f"{'='*60}\n")
        
        return True
    
    def cancelar_pedido(self, pedido):
        """
        Cancela un pedido en cualquier momento antes de la entrega.
        Solo se pueden cancelar pedidos PENDIENTE o ASIGNADO.
        """
        if pedido.estado == EstadoPedido.ENTREGADO:
            print(f"No se puede cancelar un pedido ya entregado")
            return False
        
        if pedido.estado == EstadoPedido.CANCELADO:
            print(f"El pedido ya esta cancelado")
            return False
        
        # Liberar domiciliario si estaba asignado
        if pedido.domiciliario:
            pedido.domiciliario.disponible = True
        
        pedido.estado = EstadoPedido.CANCELADO
        pedido.fecha_hora_cancelacion = datetime.now()
        
        # Mover a cancelados
        self.pedidos_cancelados.agregar(pedido)
        self.historial_pedidos[pedido.cliente.codigo].append(pedido)
        
        print(f"\n{'='*60}")
        print(f"  PEDIDO #{pedido.numero} CANCELADO")
        print(f"{'='*60}")
        print(f"Cliente: {pedido.cliente.nombre_completo}")
        print(f"Producto: {pedido.cliente.pedido_solicitado}")
        print(f"Estado: {pedido.estado.value}")
        print(f"{'='*60}\n")
        
        return True
    
    # CONSULTAS
    
    def consultar_cliente(self, codigo_cliente):
        """Muestra informacion completa del cliente."""
        if codigo_cliente not in self.clientes:
            print(f"El cliente con codigo {codigo_cliente} no existe")
            return
        
        cliente = self.clientes[codigo_cliente]
        
        print(f"\n{'='*60}")
        print(f"  INFORMACION DEL CLIENTE")
        print(f"{'='*60}")
        print(f"Codigo: {cliente.codigo}")
        print(f"Nombre: {cliente.nombre_completo}")
        print(f"Zona: {cliente.zona_ubicacion}")
        print(f"Pedidos realizados: {cliente.pedidos_realizados}")
        print(f"Pedido actual solicitado: {cliente.pedido_solicitado or 'Ninguno'}")
        
        # Mostrar historial
        historial = self.historial_pedidos.get(codigo_cliente, [])
        if historial:
            print(f"\nHistorial de pedidos ({len(historial)}):")
            for i, p in enumerate(historial, 1):
                print(f"  {i}. Pedido #{p.numero} - {p.estado.value} - {p.cliente.pedido_solicitado}")
        
        print(f"{'='*60}\n")
    
    def consultar_domiciliario(self, codigo_domiciliario):
        """Muestra informacion completa del domiciliario."""
        if codigo_domiciliario not in self.domiciliarios:
            print(f"El domiciliario con codigo {codigo_domiciliario} no existe")
            return
        
        domiciliario = self.domiciliarios[codigo_domiciliario]
        
        print(f"\n{'='*60}")
        print(f"  INFORMACION DEL DOMICILIARIO")
        print(f"{'='*60}")
        print(f"Codigo: {domiciliario.codigo}")
        print(f"Nombre: {domiciliario.nombre}")
        print(f"Ubicacion actual: {domiciliario.ubicacion_actual}")
        print(f"Disponible: {'Si' if domiciliario.disponible else 'No'}")
        print(f"Pedidos entregados: {domiciliario.pedidos_entregados}")
        print(f"{'='*60}\n")
    
    def consultar_restaurante(self, codigo_restaurante):
        """Muestra informacion completa del restaurante."""
        if codigo_restaurante not in self.restaurantes:
            print(f"El restaurante con codigo {codigo_restaurante} no existe")
            return
        
        restaurante = self.restaurantes[codigo_restaurante]
        
        print(f"\n{'='*60}")
        print(f"  INFORMACION DEL RESTAURANTE")
        print(f"{'='*60}")
        print(f"Codigo: {restaurante.codigo}")
        print(f"Nombre: {restaurante.nombre}")
        print(f"Zona: {restaurante.zona_ubicacion}")
        print(f"\nMenu disponible:")
        restaurante.mostrar_menu()
        print(f"{'='*60}\n")
    
    def visualizar_pedidos_activos(self):
        """Muestra todos los pedidos activos (asignados)."""
        print(f"\n{'='*60}")
        print(f"  PEDIDOS ACTIVOS")
        print(f"{'='*60}")
        
        if self.pedidos_activos.size == 0:
            print("No hay pedidos activos")
        else:
            temp_cola = Cola()
            contador = 1
            
            while self.pedidos_activos.size > 0:
                pedido = self.pedidos_activos.dequeue()
                print(f"\n{contador}. Pedido #{pedido.numero}")
                print(f"   Cliente: {pedido.cliente.nombre_completo}")
                print(f"   Producto: {pedido.cliente.pedido_solicitado}")
                print(f"   Restaurante: {pedido.restaurante.nombre}")
                print(f"   Domiciliario: {pedido.domiciliario.nombre}")
                print(f"   Estado: {pedido.estado.value}")
                temp_cola.enqueue(pedido)
                contador += 1
            
            # Restaurar cola
            while temp_cola.size > 0:
                self.pedidos_activos.enqueue(temp_cola.dequeue())
        
        print(f"{'='*60}\n")
    
    def visualizar_pedidos_entregados(self):
        """Muestra todos los pedidos entregados."""
        print(f"\n{'='*60}")
        print(f"  PEDIDOS ENTREGADOS")
        print(f"{'='*60}")
        
        if self.pedidos_entregados.obtener_tamano() == 0:
            print("No hay pedidos entregados")
        else:
            for i in range(self.pedidos_entregados.obtener_tamano()):
                pedido = self.pedidos_entregados.obtener(i)
                print(f"\n{i+1}. Pedido #{pedido.numero}")
                print(f"   Cliente: {pedido.cliente.nombre_completo}")
                print(f"   Producto: {pedido.cliente.pedido_solicitado}")
                print(f"   Estado: {pedido.estado.value}")
        
        print(f"{'='*60}\n")
    
    def visualizar_pedidos_cancelados(self):
        """Muestra todos los pedidos cancelados."""
        print(f"\n{'='*60}")
        print(f"  PEDIDOS CANCELADOS")
        print(f"{'='*60}")
        
        if self.pedidos_cancelados.obtener_tamano() == 0:
            print("No hay pedidos cancelados")
        else:
            for i in range(self.pedidos_cancelados.obtener_tamano()):
                pedido = self.pedidos_cancelados.obtener(i)
                print(f"\n{i+1}. Pedido #{pedido.numero}")
                print(f"   Cliente: {pedido.cliente.nombre_completo}")
                print(f"   Producto: {pedido.cliente.pedido_solicitado}")
                print(f"   Estado: {pedido.estado.value}")
        
        print(f"{'='*60}\n")
    
    def historial_por_cliente(self, codigo_cliente):
        """Muestra el historial de pedidos de un cliente especifico."""
        if codigo_cliente not in self.clientes:
            print(f"El cliente con codigo {codigo_cliente} no existe")
            return
        
        cliente = self.clientes[codigo_cliente]
        historial = self.historial_pedidos.get(codigo_cliente, [])
        
        print(f"\n{'='*60}")
        print(f"  HISTORIAL DE {cliente.nombre_completo}")
        print(f"{'='*60}")
        
        if not historial:
            print("No hay pedidos en el historial")
        else:
            for i, pedido in enumerate(historial, 1):
                print(f"\n{i}. Pedido #{pedido.numero}")
                print(f"   Producto: {pedido.cliente.pedido_solicitado}")
                print(f"   Estado: {pedido.estado.value}")
                print(f"   Fecha: {pedido.fecha_hora.strftime('%Y-%m-%d %H:%M:%S')}")
        
        print(f"{'='*60}\n")
    
    def historial_por_zona(self, zona):
        """Muestra el historial de pedidos de una zona especifica."""
        if zona not in self.mapa.zonas:
            print(f"La zona '{zona}' no existe")
            return
        
        print(f"\n{'='*60}")
        print(f"  HISTORIAL DE PEDIDOS - ZONA: {zona}")
        print(f"{'='*60}")
        
        pedidos_zona = []
        
        # Buscar en historial de todos los clientes
        for cliente in self.clientes.values():
            if cliente.zona_ubicacion == zona:
                pedidos_zona.extend(self.historial_pedidos.get(cliente.codigo, []))
        
        if not pedidos_zona:
            print("No hay pedidos en esta zona")
        else:
            for i, pedido in enumerate(pedidos_zona, 1):
                print(f"\n{i}. Pedido #{pedido.numero}")
                print(f"   Cliente: {pedido.cliente.nombre_completo}")
                print(f"   Producto: {pedido.cliente.pedido_solicitado}")
                print(f"   Estado: {pedido.estado.value}")
        
        print(f"{'='*60}\n")