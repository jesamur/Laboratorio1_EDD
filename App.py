products_file = 'products.csv'
providers_file = 'providers.csv'
sales_file = 'sales.csv'
purchases_file = 'purchases.csv'
indexproduct = 'index_producto.csv'
indexprovedor = 'index_provedor.csv'
indexventas = 'index_ventas.csv'
indexcompras = 'index_compras.csv'


products_data = [
    {"id": "1", "nombre": "Camiseta", "categoria": "Ropa casual", "precio": "45000", "stock": "50", "descripcion": "algodón 100%", "proveedor": "ModaColombia"},
    {"id": "2", "nombre": "Jean", "categoria": "Vestidos", "precio": "120000", "stock": "30", "descripcion": "azul oscuro ", "proveedor": "Textiles Andinos"},
    {"id": "3", "nombre": "Vestido", "categoria": "Vestidos", "precio": "89900", "stock": "25", "descripcion": "Verano", "proveedor": "Diseños Caribe"},
    {"id": "4", "nombre": "Chaqueta", "categoria": "Abrigos", "precio": "150000", "stock": "15", "descripcion": "Clásica" , "proveedor": "ModaColombia"}
]

providers_data = [
    {"id": "1", "nombre": "ModaColombia", "contacto": " 3105551111", "direccion": "Carrera 15 #88-90"},
    {"id": "2", "nombre": "Textiles Andinos", "contacto": "3208882222", "direccion": "Calle 45 #12-30"},
    {"id": "3", "nombre": "Diseños Caribe", "contacto": "3152223333", "direccion": "Av. 80 #50-25"}
]

sales_data = [
    {"id": "1", "id_producto": "1", "id_cliente": "6", "fecha_venta": "15/05/2023", "cantidad": "3"},
    {"id": "2", "id_producto": "2", "id_cliente": "4", "fecha_venta": "16/05/2023", "cantidad": "1"},
    {"id": "3", "id_producto": "3", "id_cliente": "6", "fecha_venta": "17/05/2023", "cantidad": "2"},
    {"id": "4", "id_producto": "4", "id_cliente": "5", "fecha_venta": "18/05/2023", "cantidad": "1"}
]

purchases_data = [
    {"id": "1", "id_producto": "1", "id_proveedor": "1", "fecha_compra": "05/05/2025", "cantidad": "100"},
    {"id": "2", "id_producto": "2", "id_proveedor": "2", "fecha_compra": "06/05/2025", "cantidad": "50"},
    {"id": "3", "id_producto": "3", "id_proveedor": "3", "fecha_compra": "07/05/2025", "cantidad": "40"},
    {"id": "4", "id_producto": "4", "id_proveedor": "1", "fecha_compra": "08/05/2025", "cantidad": "30"}
]

class Archivo:
    def __init__(self, file_name):
        self.file_name = file_name
    
    def abrir_archivo(self, headers):
        with open(self.file_name, 'w') as file:
            file.write(','.join(headers) + '\n')
    
    def escribir_archivo(self, data):
        with open(self.file_name, 'a') as file:
            file.write(','.join(str(item) for item in data) + '\n')
    
    def leer_archivo(self):
        with open(self.file_name, 'r') as file:
            for row in file:
                print(row.strip())
    
    def contar_lineas(self):
        contador = 0
        with open(self.file_name, 'r') as file:
            linea = file.readline()
            while linea: 
                contador += 1
                linea = file.readline()  
        return contador
    
class Indice:
    def __init__(self, file_name):
        self.file_name = file_name
    
    def crear_indice(self, data_file, key_index=0):
        with open(data_file, 'r') as file:
            lines = file.readlines()

        with open(self.file_name, 'w') as file:
            for i in range(1, len(lines)):  
                key = lines[i].split(',')[key_index]  
                file.write(key + ',' + str(i) + '\n') 
    
    def cargar_indice(self):
        index = {}
        with open(self.file_name, 'r') as file:
            for row in file:
                key, value = row.strip().split(',')
                if key not in index:
                    index[key] = []
                index[key].append(value)
        return index
    
    def buscar_por_id(self, id):
        with open(self.file_name, 'r') as file:
            lines = file.readlines()
            for line in lines:
                parte = line.strip().split(',')
                if str(id) == parte[0]:  
                    return True  
        return False

