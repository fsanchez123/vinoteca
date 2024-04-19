import mysql.connector
from mysql.connector import Error, cursor
from datetime import datetime
class conexion():
 def __init__(self,host,user,password,database):
  try:
    self.conexion = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database,

    )
    cursor = mi_conexion.cursor()

    if self.conexion.is_connected():
        print("Conexion Exitosa")
        cursor = conexion.cursor()
        cursor.execute()
  except Error as ex:
        print("Error al conectar con la base de datos", ex)



class Usuario:
    def __init__(self, correo, contraseña, perfil, id_usuario, permisos, fecha_nacimiento):
        self.correo = correo
        self.perfil = perfil
        self.id_usuario = id_usuario
        self.permisos = permisos
        self.fecha_nacimiento = fecha_nacimiento


    def registrar(id_usuario,correo,contraseña,perfil,fecha_nacimiento,edad_nacimiento):

        try:
            consulta = "INSERT INTO usuarios (id_usuario,nombre,correo, contraseña, perfil, fecha_nacimiento) VALUES (%s, %s, %s, %s, %s)"
            valores = (id_usuario, correo, contraseña, perfil.lower().strip(), fecha_nacimiento)
            cursor.execute(consulta, valores)
            conexion.commit()
            print("Usuario registrado correctamente")
        except mysql.connector.Error as err:
            print(f"Error al registrar usuario: {err}")
        finally:
            cursor.close()

    def iniciar_sesion(self, id_usuario, contraseña):
        cursor = conexion.cursor()
        id_usuario = input("Ingrese su nombre de usuario: ")
        contraseña = input("Ingrese su contraseña: ")

        # BUSCA EN LA TABLA DE USUARIOS LOS USUARIOS REGISTRADOS PARA EL POSIBLE INICIO DE SESIÓN
        consulta_usuarios = "SELECT * FROM usuarios WHERE id_usuario = %s AND contraseña = %s"
        valores = (id_usuario, contraseña)
        cursor.execute(consulta_usuarios, valores)
        resultado_usuarios = cursor.fetchone()

        # BUSCA EN LA TABLA ADMINISTRADOR LOS USUARIOS GUARDADOS (EL USUARIO ES NUESTRO NOMBRE Y LA CONTRASEÑA ES 1234)
        consulta_administrador = "SELECT * FROM administrador WHERE id_usuario = %s AND contraseña = %s"
        cursor.execute(consulta_administrador, valores)
        resultado_administrador = cursor.fetchone()
        cursor.close()
        print("Opción inválida. Intente nuevamente.")


class visitante(Usuario):
    def __init__(self, correo, contraseña, perfil, id_usuario, permisos, fecha_nacimiento,):
        super().__init__(correo, contraseña, perfil, id_usuario, permisos, fecha_nacimiento)
    def mostrar_advertencia(visitante):
        print(
            "\nNuestra aplicación está dedicada única y exclusivamente a la venta de vinos a los mayores de edad. \n\nEn la Vinoteca, tomamos muy en serio la responsabilidad social y cumplimos con todas las regulaciones legales para asegurar que el \nalcohol sólo sea accesible para personas que han alcanzado la mayoría de edad legal para su consumo.")


    def mostrar_vinos(self):
        cursor = conexion.cursor()
        consulta = "SELECT * FROM VINOS"
        cursor.execute(consulta)
        vinos = cursor.fetchall()

        print("\nListado de vinos:")
        for vino in vinos:
            print("Nombre:", vino[0])
            print("Bodega:", vino[1])
            print("Región:", vino[2])
            print("Uva:", vino[3])
            print("Precio:", vino[4])

    def mostrar_vinos_mas_baratos(self):
        cursor = conexion.cursor()
        consulta = "SELECT nombre, bodega, region, uva, precio FROM VINOS ORDER BY CAST(REPLACE(precio, ',', '.') AS DECIMAL) ASC"
        cursor.execute(consulta)
        vinos = cursor.fetchall()
        print("\nVinos más baratos:")
        for vino in vinos:
            print("Nombre:", vino[0])
            print("Precio:", vino[4])




