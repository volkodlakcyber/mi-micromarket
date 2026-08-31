import json
import os
from datetime import datetime

# Archivos de datos
ARCHIVO_INVENTARIO = "inventario.json"
ARCHIVO_VENTAS = "ventas.json"
ARCHIVO_PROVEEDORES = "proveedores.json"
ARCHIVO_COMPRAS = "compras.json"

# Configuración inicial
STOCK_MINIMO = 5

# Cargar datos existentes o crear estructuras vacías
if os.path.exists(ARCHIVO_INVENTARIO):
    with open(ARCHIVO_INVENTARIO, "r", encoding="utf-8") as f:
        inventario = json.load(f)
else:
    inventario = {}

if os.path.exists(ARCHIVO_VENTAS):
    with open(ARCHIVO_VENTAS, "r", encoding="utf-8") as f:
        historial_ventas = json.load(f)
else:
    historial_ventas = []

if os.path.exists(ARCHIVO_PROVEEDORES):
    with open(ARCHIVO_PROVEEDORES, "r", encoding="utf-8") as f:
        proveedores = json.load(f)
else:
    proveedores = {}

if os.path.exists(ARCHIVO_COMPRAS):
    with open(ARCHIVO_COMPRAS, "r", encoding="utf-8") as f:
        historial_compras = json.load(f)
else:
    historial_compras = []

# Funciones de guardado
def guardar_inventario():
    with open(ARCHIVO_INVENTARIO, "w", encoding="utf-8") as f:
        json.dump(inventario, f, indent=4, ensure_ascii=False)

def guardar_ventas():
    with open(ARCHIVO_VENTAS, "w", encoding="utf-8") as f:
        json.dump(historial_ventas, f, indent=4, ensure_ascii=False)

def guardar_proveedores():
    with open(ARCHIVO_PROVEEDORES, "w", encoding="utf-8") as f:
        json.dump(proveedores, f, indent=4, ensure_ascii=False)

def guardar_compras():
    with open(ARCHIVO_COMPRAS, "w", encoding="utf-8") as f:
        json.dump(historial_compras, f, indent=4, ensure_ascii=False)

def guardar_todos():
    guardar_inventario()
    guardar_ventas()
    guardar_proveedores()
    guardar_compras()

# Funciones auxiliares
def verificar_stock_bajo():
    if not inventario:
        return
    bajos = []
    for cod, datos in inventario.items():
        if datos["stock"] < STOCK_MINIMO:
            bajos.append((cod, datos["nombre"], datos["stock"]))
    if bajos:
        print("\n" + "⚠️ " + "="*35)
        print("   ALERTA: PRODUCTOS CON STOCK BAJO")
        print("="*40)
        for cod, nombre, stock in bajos:
            print(f"   📦 {cod} - {nombre}: {stock} unidades")
        print("="*40 + " ⚠️")
        print(f"   (Considera reponer antes de que se agoten)")
        print("="*40 + "\n")

def mostrar_menu():
    print("\n" + "="*40)
    print("   MICROMARKET - MENÚ PRINCIPAL")
    print("="*40)
    print("1. Agregar producto")
    print("2. Ver inventario")
    print("3. Vender producto")
    print("4. Buscar producto por nombre")
    print("5. Ver reporte de ventas (y exportar a CSV)")
    print("6. Editar producto")
    print("7. Eliminar producto")
    print("8. Configurar alerta de stock bajo")
    print("9. Gestionar categorías (ver/filtrar)")
    print("10. Registrar compra a proveedor")
    print("11. Buscar ventas por fecha")
    print("12. Salir")
    print("="*40)

# Funciones principales
def agregar_producto():
    print("\n--- NUEVO PRODUCTO ---")
    codigo = input("Código (ej: 001): ")
    if codigo in inventario:
        print("¡Ese código ya existe! Usa otro.")
        return
    nombre = input("Nombre: ")
    categoria = input("Categoría (ej: Lácteos, Bebidas): ").strip() or "Sin categoría"
    try:
        precio = float(input("Precio de venta (ej: 2.50): "))
    except:
        print("Precio inválido. Debe ser un número.")
        return
    try:
        costo = float(input("Precio de costo (ej: 1.80): "))
    except:
        print("Costo inválido. Se usará 0.")
        costo = 0
    try:
        stock = int(input("Cantidad en stock: "))
    except:
        print("Cantidad inválida. Debe ser un número entero.")
        return
    proveedor = input("Proveedor (nombre): ").strip() or "Sin proveedor"

    inventario[codigo] = {
        "nombre": nombre,
        "categoria": categoria,
        "precio": precio,
        "costo": costo,
        "stock": stock,
        "proveedor": proveedor
    }

    if proveedor not in proveedores:
        proveedores[proveedor] = []
    if codigo not in proveedores[proveedor]:
        proveedores[proveedor].append(codigo)

    guardar_inventario()
    guardar_proveedores()
    print(f"✅ Producto '{nombre}' agregado correctamente.")