class Producto:
    def __init__(self, archivo, indice):
        self.archivo = archivo
        self.indice = indice
    
    def registrar_producto(self):
        print("\n┌─────────────────────────────────────┐")
        print("│      REGISTRO DE NUEVO PRODUCTO     │")
        print("└─────────────────────────────────────┘")
        id_producto = str(self.archivo.contar_lineas())
        nombre = validar_input('| Nombre del producto: ')
        categoria = validar_input('| Categoría: ')
        precio = validar_input('| Precio: ')
        stock = validar_input('| Stock disponible: ')
        descripcion = validar_input('| Descripción: ')
        proveedor = validar_input('| Proveedor: ')
        self.archivo.escribir_archivo([id_producto, nombre, categoria, precio, stock, descripcion, proveedor])

        self.indice.crear_indice(self.archivo.file_name)
        print("\n┌─────────────────────────────────────┐")
        print("│  Producto agregado con éxito      │")
        print("└─────────────────────────────────────┘")

    
    def construir_indice_proveedores(self):
        
        indice_proveedores = {}

        with open(self.archivo.file_name, 'r') as archivo:
            for linea in archivo:
                partes = linea.strip().split(',')
                if len(partes) > 6:
                    proveedor = partes[6].strip().lower() 
                    if proveedor not in indice_proveedores:
                        indice_proveedores[proveedor] = []  
                    indice_proveedores[proveedor].append(linea.strip())  

        return indice_proveedores  
    
    def buscar_por_nombre(self, nombre):
        productos_encontrados = []
        with open(self.archivo.file_name, 'r') as archivo: 
            for linea in archivo:
                partes = linea.strip().split(',')
                if len(partes) > 1 and partes[1].lower() == nombre.lower(): 
                    productos_encontrados.append(linea.strip())

        if productos_encontrados:
            print("\n| Productos encontrados:")
            for producto in productos_encontrados:
                print(producto)
        else:
            print("\n╔════════════════════════════╗")
            print("║ Producto no encontrado      ║")
            print("╚════════════════════════════╝")

        return productos_encontrados

    
    def buscar_por_categoria(self, categoria):
        productos_encontrados = []
        with open(self.archivo.file_name, 'r') as archivo:  
            for linea in archivo:
                partes = linea.strip().split(',')
                if len(partes) > 2 and partes[2].lower() == categoria.lower(): 
                    productos_encontrados.append(linea.strip())

        if productos_encontrados:
            print("\n| Productos encontrados en la categoría '{}':".format(categoria))
            for producto in productos_encontrados:
                print(producto)
        else:
            print("\n╔════════════════════════════╗")
            print("║ Categoría no encontrada    ║")
            print("╚════════════════════════════╝")

        return productos_encontrados

    def buscar_por_proveedor(self, proveedor):
    
        proveedor = proveedor.strip().lower()
        indice_proveedores = self.construir_indice_proveedores() 

        if proveedor in indice_proveedores:
            print("\n| Productos encontrados del proveedor '{}':".format(proveedor))
            for producto in indice_proveedores[proveedor]:
                print(producto)
            return indice_proveedores[proveedor]
        else:
            print("\n╔════════════════════════════╗")
            print("║ Proveedor no encontrado    ║")
            print("╚════════════════════════════╝")
            return []
    
    
    def eliminar_por_nombre(self, nombre):
        print(f"Archivo actual: {self.archivo.file_name}")
        nombre = nombre.strip().lower()  
        eliminado = False
        nuevas_lineas = []

        
        with open(self.archivo.file_name, 'r', newline='') as file:
            lineas = file.readlines()

        if not lineas:
            print("\n El archivo está vacío.")
            return

        encabezado = lineas[0]  
        nuevas_lineas.append(encabezado)  

    
        for linea in lineas[1:]:  
            datos = linea.strip().split(',')
            if datos[1].strip().lower() != nombre:
                nuevas_lineas.append(linea)  
            else:
                eliminado = True

        
        if eliminado:
            with open(self.archivo.file_name, 'w', newline='') as file:
                file.writelines(nuevas_lineas)  

            self.indice.crear_indice(self.archivo.file_name)  

            print("\n┌───────────────────────────────┐")
            print("│    Producto eliminado con éxito  │")
            print("└───────────────────────────────┘")
        else:
            print("\n╔════════════════════════════╗")
            print("║      Producto no encontrado   ║")
            print("╚════════════════════════════╝")

