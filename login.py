from datetime import datetime
import mysql.connector


# ESTO SIRVE PARA CONECTARNOS A NUESTRA BASE DE DATOS ( EN NUESTRO CASO LA HEMOS LLAMADO BASE DE DATOS)
def establecer_conexion():
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="BASE_DE_DATOS"
    )
    return conexion

# ESTO SIRVE PARA QUE CON LA FECHA QUE INTRODUZCA EL USUARIO SE PUEDA COMPROBAR QUE ES MAYOR DE EDAD
# FUNCIONA RESTANDOLE EL AÑO ACTUAL (2024) AL AÑO QUE INTRODUZCA EL USUARIO
def calcular_edad(fecha_nacimiento):
    fecha_nacimiento = datetime.strptime(fecha_nacimiento, "%Y-%m-%d")
    hoy = datetime.now()
    edad = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
    return edad

# ESTE ES EL LOGIN AL QUE ACCEDERÁ CADA USUARIO PARA REGISTRARSE
def registrar(conexion):
    nombre_usuario = input("Ingrese un nombre de usuario: ")
    correo = input("Ingrese un correo electrónico: ")
    contraseña = input("Ingrese una contraseña: ")
    perfil = input("Ingrese su perfil (proveedor, comprador o visitante): ")
    fecha_nacimiento = input("Ingrese su fecha de nacimiento (AÑO-MES-DIA): ")

    # COMPROBAMOS QUE EL PERFIL ES VÁLIDO
    perfiles_validos = ["proveedor", "comprador", "visitante"]
    if perfil.lower().strip() not in perfiles_validos:
        print("Perfil inválido. Los perfiles válidos son: proveedor, comprador, visitante.")
        return

    # AQUI COMPRUEBA LA EDAD PARA QUE EL USUARIO PUEDA CREAR REGISTRARSE, SI NO CUMPLE CON LOS REQUISITOS SE LE DENIEGA EL ACCESO
    edad = calcular_edad(fecha_nacimiento)
    if edad < 18:
        print("Lo siento, no puedes registrarte porque eres menor de edad.")
        return

    registrar_usuario(conexion, nombre_usuario, correo, contraseña, perfil, fecha_nacimiento)

# GUARDA EL REGISTRO DE LOS USUARIOS MAYORES DE EDAD EN LA BASE DE DATOS
# CONEXION ES UN OBJETO DE CONEXION A NUESTRA BASE DE DATOS
def registrar_usuario(conexion, nombre_usuario, correo, contraseña, perfil, fecha_nacimiento):
    cursor = conexion.cursor()
    try:
        consulta = "INSERT INTO usuarios (nombre_usuario, correo, contraseña, perfil, fecha_nacimiento) VALUES (%s, %s, %s, %s, %s)"
        valores = (nombre_usuario, correo, contraseña, perfil.lower().strip(), fecha_nacimiento)
        cursor.execute(consulta, valores)
        conexion.commit()
        print("Usuario registrado correctamente")
    except mysql.connector.Error as err:
        print(f"Error al registrar usuario: {err}")
    finally:
        cursor.close()

# ESTE APARTADO ES PARA INICIAR SESION ( LOS USUARIOS PREVIAMENTE REGISTRADOS O LOS ADMINS )
def iniciar_sesion(conexion):
    nombre_usuario = input("Ingrese tu nombre de usuario: ")
    contraseña = input("Ingrese tu contraseña: ")

    # SE CONECTA A LA BASE DE DATOS
    conexion = establecer_conexion()
    cursor = conexion.cursor()

    # BUSCA EN LA TABLA DE USUARIOS LOS USUARIOS REGISTRADOS PARA EL POSIBLE INICIO DE SESIÓN
    consulta_usuarios = "SELECT * FROM usuarios WHERE nombre_usuario = %s AND contraseña = %s"
    valores = (nombre_usuario, contraseña)
    cursor.execute(consulta_usuarios, valores)
    resultado_usuarios = cursor.fetchone()

    # BUSCA EN LA TABLA ADMINISTRADOR LOS USUARIOS GUARDADOS (EL USUARIO ES NUESTRO NOMBRE Y LA CONTRASEÑA ES 1234)
    consulta_administrador = "SELECT * FROM administrador WHERE nombre_usuario = %s AND contraseña = %s"
    cursor.execute(consulta_administrador, valores)
    resultado_administrador = cursor.fetchone()