def ver_inventario():
    if not inventario:
        print("\n📭 El inventario está vacío.")
        return
    print("\n--- INVENTARIO ACTUAL ---")
    print("Código | Nombre          | Categoría   | Precio | Costo | Stock | Proveedor")
    print("-"*80)
    for cod, datos in inventario.items():
        nombre = datos["nombre"].ljust(15)[:15]
        categoria = datos.get("categoria", "Sin categoría").ljust(12)[:12]
        precio = datos["precio"]
        costo = datos.get("costo", 0)
        stock = datos["stock"]
        proveedor = datos.get("proveedor", "Sin proveedor").ljust(15)[:15]
        marca = "*" if stock < STOCK_MINIMO else " "
        print(f" {cod}   | {nombre} | {categoria} | ${precio:5.2f} | ${costo:5.2f} | {stock:3}{marca} | {proveedor}")

def vender_producto():
    if not inventario:
        print("\n📭 No hay productos para vender.")
        return
    codigo = input("\nCódigo del producto a vender: ")
    if codigo not in inventario:
        print("❌ Producto no encontrado.")
        return
    producto = inventario[codigo]
    print(f"Producto: {producto['nombre']} - Stock: {producto['stock']} - Precio: ${producto['precio']}")
    try:
        cantidad = int(input("Cantidad a vender: "))
    except:
        print("Cantidad inválida.")
        return
    if cantidad <= 0:
        print("La cantidad debe ser mayor a cero.")
        return
    if cantidad > producto["stock"]:
        print(f"❌ Stock insuficiente. Solo hay {producto['stock']} unidades.")
        return

    producto["stock"] -= cantidad
    total = cantidad * producto["precio"]
    ganancia = cantidad * (producto["precio"] - producto.get("costo", 0))

    venta = {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "producto": producto["nombre"],
        "cantidad": cantidad,
        "precio_unitario": producto["precio"],
        "costo_unitario": producto.get("costo", 0),
        "total": total,
        "ganancia": ganancia
    }
    historial_ventas.append(venta)

    guardar_inventario()
    guardar_ventas()
    print(f"✅ Venta realizada. Total a pagar: ${total:.2f} (Ganancia: ${ganancia:.2f})")

def buscar_por_nombre():
    if not inventario:
        print("\n📭 El inventario está vacío.")
        return
    busqueda = input("\n🔍 Ingresa el nombre o parte del nombre a buscar: ").strip().lower()
    if not busqueda:
        print("❌ No ingresaste nada para buscar.")
        return
    encontrados = []
    for cod, datos in inventario.items():
        if busqueda in datos["nombre"].lower():
            encontrados.append((cod, datos))
    if not encontrados:
        print(f"❌ No se encontraron productos con '{busqueda}'.")
        return
    print(f"\n--- RESULTADOS DE BÚSQUEDA ({len(encontrados)} encontrados) ---")
    print("Código | Nombre          | Precio | Stock")
    print("-"*40)
    for cod, datos in encontrados:
        nombre = datos["nombre"].ljust(15)[:15]
        print(f" {cod}   | {nombre} | ${datos['precio']:5.2f} | {datos['stock']:3}")

def reporte_ventas():
    if not historial_ventas:
        print("\n📊 No hay ventas registradas aún.")
        return

    print("\n" + "="*50)
    print("   📊 REPORTE DE VENTAS")
    print("="*50)
    total_general = 0
    ganancia_total = 0
    for i, venta in enumerate(historial_ventas, 1):
        print(f"{i}. {venta['fecha']} - {venta['producto']} x{venta['cantidad']} = ${venta['total']:.2f} (Ganancia: ${venta.get('ganancia', 0):.2f})")
        total_general += venta['total']
        ganancia_total += venta.get('ganancia', 0)
    print("-"*50)
    print(f"💰 TOTAL GENERAL VENDIDO: ${total_general:.2f}")
    print(f"📈 GANANCIA TOTAL: ${ganancia_total:.2f}")
    print("="*50)

    # Exportar a CSV
    nombre_csv = "reporte_ventas.csv"
    ruta_csv = os.path.join(os.getcwd(), nombre_csv)
    try:
        with open(nombre_csv, "w", encoding="utf-8") as f:
            f.write("Fecha,Producto,Cantidad,Precio Unitario,Costo Unitario,Total,Ganancia\n")
            for venta in historial_ventas:
                f.write(f"{venta['fecha']},{venta['producto']},{venta['cantidad']},{venta['precio_unitario']:.2f},{venta.get('costo_unitario', 0):.2f},{venta['total']:.2f},{venta.get('ganancia', 0):.2f}\n")
        print("\n✅ Archivo CSV exportado correctamente.")
        print(f"📂 Ubicación: {ruta_csv}")
    except Exception as e:
        print(f"❌ Error al exportar CSV: {e}")