def validar_input(mensaje):
    while True:
        dato = input(mensaje).strip()
        if dato:
            return dato
        print("Este campo no puede estar vacío. Intente nuevamente.")

def validar_fecha(mensaje, tipo):
    while True:
        try:
            dato = int(validar_input(mensaje))
            if tipo == 1 and 1 <= dato <= 31:  
                return dato
            elif tipo == 2 and 1 <= dato <= 12:  
                return dato
            elif tipo == 3 and dato >= 2025: 
                return dato
            else:
                print("Ingrese un valor válido.")
        except ValueError:
            print("Debe ingresar un número válido.")

def validar_producto(mensaje, indice_productos):
    while True:
        id_producto = validar_input(mensaje)
        if indice_productos.buscar_por_id(id_producto):
            return id_producto
        print("\n╔════════════════════════════╗")
        print("║       No encontrado         ║")
        print("╚════════════════════════════╝")

def update_stock(file_name, id_producto, nuevo_stock):
    with open(file_name, 'r') as file:
        lines = file.readlines()
    
    for i in range(1, len(lines)):
        partes = lines[i].strip().split(',')
        if partes[0] == id_producto:
            lines[i] = (partes[0] + "," + partes[1] + "," + partes[2] + "," + partes[3] + "," + str(nuevo_stock) + "," + partes[5] + "\n")
            break
    
    with open(file_name, 'w') as file:
        file.writelines(lines)

def validar_stock(file_name, id_producto, cantidad,tipo):
    with open(file_name, 'r') as file:
        if tipo == 2:
            for line in file:
                 partes = line.strip().split(',')
                 if partes[0] == id_producto:
                    stock_actual = int(partes[4])
                    if stock_actual >= int(cantidad):
                        nuevo_stock = stock_actual - int(cantidad)
                        update_stock(file_name, id_producto, nuevo_stock)
                        return True
                    else:
                        print("\n╔════════════════════════════╗")
                        print("║  Cantidad de producto no   ║")
                        print("║  disponible                ║")
                        print("╚════════════════════════════╝")
                        return False
        if tipo == 1:
            for line in file:
                 partes = line.strip().split(',')
                 if partes[0] == id_producto:
                        stock_actual = int(partes[4])
                        nuevo_stock = stock_actual + int(cantidad)
                        update_stock(file_name, id_producto, nuevo_stock)
                        return True

def productos_mas_vendidos(archivo_ventas):
    
    with open(archivo_ventas, 'r') as file:
        file.readline()  
        conteo_ventas = {}

        for linea in file:
            datos = linea.strip().split(',')
            producto = datos[1]  
            cantidad = int(datos[2])  
            if producto in conteo_ventas:
                conteo_ventas[producto] += cantidad
            else:
                conteo_ventas[producto] = cantidad

    productos = [[k, v] for k, v in conteo_ventas.items()]
    for i in range(len(productos)):
        for j in range(i + 1, len(productos)):
            if productos[i][1] < productos[j][1]:  
                productos[i], productos[j] = productos[j], productos[i]

    print("\n Productos más vendidos:")
    for i in range(min(5, len(productos))):
        print(f"- {productos[i][0]}: {productos[i][1]} unidades vendidas")

            
            
def productos_menor_stock(archivo_productos):
    
    with open(archivo_productos, 'r') as file:
        file.readline()  
        productos_stock = []

        for linea in file:
            datos = linea.strip().split(',')
            if len(datos) > 4:  
                nombre = datos[1]  
                
                stock = int(datos[4])  
                productos_stock.append([nombre, stock])
                
                
    for i in range(len(productos_stock)):
        for j in range(i + 1, len(productos_stock)):
            if productos_stock[i][1] > productos_stock[j][1]:  
                productos_stock[i], productos_stock[j] = productos_stock[j], productos_stock[i]

    print("\n Productos con menor stock:")
    for i in range(min(5, len(productos_stock))):
        print(f"- {productos_stock[i][0]}: {productos_stock[i][1]} unidades disponibles")


