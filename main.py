from datetime import datetime
import mysql.connector


#Hola Mundo
# ESTO SIRVE PARA CONECTARNOS A NUESTRA BASE DE DATOS ( EN NUESTRO CASO LA HEMOS LLAMADO BASE DE DATOS)
def establecer_conexion():
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root1234",
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
    perfil = input("Ingrese su perfil ( proveedor, comprador o visitante): ")
    fecha_nacimiento = input("Ingrese su fecha de nacimiento (YYYY-MM-DD): ")

# COMPROBAMOS QUE EL PERFIL ES VÁLIDO
    perfiles_validos = ["proveedor", "comprador", "visitante"]
    if perfil.lower().strip() not in perfiles_validos:
        print("Perfil inválido. Los perfiles válidos son: proveedor, comprador, visitante.")
        return


    # AQUI COMPRUEBA LA EDAD PARA QUE EL USUARIO PUEDA CREAR REGISTRARSE, SI NO CUMPLE CON LOS REQUISITOS SE LE DENIEGA EL ACCESO
    edad = calcular_edad(fecha_nacimiento)
    if edad < 18:
        print("Lo siento, no puedes registrarte porque eres menor de edad.")
        return  # Finalizar la función si el usuario es menor de edad

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
    nombre_usuario = input("Ingrese su nombre de usuario: ")
    contraseña = input("Ingrese su contraseña: ")

    cursor = conexion.cursor() # ABRIMOS EL CURSOR PARA PODER EDITAR NUESTRA BASE DE DATOS
    # COMPROBAMOS QUE LOS DATOS DE INICIO DE SESION COINCIDEN CON LOS DATOS REGISTRADOS QUE TENEMOS EN NUESTRA BASE DE DATOS
    consulta = "SELECT * FROM usuarios WHERE nombre_usuario = %s AND contraseña = %s"
    consulta = "SELECT * FROM administrador WHERE nombre_usuario = %s AND contraseña = %s"
    valores = (nombre_usuario, contraseña)
    cursor.execute(consulta, valores)

    # ESTO SIRVE PARA OBTENER LA PRIMERA FILA ( NOMBRE Y USUARIO) QUE COINCIDA CON EL NOMBRE Y CONTRASEÑA QUE HAS ESCRITO AL INICIAR SESION
    # SI NO COINCIDE NO TE DEVUELVE NADA. ES DECIR NO INICIAS SESIÓN
    resultado = cursor.fetchone()






# AQUI SI EL RESULTADO DEL CURSOR ES FAVORABLE ( ES DECIR HA ENCONTRADO EN NUESTRA BBDD UN USUARIO CON UN NOMBRE Y CONTRASEÑA ALMACENADOS) TE DEJA INICIAR SESIÓN
    if resultado:
        print("Inicio de sesión exitoso")
        perfil = resultado[3].strip()
        print("Perfil:", perfil)
        if perfil == "administrador":
            conexion.close()
            conexion = establecer_conexion()
            menu_administrador(conexion)
        elif perfil == "visitante":
            menu_visitante(conexion)
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


# MENU DE ADMINISTRADOR
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
# AQUI EL ADMINISTRADOR PUEDE ELIMINAR USUARIOS QUE SE HAYAN REGISTRADO ( ESTO LO IMPLEMENTAREMOS CUANDO DESARROLLEMOS EL CODIGO DONDE LOS USUARIOS TENGAN QUE SUBIR UN DOCUMENTO PARA VERIFICAR LA EDAD

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

# MUESTRA LOS VINOS DENUESTRA BASE DE DATOS
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


# ORDENA A LOS VINOS SEGUN SU PRECIO DE FORMA ASCENDENTE
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


# MENU DE VISITANTE ( NO PUEDE REALIZAR NINGUNA COMPRA)
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
print(" saliendo del programa ")


