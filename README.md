# Sistema de Gestión de Pedidos a Domicilio

Un sistema completo desarrollado en Python que simula el funcionamiento de un servicio de pedidos a domicilio, optimizando rutas de entrega mediante algoritmos de grafos y estructuras de datos eficientes.

## Descripción General

El Sistema de Gestión de Pedidos a Domicilio desarrollado en Python es un programa trata de simular el funcionamiento completo de un servicio de pedidos a domicilio. El sistema es de capaz de gestionar clientes, restaurantes, domiciliarios y pedidos, utilizando el algoritmo de grafos dado por el profesor para optimizar las rutas de entrega y estructuras de datos eficientes para el manejo de la información. 

## Características Principales

### Gestión de Entidades

El sistema maneja cuatro tipos de entidades principales:

- **Clientes**: Registro completo con información de contacto y ubicación
- **Restaurantes**: Gestión de menús categorizados por tipo de producto
- **Domiciliarios**: Control de disponibilidad y ubicación en tiempo real
- **Pedidos**: Ciclo de vida completo desde creación hasta entrega o cancelación

### Procesos Automatizados

- Búsqueda inteligente del restaurante más cercano que tenga el producto solicitado
- Asignación automática del domiciliario disponible más próximo
- Actualización dinámica de ubicaciones después de cada entrega
- Cálculo de rutas óptimas utilizando el algoritmo de Dijkstra

### Consultas y Reportes

- Visualización de pedidos por estado (activos, entregados, cancelados)
- Historial detallado por cliente y por zona
- Consultas completas de restaurantes, domiciliarios y zonas
- Mapa interactivo de la ciudad con todas las conexiones

## Estructuras de Datos y Algoritmos

### Estructuras Implementadas

- **Grafos**: Representación del mapa de la ciudad para calcular distancias entre zonas
- **Colas (FIFO)**: Gestión ordenada de pedidos activos
- **Listas Enlazadas**: Almacenamiento eficiente de historiales de pedidos

### Algoritmos Utilizados

- **Dijkstra**: Encuentra el camino más corto entre dos zonas cualesquiera
- **Búsqueda por Prioridad**: Optimiza la asignación de recursos (restaurantes y domiciliarios)

## Requisitos

- Python 3.6 en adelante

## Instalación y Ejecución

1. Clone el repositorio:

