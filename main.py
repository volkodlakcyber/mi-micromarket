import json
import os
from datetime import datetime

# Archivos de datos
ARCHIVO_INVENTARIO = "inventario.json"
ARCHIVO_VENTAS = "ventas.json"

# Cargar inventario
if os.path.exists(ARCHIVO_INVENTARIO):
    with open(ARCHIVO_INVENTARIO, "r", encoding="utf-8") as f:
        inventario = json.load(f)
else:
    inventario = {}

# Cargar historial de ventas
if os.path.exists(ARCHIVO_VENTAS):
    with open(ARCHIVO_VENTAS, "r", encoding="utf-8") as f:
        ventas = json.load(f)
else:
    ventas = []

def guardar_inventario():
    with open(ARCHIVO_INVENTARIO, "w", encoding="utf-8") as f:
        json.dump(inventario, f, indent=4, ensure_ascii=False)

def guardar_ventas():
    with open(ARCHIVO_VENTAS, "w", encoding="utf-8") as f:
        json.dump(ventas, f, indent=4, ensure_ascii=False)

def mostrar_menu():
    print("\n" + "="*50)
    print("        MICROMARKET - MENÚ PRINCIPAL")
    print("="*50)
    print("1. Agregar producto")
    print("2. Ver inventario")
    print("3. Vender producto")
    print("4. Ver reporte de ventas")
    print("5. Salir")
    print("="*50)

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
    # Restar stock
    producto["stock"] -= cantidad
    guardar_inventario()
    total = cantidad * producto["precio"]
    # Registrar venta
    venta = {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "producto": producto["nombre"],
        "codigo": codigo,
        "cantidad": cantidad,
        "precio_unitario": producto["precio"],
        "total": total
    }
    ventas.append(venta)
    guardar_ventas()
    print(f"✅ Venta realizada. Total a pagar: ${total:.2f}")

def ver_reporte_ventas():
    if not ventas:
        print("\n📭 No hay ventas registradas aún.")
        return
    print("\n" + "="*60)
    print("           REPORTE DE VENTAS")
    print("="*60)
    total_general = 0
    for i, venta in enumerate(ventas, 1):
        print(f"{i}. {venta['fecha']} | {venta['producto']} x{venta['cantidad']} | ${venta['total']:.2f}")
        total_general += venta["total"]
    print("-"*60)
    print(f"💰 TOTAL GENERAL DE VENTAS: ${total_general:.2f}")
    print("="*60)

# --- PROGRAMA PRINCIPAL ---
while True:
    mostrar_menu()
    opcion = input("Elige una opción (1-5): ")
    if opcion == "1":
        agregar_producto()
    elif opcion == "2":
        ver_inventario()
    elif opcion == "3":
        vender_producto()
    elif opcion == "4":
        ver_reporte_ventas()
    elif opcion == "5":
        guardar_inventario()
        guardar_ventas()
        print("\n👋 ¡Hasta luego! Gracias por usar el sistema.")
        break
    else:
        print("⚠️ Opción no válida. Elige 1, 2, 3, 4 o 5.")
    input("\nPresiona Enter para continuar...")