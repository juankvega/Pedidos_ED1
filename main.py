from Sistema import Sistema
import os
import sys

def limpiar_pantalla():
    """Limpia la pantalla de la consola."""
    os.system('cls' if os.name == 'nt' else 'clear')

def pausa():
    """Pausa la ejecucion hasta que el usuario presione Enter."""
    input("\nPresione Enter para continuar...")

def mostrar_menu_principal():
    """Muestra el menu principal del sistema."""
    print("\n" + "="*70)
    print(" "*15 + "SISTEMA DE GESTION DE PEDIDOS A DOMICILIO")
    print("="*70)
    print("\nMENU PRINCIPAL\n")
    print("1.  Registrar Cliente")
    print("2.  Registrar Restaurante")
    print("3.  Registrar Domiciliario")
    print("4.  Crear Pedido (Solicitar producto)")
    print("5.  Asignar Pedido")
    print("6.  Entregar Pedido")
    print("7.  Cancelar Pedido")
    print("8.  Consultar Cliente")
    print("9.  Consultar Domiciliario")
    print("10. Consultar Restaurante")
    print("11. Ver Pedidos Activos")
    print("12. Ver Pedidos Entregados")
    print("13. Ver Pedidos Cancelados")
    print("14. Historial por Cliente")
    print("15. Historial por Zona")
    print("16. Mostrar Mapa")
    print("17. Agregar Zona al Mapa")
    print("18. Conectar Zonas")
    print("19. Cargar Menu Predeterminado a Restaurante")
    print("20. Agregar Plato a Restaurante")
    print("\n0.  Salir del Sistema")
    print("="*70)

def registrar_cliente(sistema):
    """Interfaz para registrar un cliente."""
    limpiar_pantalla()
    print("\n" + "="*70)
    print(" "*20 + "REGISTRAR CLIENTE")
    print("="*70 + "\n")
    
    codigo = input("Codigo del cliente: ")
    nombre = input("Nombre completo: ")
    zona = input("Zona de ubicacion: ")
    
    sistema.registrar_cliente(codigo, nombre, zona)
    pausa()

def registrar_restaurante(sistema):
    """Interfaz para registrar un restaurante."""
    limpiar_pantalla()
    print("\n" + "="*70)
    print(" "*20 + "REGISTRAR RESTAURANTE")
    print("="*70 + "\n")
    
    codigo = input("Codigo del restaurante: ")
    nombre = input("Nombre del restaurante: ")
    zona = input("Zona de ubicacion: ")
    
    sistema.registrar_restaurante(codigo, nombre, zona)
    pausa()

def registrar_domiciliario(sistema):
    """Interfaz para registrar un domiciliario."""
    limpiar_pantalla()
    print("\n" + "="*70)
    print(" "*20 + "REGISTRAR DOMICILIARIO")
    print("="*70 + "\n")
    
    codigo = input("Codigo del domiciliario: ")
    nombre = input("Nombre del domiciliario: ")
    zona = input("Zona de ubicacion actual: ")
    
    sistema.registrar_domiciliario(codigo, nombre, zona)
    pausa()

def crear_pedido(sistema):
    """Interfaz para crear un pedido."""
    limpiar_pantalla()
    print("\n" + "="*70)
    print(" "*20 + "CREAR PEDIDO")
    print("="*70 + "\n")
    
    codigo_cliente = input("Codigo del cliente: ")
    producto = input("Producto a solicitar: ")
    
    pedido = sistema.crear_pedido(codigo_cliente, producto)
    
    if pedido:
        print("\n¿Desea continuar con este pedido?")
        print("1. Si, asignar ahora")
        print("2. No, cancelar")
        print("3. Volver (dejar pendiente)")
        
        opcion = input("\nSeleccione una opcion: ")
        
        if opcion == "1":
            sistema.asignar_pedido(pedido)
        elif opcion == "2":
            sistema.cancelar_pedido(pedido)
    
    pausa()