class comprador(visitante):
    def __init__(self, correo, contraseña, perfil, id_usuario, permisos, fecha_nacimiento):
        super().__init__(correo, contraseña, perfil, id_usuario, permisos, fecha_nacimiento)
    def mostrar_vinos_mas_baratos(self):
        super().mostrar_vinos()
    def mostrar_vinos(self):
        super().mostrar_vinos()
    def dejar_reseña(self,nombre, valoracion, likes, opinion, comprador_id):
        comprador_id = input("Su usuario: ")
        nombre = input("Ingrese el nombre del producto al que desea dejar una reseña: ")
        valoracion = input("Ingrese una calificación (del 1 al 5): ")
        likes = input("si o no")
        opinion = input("Deje un comentario sobre el producto: ")

        cursor = conexion.cursor()
        try:
            consulta = "INSERT INTO reseñas (comprador_id, nombre, valoracion,likes, opinion)VALUES (%s, %s, %s, %s, %s)"
            valores = (comprador_id, nombre, valoracion, likes, opinion)
            cursor.execute(consulta, valores)
            conexion.commit()
            print("Reseña dejada correctamente")
        except mysql.connector.Error as err:
            print(f"Error al dejar reseña: {err}")
        finally:
            cursor.close()

    def comprar_vinos(self,nombre):
        nombre = input("Ingrese el nombre del vino")
        cursor = conexion.cursor()
        consulta = "SELECT nombre FROM VINOS"
        cursor.execute(consulta)
        vinos = cursor.fetchall()

class proveedor(Usuario):
    def __init__(self, correo, contraseña, perfil, id_usuario, permisos, fecha_nacimiento):
        super().__init__(correo, contraseña, perfil, id_usuario, permisos, fecha_nacimiento)

        def mostrar_vinos_proveedor(self,nombre):
            nombre = input("Ingrese el nombre del vino: ")
            cursor = conexion.cursor()
            consulta = "SELECT * FROM VINOS WHERE nombre =%s"
            valores=(nombre)
            cursor.execute(consulta,valores)
            productos = cursor.fetchall()
            print("\nListado de productos:")
            for producto in vino:
                print("Nombre:", producto[1])

        def agregar_vino(self,nombre, bodega, region, uva, precio):
            nombre = input("Ingrese el nombre del vino: ")
            bodega = input("Ingrese la bodega vino: ")
            region=input("Ingrese la region dek vino")
            uva=input("Ingrese el tipo de uva")
            precio =input("Ingrese el precio del vino: ")
            cursor = conexion.cursor()
            try:
                consulta = "INSERT INTO VINOS (nombre,bodega,region,uva,precio) VALUES (%s,%s,%s,%s,%s) "
                valores = (nombre, bodega,region,uva, precio)
                cursor.execute(consulta, valores)
                conexion.commit()
                print("vino agregado correctamente")
            except mysql.connector.Error as err:
                print(f"Error al agregar vino: {err}")
            finally:
                cursor.close()
        def eliminar_vino(self,nombre, bodega, region, uva, precio):
            nombre = input("Ingrese el nombre del vino: ")
            bodega = input("Ingrese la bodega vino: ")
            region = input("Ingrese la region dek vino")
            uva = input("Ingrese el tipo de uva")
            precio = input("Ingrese el precio del vino: ")
            cursor = conexion.cursor()
            try:
                consulta = "DELETE FROM VINOS WHERE nombre = %s AND bodega = %s AND uva = %s AND region = %s AND precio = %s"
                valores = (nombre, bodega, region, uva, precio)
                conexion.commit()
                print("vino eliminado correctamente")
            except mysql.connector.Error as err:
                print(f"Error al eliminar vino: {err}")
            finally:
                cursor.close()

        def ver_reseñas_compradores(id_usuario, valoracion, likes, opinion):
            cursor = conexion.cursor()
            try:
                id_usuario=input("ingrese el nombre ")
                valoracion=input("ingrese la valoracion")
                likes=input("ingrese el like")
                opinion=input("ingrese la opinion")
                consulta = "SELECT * FROM RESEÑAS"
                cursor.execute(consulta)
                reseñas = cursor.fetchall()

                if not reseñas:
                    print("No hay reseñas disponibles.")
                else:
                    print("\nReseñas de los compradores:")
                    for reseña in reseñas:
                        print("Comprador ID:", reseña[0])
                        print("Nombre:", reseña[1])
                        print("Valoración:", reseña[2])
                        print("Likes:", reseña[3])
                        print("Opinión:", reseña[4])
            except mysql.connector.Error as err:
                print(f"Error al obtener reseñas: {err}")




class administrador(Usuario):
    def __init__(self, correo, contraseña, perfil, id_usuario, permisos, fecha_nacimiento):
        super().__init__(correo, contraseña, perfil, id_usuario, permisos, fecha_nacimiento)

    def eliminar_usuario(self,nombre_usuario):
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
class vino:
    def __init__(self,nombre,bodega,region,uva,precio,prices_old,likes,valoracion,opinion,vinificacion):
        self.nombre = nombre
        self.bodega = bodega
        self.region = region
        self.uva = uva
        self.precio = precio
        self.prices_old = prices_old
        self.likes = likes
        self.valoracion = valoracion
        self.opinion = opinion
        self.vinificacion = vinificacion