def ventas_por_periodo(archivo_ventas, fecha_inicio, fecha_fin):

    with open(archivo_ventas, 'r') as file:
        file.readline()  
        ventas_filtradas = []

        for linea in file:
            datos = linea.strip().split(',')
            fecha = datos[3]  

            
            if fecha_inicio <= fecha <= fecha_fin:
                ventas_filtradas.append(datos)

    print(f"\nVentas desde {fecha_inicio} hasta {fecha_fin}:")
    if not ventas_filtradas:
        print("No hay ventas en este período.")
    else:
        for venta in ventas_filtradas:
            print(f"- {venta[1]}: {venta[2]} unidades (Fecha: {venta[3]})")
            
def proveedores_frecuentes(archivo_productos):
    
    with open(archivo_productos, 'r') as file:
        file.readline()  
        conteo_proveedores = {}

        for linea in file:
            datos = linea.strip().split(',')
            if len(datos) > 6:  
                proveedor = datos[6]  
                
                if proveedor in conteo_proveedores:
                    conteo_proveedores[proveedor] += 1
                else:
                    conteo_proveedores[proveedor] = 1


    proveedores = [[k, v] for k, v in conteo_proveedores.items()]
    for i in range(len(proveedores)):
        for j in range(i + 1, len(proveedores)):
            if proveedores[i][1] < proveedores[j][1]:  
                proveedores[i], proveedores[j] = proveedores[j], proveedores[i]

    
    print("\n Proveedores más frecuentes:")
    for i in range(min(5, len(proveedores))):
        print(f"- {proveedores[i][0]}: {proveedores[i][1]} productos")
                
def register_provider(providers_file):
    print("\n--- Registrar Proveedor ---")
    id_proveedor = str(Archivo(providers_file).contar_lineas())
    nombre = input("Nombre del proveedor: ")
    contacto = input("Contacto: ")
    direccion = input("Dirección: ")
    with open(providers_file, 'a') as file:
            file.write(f"{id_proveedor},{nombre},{contacto},{direccion}\n")
    indice = Indice(indexprovedor)
    indice.crear_indice(providers_file, id_proveedor) 
    
    print("Proveedor agregado con éxito.")
    
    
def register_venta(archivo_ventas, indice_productos):
    print("\n┌─────────────────────────────────────┐")
    print("│        REGISTRAR NUEVA VENTA        │")
    print("└─────────────────────────────────────┘")
    id_venta = str(Archivo(archivo_ventas).contar_lineas())
    id_producto = validar_producto("| ID Producto: ", indice_productos)
    id_cliente = validar_input("| ID Cliente: ")
    
    print("\n--- Fecha de venta ---")
    dia = str(validar_fecha("| Día: ", 1))
    mes = str(validar_fecha("| Mes: ", 2))
    año = str(validar_fecha("| Año: ", 3))
    fecha_venta = str(dia) + "/" + str(mes) + "/" + str(año)
    cantidad = validar_input("| Cantidad: ")
    while cantidad==0:
        print("Por favor digite un valor valido")
        cantidad = validar_input("| Cantidad: ")
    validar_stock(products_file, id_producto, cantidad,2)

    with open(archivo_ventas, 'a') as file:
            file.write(f"{id_venta},{id_producto},{id_cliente},{fecha_venta},{cantidad}\n")
        
    indice = Indice(indexventas)
    indice.crear_indice(archivo_ventas)
        
    print("\n┌─────────────────────────────────────┐")
    print("│     ✔ Venta registrada con éxito     │")
    print("└──────────────────────────────────────┘")

def realizar_compra(archivo_compras, indice_productos, indice_proveedores):
    print("\n┌─────────────────────────────────────┐")
    print("│        REGISTRAR NUEVA COMPRA       │")
    print("└─────────────────────────────────────┘")
    id_compra = str(Archivo(archivo_compras).contar_lineas())
    
    id_producto = validar_producto("ID Producto: ", indice_productos)
    id_proveedor = validar_producto("ID Proveedor: ", indice_proveedores)
    
    print("\n--- Fecha de compra ---")
    dia = str(validar_fecha("| Día: ", 1))
    mes = str(validar_fecha("| Mes: ", 2))
    año = str(validar_fecha("| Año: ", 3))
    fecha_compra = str(dia) + "/" + str(mes) + "/" + str(año)
    cantidad = validar_input("| Cantidad: ")
    while cantidad==0:
        print("Por favor digite un valor valido")
        cantidad = validar_input("| Cantidad: ")
    validar_stock(products_file, id_producto, cantidad,1)
    
    with open(archivo_compras, 'a') as file:
        file.write(f"{id_compra},{id_producto},{id_proveedor},{fecha_compra},{cantidad}\n")
    
    indice = Indice(indexcompras)
    indice.crear_indice(archivo_compras)
    
    print("\n┌─────────────────────────────────────┐")
    print("│  ✔ Compra registrada con éxito      │")
    print("└─────────────────────────────────────┘")