def editar_producto():
    if not inventario:
        print("\n📭 El inventario está vacío.")
        return
    codigo = input("\nCódigo del producto a editar: ")
    if codigo not in inventario:
        print("❌ Producto no encontrado.")
        return
    producto = inventario[codigo]
    print(f"Editando: {producto['nombre']} - Precio: ${producto['precio']} - Stock: {producto['stock']}")

    nuevo_nombre = input(f"Nuevo nombre (Enter para dejar '{producto['nombre']}'): ").strip()
    if nuevo_nombre:
        producto['nombre'] = nuevo_nombre

    nueva_categoria = input(f"Nueva categoría (Enter para dejar '{producto.get('categoria', 'Sin categoría')}'): ").strip()
    if nueva_categoria:
        producto['categoria'] = nueva_categoria

    try:
        nuevo_precio = input(f"Nuevo precio de venta (Enter para dejar ${producto['precio']}): ").strip()
        if nuevo_precio:
            producto['precio'] = float(nuevo_precio)
    except:
        print("Precio inválido, se mantiene el anterior.")

    try:
        nuevo_costo = input(f"Nuevo precio de costo (Enter para dejar ${producto.get('costo', 0)}): ").strip()
        if nuevo_costo:
            producto['costo'] = float(nuevo_costo)
    except:
        print("Costo inválido, se mantiene el anterior.")

    try:
        nuevo_stock = input(f"Nuevo stock (Enter para dejar {producto['stock']}): ").strip()
        if nuevo_stock:
            producto['stock'] = int(nuevo_stock)
    except:
        print("Stock inválido, se mantiene el anterior.")

    nuevo_proveedor = input(f"Nuevo proveedor (Enter para dejar '{producto.get('proveedor', 'Sin proveedor')}'): ").strip()
    if nuevo_proveedor:
        producto['proveedor'] = nuevo_proveedor

    guardar_inventario()
    guardar_proveedores()
    print("✅ Producto actualizado correctamente.")

def eliminar_producto():
    if not inventario:
        print("\n📭 El inventario está vacío.")
        return
    codigo = input("\nCódigo del producto a eliminar: ")
    if codigo not in inventario:
        print("❌ Producto no encontrado.")
        return
    producto = inventario[codigo]
    print(f"¿Estás seguro de eliminar '{producto['nombre']}' (código {codigo})?")
    confirmar = input("Escribe 'si' para confirmar: ").lower()
    if confirmar == "si":
        del inventario[codigo]
        guardar_inventario()
        print("🗑️ Producto eliminado correctamente.")
    else:
        print("Operación cancelada.")

def configurar_stock_minimo():
    global STOCK_MINIMO
    try:
        nuevo = int(input(f"Stock mínimo actual: {STOCK_MINIMO}. Ingresa nuevo valor (número entero): "))
        if nuevo >= 0:
            STOCK_MINIMO = nuevo
            print(f"✅ Stock mínimo actualizado a {STOCK_MINIMO}")
        else:
            print("❌ El valor debe ser mayor o igual a 0.")
    except:
        print("❌ Entrada inválida. Debe ser un número entero.")