git clone [https://github.com/juankvega/Pedidos_ED1.git]

cd sistema-pedidos-domicilio


2. Ejecute el programa principal:

python main.py



## Estructura del Proyecto

sistema-pedidos/

 main.py                  | Aplicación principal con interfaz de usuario
 
 Sistema.py               | Clase principal del sistema
 
 Mapa.py                  | Gestión del mapa y zonas
 
 Grafo.py                 | Implementación de grafos y algoritmos
 
 Modelos.py               | Clases de entidades
 
 Cola.py                  | Implementación de cola FIFO
 
 ColaConPrioridad.py      | Cola con prioridad
 
 ListaEnlazada.py         | Lista enlazada simple
 
 Nodo.py                  | Nodo genérico para estructuras

## Guía de Uso

### Datos de Prueba

El sistema incluye datos precargados para facilitar las pruebas:

**Clientes:**
- "Juan Vega" ingresar código “C001” a la hora de Crear pedido, Consultar cliente y Historial por cliente 
- “Ana Joely” ingresar código “C002” a la hora de Crear pedido, Consultar cliente y Historial por cliente 
- “Nicolas Arends” ingresar código “C003” a la hora de Crear pedido, Consultar cliente y Historial por cliente 

**Restaurantes:**
- “Restaurante La Sarten” ingresar código “R001” a la hora de Consultar Restaurante, Cargar Menu Predeterminado a Restaurante y agregar Plato a Restaurante
- “Restaurante La Sazon de Macondo” ingresar código “R002” a la hora de Consultar Restaurante, Cargar Menu Predeterminado a Restaurante y Agregar Plato a Restaurante 
- “Comidas Rapidas Punto Chevere” ingresar código “R003” a la hora de Consultar Restaurante, Cargar Menu Predeterminado a Restaurante y Agregar Plato a Restaurante 

**Domiciliarios:**
- “Javier Hernández” ingresar código “D001” a la hora de Consultar Domiciliario
- “Nairobi Diaz” ingresar código “D002” a la hora de Consultar Domiciliario 
- “Samuel Deluque” ingresar código “D003” a la hora de Consultar Domiciliario 

### Menú Disponible

El sistema ofrece 30 productos organizados en tres categorías:

**Bebidas:** 
• Pony Malta 
• Postobón Manzana 
• Pepsi 
• Coca Cola 
• Coca Cola Zero 
• Sprite 
• Agua 
• Jugo Natural 
• Limonada Natural 
• Cerveza 

**Platos:**
 • Pechuga a la Plancha 
• Pasta Carbonara 
• Pasta Boloñesa 
• Pasta Alfredo 
• Sopa de Pollo 
• Sopa de Costilla 
• Sancocho 
• Ajiaco 
• Ensalada Cesar 
• Arroz con Pollo 

**Platos Fuertes:** 
• Bandeja Paisa 
• Lechona 
• Pescado Frito 
• Mojarra Frita 
• Churrasco 
• Sobrebarriga 
• Cazuela de Mariscos • Arroz con Camarones • Lomo de Cerdo 
• Costillas BBQ

### Flujo de Uso Típico

1. **Configuración Inicial**
   - Cargar datos de prueba o crear nuevos
   - Agregar zonas al mapa de la ciudad
   - Establecer conexiones entre zonas con distancias

2. **Registro de Entidades**
   - Registrar clientes con sus zonas de ubicación
   - Dar de alta restaurantes con sus menús
   - Registrar domiciliarios disponibles

3. **Gestión de Pedidos**
   - Crear pedido para un cliente específico
   - El sistema asigna automáticamente restaurante y domiciliario
   - Procesar entrega o cancelación según corresponda

4. **Consultas**
   - Revisar estados de todos los pedidos
   - Consultar historiales por cliente o zona
   - Visualizar el mapa completo del sistema

## Arquitectura del Sistema

### Roles de las Entidades

**Cliente**
- Solicita productos específicos del menú
- Tiene una zona de ubicación fija
- Puede consultar su historial de pedidos

**Restaurante**
- Ofrece menú categorizado
- Ubicación fija en una zona específica
- Provee los productos para los pedidos

**Domiciliario**
- Transporta pedidos del restaurante al cliente
- Actualiza su ubicación después de cada entrega
- Estado de disponibilidad gestionado automáticamente

**Sistema (Coordinador)**
- Asigna recursos de forma inteligente
- Calcula rutas óptimas para cada entrega
- Gestiona estados de pedidos
- Genera reportes y estadísticas

### Flujo de Datos

1. Cliente solicita producto → Sistema busca restaurante más cercano con disponibilidad
2. Restaurante encontrado → Sistema busca domiciliario disponible más cercano
3. Domiciliario asignado → Pedido cambia a estado ASIGNADO
4. Entrega completada → Domiciliario actualiza ubicación a la del cliente
5. Pedido finalizado → Se registra en historiales correspondientes

## Decisiones Técnicas

### Arquitectura Modular

- Separación clara de responsabilidades entre clases
- Bajo acoplamiento entre componentes
- Alta cohesión en cada módulo

### Optimización

- Uso de grafos para representación eficiente del mapa
- Cola FIFO para garantizar orden de procesamiento
- Listas enlazadas para crecimiento dinámico de historiales

### Gestión de Estado

Estados definidos para cada pedido:

PENDIENTE → ASIGNADO → ENTREGADO/CANCELADO


- Transiciones controladas con validación
- Persistencia en memoria durante ejecución

## Características Destacadas

### Eficiencia en Asignaciones

- Selección automática del restaurante más cercano con el producto
- Asignación del domiciliario disponible más próximo
- Minimización de distancias totales recorridas

### Gestión Dinámica de Ubicaciones

- Actualización automática de posiciones de domiciliarios
- Consideración de nuevas ubicaciones para futuras asignaciones
- Distribución equilibrada de la carga de trabajo

### Robustez

- Validación exhaustiva de existencia de entidades
- Control de estados válidos en todo momento
- Manejo de zonas no conectadas
- Prevención de operaciones inválidas

## Escalabilidad

El sistema está diseñado pensando en el crecimiento:

- Estructuras de datos eficientes para grandes volúmenes
- Algoritmos con complejidad temporal óptima
- Arquitectura modular para agregar funcionalidades
- Separación entre lógica de negocio e interfaz

## Solución de Problemas Comunes

**Error: "Sistema object has no attribute 'Cola'"**

Solución: Verificar que el archivo  main.py  importe correctamente:

from Cola import Cola


## Equipo de Desarrollo

- **Nicolas Arends**: Entidades y modelo de datos
- **Ana Joely**: Estructuras de datos
- **Juan Vega**: Lógica de negocio