# AQUI SI LOS DATOS DEL USUARIO REGUSTRADO COINCIDEN CON LOS DATOS DEL USUARIO QUE INTENTA INICIAR SESIÓN SE MUESTRA EL MENÚ DE DICHO USUARIO
    if resultado_usuarios:
        print("Inicio de sesión exitoso")
        perfil = resultado_usuarios[4].strip()
        print("Perfil:", perfil)
        if perfil == "visitante":
            menu_visitante(conexion)
        return
    elif resultado_administrador:
        print("Inicio de sesión exitoso como administrador")
        conexion.close()
        menu_administrador(establecer_conexion())  # Establecer nueva conexión
        return
    else:
        print("Nombre de usuario o contraseña incorrectos")

    cursor.close()

def mostrar_menu_administrador():
    print("\nMenú de administrador:")
    print("1. Ver usuarios y borrarlos de la bbdd")
    print("2. Salir del programa")

def mostrar_menu_visitante():
    print("\nMenú de visitante:")
    print("1. Ver todos los productos")
    print("2. Ver los más baratos")
    print("3. Salir del programa")

def menu_administrador(conexion):
    while True:
        mostrar_menu_administrador()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            eliminar_usuario(conexion)
        elif opcion == "2":
            break
        else:
            print("Opción inválida. Intente nuevamente.")

# ESTE APARTADO ES PARA QUE EL ADMIN PUEDA ELIMINAR A USUARIOS
# NOS SERVIRÁ PARA MAS TARDE CUANDO PIDAMOS QUE LOS USUARIOS SUBAN SU DOCUMENTACION PARA COMPROBAR QUE SON MAYORES DE EDAD
def eliminar_usuario(conexion):
    cursor = conexion.cursor()
    try:
        consulta = "SELECT nombre_usuario FROM usuarios"
        cursor.execute(consulta)
        usuarios = cursor.fetchall()

        if len(usuarios) == 0:
            print("No hay usuarios para eliminar.")
            return

        print("\nLista de usuarios:")
        for usuario in usuarios:
            print("Nombre:", usuario[0])

        nombre_usuario = input("Ingrese el nombre del usuario que desea eliminar: ")
        cursor.execute("DELETE FROM usuarios WHERE nombre_usuario = %s", (nombre_usuario,))
        conexion.commit()
        print("Usuario eliminado correctamente.")

    except mysql.connector.Error as err:
        print(f"Error al eliminar usuario: {err}")
    finally:
        cursor.close()

# AQUI MUESTRA LOS VINOS
def mostrar_vinos(conexion):
    cursor = conexion.cursor()
    consulta = "SELECT * FROM vinos"
    cursor.execute(consulta)
    vinos = cursor.fetchall()

    print("\nListado de vinos:")
    for vino in vinos:
        print("Nombre:", vino[0])
        print("Bodega:", vino[1])
        print("Región:", vino[2])
        print("Uva:", vino[3])
        print("Precio:", vino[4])
        print("----------")


# MUESTRA A LOS VINOS MAS BARATOS PRIMERO
def mostrar_vinos_mas_baratos(conexion):
    cursor = conexion.cursor()
    consulta = "SELECT nombre, bodega, region, uva, precio FROM vinos ORDER BY CAST(REPLACE(precio, ',', '.') AS DECIMAL) ASC"
    cursor.execute(consulta)
    vinos = cursor.fetchall()

    print("\nVinos más baratos:")
    for vino in vinos:
        print("Nombre:", vino[0])
        print("Precio:", vino[4])
        print("----------")

def menu_visitante(conexion):
    while True:
        mostrar_menu_visitante()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            mostrar_vinos(conexion)
        elif opcion == "2":
            mostrar_vinos_mas_baratos(conexion)
        elif opcion == "3":
            break
        else:
            print("Opción inválida. Intente nuevamente.")

conexion = establecer_conexion()

while True:
    print("\nMenú principal:")
    print("1. Registrarme")
    print("2. Iniciar sesión")
    print("3. Salir del programa")
    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        registrar(conexion)
    elif opcion == "2":

        iniciar_sesion(conexion)
    elif opcion == "3":
        break
    else:
        print("Opción inválida. Intente nuevamente.")

conexion.close()