def asignar_pedido_menu(sistema):
    """Interfaz para asignar un pedido pendiente."""
    limpiar_pantalla()
    print("\n" + "="*70)
    print(" "*20 + "ASIGNAR PEDIDO")
    print("="*70 + "\n")
    
    print("Esta funcion asigna automaticamente el pedido mas antiguo pendiente.")
    print("Si tiene un pedido especifico, use la opcion 'Crear Pedido'.\n")
    
    pausa()

def entregar_pedido_menu(sistema):
    """Interfaz para entregar un pedido."""
    limpiar_pantalla()
    print("\n" + "="*70)
    print(" "*20 + "ENTREGAR PEDIDO")
    print("="*70 + "\n")
    
    sistema.visualizar_pedidos_activos()
    
    if sistema.pedidos_activos.size == 0:
        pausa()
        return
    
    try:
        numero_pedido = int(input("\nNumero de pedido a entregar: "))
        
        # Buscar el pedido en la cola
        temp_cola = sistema.Cola()
        pedido_encontrado = None
        
        while sistema.pedidos_activos.size > 0:
            pedido = sistema.pedidos_activos.dequeue()
            if pedido.numero == numero_pedido:
                pedido_encontrado = pedido
            else:
                temp_cola.enqueue(pedido)
        
        # Restaurar la cola
        while temp_cola.size > 0:
            sistema.pedidos_activos.enqueue(temp_cola.dequeue())
        
        if pedido_encontrado:
            sistema.entregar_pedido(pedido_encontrado)
        else:
            print(f"\nNo se encontro el pedido #{numero_pedido}")
    
    except ValueError:
        print("\nDebe ingresar un numero valido")
    
    pausa()

def cancelar_pedido_menu(sistema):
    """Interfaz para cancelar un pedido."""
    limpiar_pantalla()
    print("\n" + "="*70)
    print(" "*20 + "CANCELAR PEDIDO")
    print("="*70 + "\n")
    
    sistema.visualizar_pedidos_activos()
    
    if sistema.pedidos_activos.size == 0:
        pausa()
        return
    
    try:
        numero_pedido = int(input("\nNumero de pedido a cancelar: "))
        
        # Buscar el pedido
        temp_cola = sistema.Cola()
        pedido_encontrado = None
        
        while sistema.pedidos_activos.size > 0:
            pedido = sistema.pedidos_activos.dequeue()
            if pedido.numero == numero_pedido:
                pedido_encontrado = pedido
            else:
                temp_cola.enqueue(pedido)
        
        # Restaurar la cola
        while temp_cola.size > 0:
            sistema.pedidos_activos.enqueue(temp_cola.dequeue())
        
        if pedido_encontrado:
            confirmar = input(f"\n¿Esta seguro de cancelar el pedido #{numero_pedido}? (s/n): ")
            if confirmar.lower() == 's':
                sistema.cancelar_pedido(pedido_encontrado)
        else:
            print(f"\nNo se encontro el pedido #{numero_pedido}")
    
    except ValueError:
        print("\nDebe ingresar un numero valido")
    
    pausa()

def consultar_cliente_menu(sistema):
    """Interfaz para consultar un cliente."""
    limpiar_pantalla()
    codigo = input("\nCodigo del cliente a consultar: ")
    sistema.consultar_cliente(codigo)
    pausa()

def consultar_domiciliario_menu(sistema):
    """Interfaz para consultar un domiciliario."""
    limpiar_pantalla()
    codigo = input("\nCodigo del domiciliario a consultar: ")
    sistema.consultar_domiciliario(codigo)
    pausa()

def consultar_restaurante_menu(sistema):
    """Interfaz para consultar un restaurante."""
    limpiar_pantalla()
    codigo = input("\nCodigo del restaurante a consultar: ")
    sistema.consultar_restaurante(codigo)
    pausa()