def gestionar_categorias():
    while True:
        print("\n--- GESTIÓN DE CATEGORÍAS ---")
        print("1. Ver todas las categorías")
        print("2. Filtrar productos por categoría")
        print("3. Volver al menú principal")
        opcion = input("Elige una opción (1-3): ")
        if opcion == "1":
            categorias = set(datos.get("categoria", "Sin categoría") for datos in inventario.values())
            print("\n📂 Categorías existentes:")
            for cat in sorted(categorias):
                print(f"   - {cat}")
        elif opcion == "2":
            cat_buscar = input("Ingresa el nombre de la categoría a filtrar: ").strip()
            encontrados = []
            for cod, datos in inventario.items():
                if datos.get("categoria", "Sin categoría").lower() == cat_buscar.lower():
                    encontrados.append((cod, datos))
            if not encontrados:
                print(f"❌ No hay productos en la categoría '{cat_buscar}'.")
            else:
                print(f"\n--- PRODUCTOS EN CATEGORÍA '{cat_buscar}' ({len(encontrados)} encontrados) ---")
                print("Código | Nombre          | Precio | Stock")
                print("-"*40)
                for cod, datos in encontrados:
                    nombre = datos["nombre"].ljust(15)[:15]
                    print(f" {cod}   | {nombre} | ${datos['precio']:5.2f} | {datos['stock']:3}")
        elif opcion == "3":
            break
        else:
            print("⚠️ Opción no válida.")
        input("\nPresiona Enter para continuar...")

def registrar_compra():
    print("\n--- REGISTRO DE COMPRA A PROVEEDOR ---")
    proveedor = input("Nombre del proveedor: ").strip()
    if not proveedor:
        print("❌ El nombre del proveedor es obligatorio.")
        return
    codigo = input("Código del producto: ")
    if codigo not in inventario:
        print("❌ Producto no encontrado.")
        return
    try:
        cantidad = int(input("Cantidad comprada: "))
    except:
        print("❌ Cantidad inválida.")
        return
    if cantidad <= 0:
        print("❌ La cantidad debe ser mayor a 0.")
        return
    try:
        precio_costo = float(input("Precio de costo por unidad: "))
    except:
        print("❌ Precio inválido.")
        return
    if precio_costo <= 0:
        print("❌ El precio debe ser mayor a 0.")
        return

    producto = inventario[codigo]
    producto["stock"] += cantidad
    producto["costo"] = precio_costo
    producto["proveedor"] = proveedor

    compra = {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "proveedor": proveedor,
        "producto": producto["nombre"],
        "codigo": codigo,
        "cantidad": cantidad,
        "precio_costo": precio_costo,
        "total": cantidad * precio_costo
    }
    historial_compras.append(compra)

    if proveedor not in proveedores:
        proveedores[proveedor] = []
    if codigo not in proveedores[proveedor]:
        proveedores[proveedor].append(codigo)

    guardar_inventario()
    guardar_proveedores()
    guardar_compras()
    print(f"✅ Compra registrada. Stock de '{producto['nombre']}' ahora es {producto['stock']}.")

def buscar_ventas_por_fecha():
    if not historial_ventas:
        print("\n📊 No hay ventas registradas aún.")
        return
    fecha = input("Ingresa la fecha (formato YYYY-MM-DD, ej: 2026-08-30): ").strip()
    if not fecha:
        print("❌ Debes ingresar una fecha.")
        return
    encontradas = []
    for venta in historial_ventas:
        if venta["fecha"].startswith(fecha):
            encontradas.append(venta)
    if not encontradas:
        print(f"❌ No hay ventas en la fecha {fecha}.")
        return
    print(f"\n--- VENTAS DEL DÍA {fecha} ---")
    total_dia = 0
    for i, venta in enumerate(encontradas, 1):
        print(f"{i}. {venta['fecha']} - {venta['producto']} x{venta['cantidad']} = ${venta['total']:.2f}")
        total_dia += venta['total']
    print("-"*40)
    print(f"💰 TOTAL VENDIDO EL DÍA {fecha}: ${total_dia:.2f}")

# --- PROGRAMA PRINCIPAL ---
while True:
    verificar_stock_bajo()
    mostrar_menu()
    opcion = input("Elige una opción (1-12): ")
    if opcion == "1":
        agregar_producto()
    elif opcion == "2":
        ver_inventario()
    elif opcion == "3":
        vender_producto()
    elif opcion == "4":
        buscar_por_nombre()
    elif opcion == "5":
        reporte_ventas()
    elif opcion == "6":
        editar_producto()
    elif opcion == "7":
        eliminar_producto()
    elif opcion == "8":
        configurar_stock_minimo()
    elif opcion == "9":
        gestionar_categorias()
    elif opcion == "10":
        registrar_compra()
    elif opcion == "11":
        buscar_ventas_por_fecha()
    elif opcion == "12":
        guardar_todos()
        print("\n👋 ¡Hasta luego! Gracias por usar el sistema.")
        break
    else:
        print("⚠️ Opción no válida. Elige 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11 o 12.")
    input("\nPresiona Enter para continuar...")