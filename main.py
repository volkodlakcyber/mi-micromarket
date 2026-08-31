import json
import os
from datetime import datetime

ARCHIVO_INVENTARIO = "inventario.json"
ARCHIVO_VENTAS = "ventas.json"
STOCK_MINIMO = 5  # <--- AJUSTA ESTE NÚMERO SEGÚN TU NECESIDAD

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

def guardar_inventario():
    with open(ARCHIVO_INVENTARIO, "w", encoding="utf-8") as f:
        json.dump(inventario, f, indent=4, ensure_ascii=False)

def guardar_ventas():
    with open(ARCHIVO_VENTAS, "w", encoding="utf-8") as f:
        json.dump(historial_ventas, f, indent=4, ensure_ascii=False)

def verificar_stock_bajo():
    """Revisa productos con stock menor al mínimo y muestra alerta."""
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
    print("5. Ver reporte de ventas")
    print("6. Editar producto")
    print("7. Eliminar producto")
    print("8. Salir")
    print("="*40)

def agregar_producto():
    print("\n--- NUEVO PRODUCTO ---")
    codigo = input("Código (ej: 001): ")
    if codigo in inventario:
        print("¡Ese código ya existe! Usa otro.")
        return
    nombre = input("Nombre: ")
    try:
        precio = float(input("Precio (ej: 2.50): "))
    except:
        print("Precio inválido. Debe ser un número.")
        return
    try:
        stock = int(input("Cantidad en stock: "))
    except:
        print("Cantidad inválida. Debe ser un número entero.")
        return
    inventario[codigo] = {"nombre": nombre, "precio": precio, "stock": stock}
    guardar_inventario()
    print(f"✅ Producto '{nombre}' agregado correctamente.")

def ver_inventario():
    if not inventario:
        print("\n📭 El inventario está vacío.")
        return
    print("\n--- INVENTARIO ACTUAL ---")
    print("Código | Nombre          | Precio | Stock")
    print("-"*40)
    for cod, datos in inventario.items():
        nombre = datos["nombre"].ljust(15)[:15]
        stock = datos["stock"]
        # Marcar con un * si el stock es bajo
        marca = "*" if stock < STOCK_MINIMO else " "
        print(f" {cod}   | {nombre} | ${datos['precio']:5.2f} | {stock:3}{marca}")

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
    venta = {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "producto": producto["nombre"],
        "cantidad": cantidad,
        "precio_unitario": producto["precio"],
        "total": total
    }
    historial_ventas.append(venta)
    guardar_inventario()
    guardar_ventas()
    print(f"✅ Venta realizada. Total a pagar: ${total:.2f}")

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
    for i, venta in enumerate(historial_ventas, 1):
        print(f"{i}. {venta['fecha']} - {venta['producto']} x{venta['cantidad']} = ${venta['total']:.2f}")
        total_general += venta['total']
    print("-"*50)
    print(f"💰 TOTAL GENERAL VENDIDO: ${total_general:.2f}")
    print("="*50)

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
    try:
        nuevo_precio = input(f"Nuevo precio (Enter para dejar ${producto['precio']}): ").strip()
        if nuevo_precio:
            producto['precio'] = float(nuevo_precio)
    except:
        print("Precio inválido, se mantiene el anterior.")
    try:
        nuevo_stock = input(f"Nuevo stock (Enter para dejar {producto['stock']}): ").strip()
        if nuevo_stock:
            producto['stock'] = int(nuevo_stock)
    except:
        print("Stock inválido, se mantiene el anterior.")
    guardar_inventario()
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

# --- PROGRAMA PRINCIPAL ---
while True:
    verificar_stock_bajo()  # <--- NUEVA ALERTA AL INICIO DE CADA CICLO
    mostrar_menu()
    opcion = input("Elige una opción (1-8): ")
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
        guardar_inventario()
        guardar_ventas()
        print("\n👋 ¡Hasta luego! Gracias por usar el sistema.")
        break
    else:
        print("⚠️ Opción no válida. Elige 1, 2, 3, 4, 5, 6, 7 u 8.")
    input("\nPresiona Enter para continuar...")