def historial_cliente_menu(sistema):
    """Interfaz para ver historial por cliente."""
    limpiar_pantalla()
    codigo = input("\nCodigo del cliente: ")
    sistema.historial_por_cliente(codigo)
    pausa()

def historial_zona_menu(sistema):
    """Interfaz para ver historial por zona."""
    limpiar_pantalla()
    zona = input("\nNombre de la zona: ")
    sistema.historial_por_zona(zona)
    pausa()

def agregar_zona_menu(sistema):
    """Interfaz para agregar una zona al mapa."""
    limpiar_pantalla()
    print("\n" + "="*70)
    print(" "*20 + "AGREGAR ZONA AL MAPA")
    print("="*70 + "\n")
    
    nombre_zona = input("Nombre de la zona: ")
    sistema.mapa.agregar_zona(nombre_zona)
    pausa()

def conectar_zonas_menu(sistema):
    """Interfaz para conectar dos zonas."""
    limpiar_pantalla()
    print("\n" + "="*70)
    print(" "*20 + "CONECTAR ZONAS")
    print("="*70 + "\n")
    
    zona1 = input("Zona de origen: ")
    zona2 = input("Zona de destino: ")
    try:
        distancia = float(input("Distancia entre zonas: "))
        sistema.mapa.conectar_zonas(zona1, zona2, distancia)
    except ValueError:
        print("\nLa distancia debe ser un numero valido")
    
    pausa()

def cargar_menu_predeterminado(sistema):
    """Interfaz para cargar menu predeterminado a un restaurante."""
    limpiar_pantalla()
    print("\n" + "="*70)
    print(" "*15 + "CARGAR MENU PREDETERMINADO")
    print("="*70 + "\n")
    
    codigo = input("Codigo del restaurante: ")
    
    if codigo in sistema.restaurantes:
        restaurante = sistema.restaurantes[codigo]
        restaurante.cargar_menu_predeterminado()
        print(f"\nMenu predeterminado cargado para {restaurante.nombre}")
        print("\nEl menu incluye:")
        print("  - 10 Bebidas")
        print("  - 10 Platos")
        print("  - 10 Platos Fuertes")
    else:
        print(f"\nEl restaurante con codigo {codigo} no existe")
    
    pausa()

def agregar_plato_menu(sistema):
    """Interfaz para agregar un plato a un restaurante."""
    limpiar_pantalla()
    print("\n" + "="*70)
    print(" "*20 + "AGREGAR PLATO")
    print("="*70 + "\n")
    
    codigo = input("Codigo del restaurante: ")
    
    if codigo not in sistema.restaurantes:
        print(f"\nEl restaurante con codigo {codigo} no existe")
        pausa()
        return
    
    print("\nCategorias disponibles:")
    print("1. Bebidas")
    print("2. Platos")
    print("3. Platos Fuertes")
    print("4. Otra (especificar)")
    
    opcion = input("\nSeleccione categoria: ")
    
    categorias = {
        "1": "Bebidas",
        "2": "Platos",
        "3": "Platos Fuertes"
    }
    
    if opcion in categorias:
        categoria = categorias[opcion]
    elif opcion == "4":
        categoria = input("Nombre de la categoria: ")
    else:
        print("\nOpcion invalida")
        pausa()
        return
    
    plato = input("Nombre del plato: ")
    sistema.agregar_plato_restaurante(codigo, categoria, plato)
    pausa()

