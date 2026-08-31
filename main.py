import json
import os

# Archivo donde se guardarán los datos
ARCHIVO_DATOS = "inventario.json"

# Cargar inventario si existe
if os.path.exists(ARCHIVO_DATOS):
    with open(ARCHIVO_DATOS, "r", encoding="utf-8") as f:
        inventario = json.load(f)
else:
    inventario = {}

def guardar_datos():
    with open(ARCHIVO_DATOS, "w", encoding="utf-8") as f:
        json.dump(inventario, f, indent=4, ensure_ascii=False)

def mostrar_menu():
    print("\n" + "="*40)
    print("   MICROMARKET - MENÚ PRINCIPAL")
    print("="*40)
    print("1. Agregar producto")
    print("2. Ver inventario")
    print("3. Vender producto")
    print("4. Salir")
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
    guardar_datos()
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
    guardar_datos()
    total = cantidad * producto["precio"]
    print(f"✅ Venta realizada. Total a pagar: ${total:.2f}")

# --- PROGRAMA PRINCIPAL ---
while True:
    mostrar_menu()
    opcion = input("Elige una opción (1-4): ")
    if opcion == "1":
        agregar_producto()
    elif opcion == "2":
        ver_inventario()
    elif opcion == "3":
        vender_producto()
    elif opcion == "4":
        guardar_datos()
        print("\n👋 ¡Hasta luego! Gracias por usar el sistema.")
        break
    else:
        print("⚠️ Opción no válida. Elige 1, 2, 3 o 4.")
    input("\nPresiona Enter para continuar...")