def inicializar_archivos():
    
    archivo_prod = Archivo(products_file)
    archivo_prod.abrir_archivo(['id', 'nombre', 'categoria', 'precio', 'stock', 'descripcion', 'proveedor'])
    for producto in products_data:
        archivo_prod.escribir_archivo(list(producto.values()))
    
    
    archivo_prov = Archivo(providers_file)
    archivo_prov.abrir_archivo(['id', 'nombre', 'contacto', 'direccion'])
    for proveedor in providers_data:
        archivo_prov.escribir_archivo(list(proveedor.values()))
    
    
    archivo_ventas = Archivo(sales_file)
    archivo_ventas.abrir_archivo(['id', 'id_producto', 'id_cliente', 'fecha_venta', 'cantidad'])
    for venta in sales_data:
        archivo_ventas.escribir_archivo(list(venta.values()))
    
    
    archivo_compras = Archivo(purchases_file)
    archivo_compras.abrir_archivo(['id', 'id_producto', 'id_proveedor', 'fecha_compra', 'cantidad'])
    for compra in purchases_data:
        archivo_compras.escribir_archivo(list(compra.values()))
    
    
    indice_productos = Indice(indexproduct)
    indice_productos.crear_indice(products_file)
    
    indice_proveedores = Indice(indexprovedor)
    indice_proveedores.crear_indice(providers_file)
    
    indice_ventas = Indice(indexventas)
    indice_ventas.crear_indice(sales_file)
    
    indice_compras = Indice(indexcompras)
    indice_compras.crear_indice(purchases_file)

