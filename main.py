import json
import os
from datetime import datetime

ARCHIVO_INVENTARIO = "inventario.json"
ARCHIVO_VENTAS = "ventas.json"

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

def mostrar_menu():
    print("\n" + "="*40)
    print("   MICROMARKET - MENÚ PRINCIPAL")
    print("="*40)
    print("1. Agregar producto")
    print("2. Ver inventario")
    print("3. Vender producto")
    print("4. Buscar producto por nombre")
    print("5. Ver reporte de ventas")
    print("6. Salir")
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
        print(f" {cod}   | {nombre} | ${datos['precio']:5.2f} | {datos['stock']:3}")

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

while True:
    mostrar_menu()
    opcion = input("Elige una opción (1-6): ")
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
        guardar_inventario()
        guardar_ventas()
        print("\n👋 ¡Hasta luego! Gracias por usar el sistema.")
        break
    else:
        print("⚠️ Opción no válida. Elige 1, 2, 3, 4, 5 o 6.")
    input("\nPresiona Enter para continuar...")