def inicializar_datos_prueba(sistema):
    """Inicializa el sistema con datos de prueba."""
    print("\n Inicializando datos de prueba...")
    
    # Crear mapa
    zonas = ["Norte", "Sur", "Este", "Oeste", "Centro"]
    for zona in zonas:
        sistema.mapa.agregar_zona(zona)
    
    # Conectar zonas
    sistema.mapa.conectar_zonas("Centro", "Norte", 5)
    sistema.mapa.conectar_zonas("Centro", "Sur", 5)
    sistema.mapa.conectar_zonas("Centro", "Este", 5)
    sistema.mapa.conectar_zonas("Centro", "Oeste", 5)
    sistema.mapa.conectar_zonas("Norte", "Este", 7)
    sistema.mapa.conectar_zonas("Sur", "Oeste", 7)
    
    # Registrar clientes
    sistema.registrar_cliente("C001", "Juan Perez", "Norte")
    sistema.registrar_cliente("C002", "Maria Garcia", "Sur")
    sistema.registrar_cliente("C003", "Carlos Lopez", "Este")
    
    # Registrar restaurantes
    sistema.registrar_restaurante("R001", "Restaurante El Buen Sabor", "Centro")
    sistema.registrar_restaurante("R002", "Pizzeria Italiana", "Norte")
    sistema.registrar_restaurante("R003", "Comidas Rapidas Express", "Sur")
    
    # Cargar menús
    for codigo in sistema.restaurantes:
        sistema.restaurantes[codigo].cargar_menu_predeterminado()
    
    # Registrar domiciliarios
    sistema.registrar_domiciliario("D001", "Pedro Martinez", "Centro")
    sistema.registrar_domiciliario("D002", "Ana Rodriguez", "Norte")
    sistema.registrar_domiciliario("D003", "Luis Gomez", "Sur")
    
    print("Datos de prueba cargados exitosamente")
    pausa()

def main():
    """Función principal del programa."""
    sistema = Sistema()
    
    # Preguntar si desea cargar datos de prueba
    limpiar_pantalla()
    print("\n" + "="*70)
    print(" "*10 + "BIENVENIDO AL SISTEMA DE GESTION DE PEDIDOS")
    print("="*70 + "\n")
    
    cargar = input("¿Desea cargar datos de prueba? (s/n): ")
    if cargar.lower() == 's':
        inicializar_datos_prueba(sistema)
    
    while True:
        limpiar_pantalla()
        mostrar_menu_principal()
        
        opcion = input("\nSeleccione una opcion: ")
        
        if opcion == "1":
            registrar_cliente(sistema)
        elif opcion == "2":
            registrar_restaurante(sistema)
        elif opcion == "3":
            registrar_domiciliario(sistema)
        elif opcion == "4":
            crear_pedido(sistema)
        elif opcion == "5":
            asignar_pedido_menu(sistema)
        elif opcion == "6":
            entregar_pedido_menu(sistema)
        elif opcion == "7":
            cancelar_pedido_menu(sistema)
        elif opcion == "8":
            consultar_cliente_menu(sistema)
        elif opcion == "9":
            consultar_domiciliario_menu(sistema)
        elif opcion == "10":
            consultar_restaurante_menu(sistema)
        elif opcion == "11":
            limpiar_pantalla()
            sistema.visualizar_pedidos_activos()
            pausa()
        elif opcion == "12":
            limpiar_pantalla()
            sistema.visualizar_pedidos_entregados()
            pausa()
        elif opcion == "13":
            limpiar_pantalla()
            sistema.visualizar_pedidos_cancelados()
            pausa()
        elif opcion == "14":
            historial_cliente_menu(sistema)
        elif opcion == "15":
            historial_zona_menu(sistema)
        elif opcion == "16":
            limpiar_pantalla()
            sistema.mapa.mostrar_mapa()
            pausa()
        elif opcion == "17":
            agregar_zona_menu(sistema)
        elif opcion == "18":
            conectar_zonas_menu(sistema)
        elif opcion == "19":
            cargar_menu_predeterminado(sistema)
        elif opcion == "20":
            agregar_plato_menu(sistema)
        elif opcion == "0":
            limpiar_pantalla()
            print("\n" + "="*70)
            print(" "*15 + "GRACIAS POR USAR EL SISTEMA.")
            print("="*70 + "\n")
            sys.exit(0)
        else:
            print("\nOpcion invalida. Intente de nuevo.")
            pausa()

if __name__ == "__main__":
    main()