def menu_comprador(conexion):
    while True:
        print("\nMenú de comprador:")
        print("1. Ver todos los productos")
        print("2. Ver los más baratos")
        print("3. agregar producto")
        print("4. Dejar reseña")
        print("5. Salir del programa")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            mostrar_vinos(conexion)
        elif opcion == "2":
            mostrar_vinos_mas_baratos(conexion)
        elif opcion == "3":
            agregar_producto(conexion)
        elif opcion == "4":
            dejar_resena(conexion)
        elif opcion == "5":
            break
        else:
            print("Opción incorrecta, elija una opción válida (1-5).")
def agregar_producto(conexion):
    nombre = input("Ingrese el nombre del producto: ")
    descripcion = input("Ingrese la descripción del producto: ")
    precio = input("Ingrese el precio del producto: ")
    cantidad = input("Ingrese la cantidad disponible del producto: ")

    cursor = conexion.cursor()
    try:
        consulta = " Decribe el producto (nombre, descripcion, precio, cantidad_disponible) VALOR   (%s, %s, %s, %s)"
        valores = (nombre, descripcion, precio, cantidad)
        cursor.execute(consulta, valores)
        conexion.commit()
        print("Producto agregado ")
    except mysql.connector.Error as err:
        print(f"Error al agregar producto: {err}")
    finally:
        cursor.close()
def dejar_resena(conexion):
    nombre_producto = input("Ingrese el nombre del producto al que desea dejar una reseña: ")
    calificacion = input("Ingrese una calificación (del 1 al 5): ")
    comentario = input("Deje un comentario sobre el producto: ")

    cursor = conexion.cursor()
    try:
        consulta = "INSERT INTO resenas (nombre_producto, calificacion, comentario) VALUES (%s, %s, %s)"
        valores = (nombre_producto, calificacion, comentario)
        cursor.execute(consulta, valores)
        conexion.commit()
        print("Reseña dejada correctamente")
    except mysql.connector.Error as err:
        print(f"Error al dejar reseña: {err}")
    finally:
        cursor.close()
def menu_proveedor(conexion):
    while True:
        print("\nMenú de proveedor:")
        print("1. Ver productos")
        print("2. Agregar nuevo producto")
        print("3. Ver reseñas de los compradores")
        print("4. Salir del programa")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            mostrar_productos(conexion)
        elif opcion == "2":
            agregar_producto(conexion)
        elif opcion == "3":
            ver_reseñas_compradores(conexion)
        elif opcion == "4":
            break
        else:
            print("Opción incorrecta, elija una opción válida (1-4).")
def mostrar_productos(conexion):
    cursor = conexion.cursor()
    consulta = "SELECT * FROM productos"
    cursor.execute(consulta)
    productos = cursor.fetchall()

    print("\nListado de productos:")
    for producto in productos:
        print("Nombre:", producto[1])
        print("Descripción:", producto[2])
        print("Precio:", producto[3])
        print("Cantidad disponible:", producto[4])
        print("----------")
def agregar_producto(conexion):
    nombre = input("Ingrese el nombre del producto: ")
    descripcion = input("Ingrese la descripción del producto: ")
    precio = input("Ingrese el precio del producto: ")
    cantidad = input("Ingrese la cantidad disponible del producto: ")

    cursor = conexion.cursor()
    try:
        consulta = "INSERT INTO productos (nombre, descripcion, precio, cantidad_disponible) VALUES (%s, %s, %s, %s)"
        valores = (nombre, descripcion, precio, cantidad)
        cursor.execute(consulta, valores)
        conexion.commit()
        print("Producto agregado correctamente")
    except mysql.connector.Error as err:
        print(f"Error al agregar producto: {err}")
    finally:
        cursor.close()


def ver_reseñas_compradores(conexion):
    cursor = conexion.cursor()
    try:
        consulta = "SELECT * FROM reseñas"
        cursor.execute(consulta)
        reseñas = cursor.fetchall()

        if not reseñas:
            print("No hay reseñas disponibles.")
        else:
            print("\nReseñas de los compradores:")
            for reseña in reseñas:
                print("Usuario:", reseña[1])
                print("Producto:", reseña[2])
                print("Reseña:", reseña[3])
                print("----------")
    except mysql.connector.Error as err:
        print(f"Error al obtener reseñas: {err}")
    finally:
        cursor.close()