def main():
    
    
    inicializar_archivos()
    
    
    archivo_productos = Archivo(products_file)
    indice_productos = Indice(indexproduct)
    producto = Producto(archivo_productos, indice_productos)
    
    archivo_proveedores = Archivo(providers_file)
    indice_proveedores = Indice(indexprovedor)
    
    archivo_ventas = Archivo(sales_file)
    indice_ventas = Indice(indexventas)
    
    archivo_compras = Archivo(purchases_file)
    indice_compras = Indice(indexcompras)
    
    while True:
        print("\n╔══════════════════════════════════════════╗")
        print("║  MENÚ PRINCIPAL - GESTIÓN DE INVENTARIO  ║")
        print("╠══════════════════════════════════════════╣")
        print("║  1. Buscar productos                     ║")
        print("║  2. Registrar/Actualizar datos           ║")
        print("║  3. Gestionar compras                    ║")
        print("║  4. Visualizar                           ║")
        print("║  5. Reportes                             ║")
        print("║  6. Salir                                ║")
        print("╚══════════════════════════════════════════╝")
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            print("\n╔══════════════════════════════════════════╗")
            print("║           BUSCAR PRODUCTOS               ║")
            print("╠══════════════════════════════════════════╣")
            print("║  1. Buscar por nombre                    ║")
            print("║  2. Buscar por categoría                 ║")
            print("║  3. Buscar por proveedor                 ║")
            print("╚══════════════════════════════════════════╝")
            sub_opcion = input("Seleccione una opción: ")
            if sub_opcion == "1":
                nombre = validar_input("| Ingrese el nombre del producto: ")
                resultados = producto.buscar_por_nombre(nombre)
                if not resultados:
                    print("\n╔════════════════════════════╗")
                    print("║ No se encontraron productos║")
                    print("╚════════════════════════════╝")
            elif sub_opcion == "2":
                categoria = input("| Ingrese la categoría del producto: ").strip()
                resultados = producto.buscar_por_categoria(categoria)
                if not resultados:
                    print("\n╔════════════════════════════╗")
                    print("║ No se encontraron productos║")
                    print("╚════════════════════════════╝")
            
            elif sub_opcion == "3":
                proveedor = input("| Ingrese el proveedor: ").strip()
                resultados = producto.buscar_por_proveedor(proveedor)
                if not resultados:
                    print("\n╔════════════════════════════╗")
                    print("║ No se encontraron productos║")
                    print("╚════════════════════════════╝")
                        
            else:
                print("Opción no válida.")
        
        elif opcion == "2":
            print("\n╔══════════════════════════════════════════╗")
            print("║     REGISTRO Y ACTUALIZACIÓN DE DATOS    ║")
            print("╠══════════════════════════════════════════╣")
            print("║  1. Registrar producto                   ║")
            print("║  2. Registrar proveedor                  ║")
            print("║  3. Registrar venta                      ║")
            print("║  4. Eliminar producto                    ║")
            print("╚══════════════════════════════════════════╝")
            sub_opcion = input("Seleccione una opción: ")
            
            if sub_opcion == "1":
                producto.registrar_producto()
                
            elif sub_opcion == "2":
                register_provider(providers_file)
            elif sub_opcion == "3":
                register_venta(sales_file, indexventas, products_file, indice_productos)
            
            elif sub_opcion == "4":
                nombre = input("Ingrese el nombre del producto a eliminar: ")
                producto.eliminar_por_nombre(nombre)
            
            else:
                print("Ingrese valores válidos.")
        
        elif opcion == "3":
            print("\n╔══════════════════════════════════════════╗")
            print("║           GESTIÓN DE COMPRAS             ║")
            print("╠══════════════════════════════════════════╣")
            print("║  1. Registrar nueva compra               ║")
            print("║  2. Consultar compras                    ║")
            print("╚══════════════════════════════════════════╝")
            sub_opcion = input("Seleccione una opción: ")
            
            if sub_opcion == "1":
                realizar_compra(purchases_file, indice_productos, indice_proveedores)
            elif sub_opcion == "2":
                print("\nCompras realizadas:")
                archivo_compras.leer_archivo()
            else:
                print("Opción no válida.")
        
        elif opcion == "4":
            print("\n╔══════════════════════════════════════════╗")
            print("║              VISUALIZAR                  ║")
            print("╠══════════════════════════════════════════╣")
            print("║  1. Inventario de productos              ║")
            print("║  2. Ventas realizadas                    ║")
            print("╚══════════════════════════════════════════╝")
            sub_opcion = input("Seleccione una opción: ")
            
            if sub_opcion == "1":
                print("\nInventario de productos:")
                archivo_productos.leer_archivo()
            elif sub_opcion == "2":
                print("\nVentas realizadas:")
                archivo_ventas.leer_archivo()
            else:
                print("Opción no válida.")
                
        elif opcion == "5":
            print("\n╔══════════════════════════════════════════╗")
            print("║              REPORTES                    ║")
            print("╠══════════════════════════════════════════╣")
            print("║  1. Productos con menor stock            ║")
            print("║  2. Proveedores más frecuentes           ║")
            print("║  3. Productos más vendidos               ║")
            print("║  4. Ventas por período de tiempo         ║")
            print("╚══════════════════════════════════════════╝")
            sub_opcion = input("Seleccione una opción: ")

            if sub_opcion == "1":
                productos_menor_stock("products.csv")

            elif sub_opcion == "2":
                proveedores_frecuentes("products.csv")  

            elif sub_opcion == "3":
                productos_mas_vendidos("sales.csv", "products.csv")

            elif sub_opcion == "4":
                fecha_inicio = input("Ingrese la fecha de inicio (DD/MM/YYYY): ").strip()
                fecha_fin = input("Ingrese la fecha de fin (DD/MM/YYYY): ").strip()
                ventas_por_periodo("sales.csv", fecha_inicio, fecha_fin)

            else:
                print("Opción no válida, intente de nuevo.")
                 
        elif opcion == "6":
            print("\n╔══════════════════════════════════════════╗")
            print("║          ¡Hasta pronto!                  ║")
            print("╚══════════════════════════════════════════╝")
            break
        
        else:
            print("Opción no válida, intente de nuevo.")

if __name__ == '__main__':
    main()
