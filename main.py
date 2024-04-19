import Usuarios
from Usuarios import *


def main():
    self.conexion = Conexion(
        host="127.0.0.1",
        user="root",
        password="1234",
        database="proyecto1"
    )
    cursor = mi_conexion.cursor()


while True:

    print("\nMenú principal:")
    print("1. Registrarme")
    print("2. Iniciar sesión")
    print("3. Salir del programa")
    print("Correo atención al cliente: vinoteca.atencion.alcliente@gmail.com")
    opcion = input("Seleccione una opción: ")
    if opcion == "1":
        id_usuario = input("Ingrese un nombre de usuario: ")
        correo = input("Ingrese un correo electrónico: ")
        contraseña = input("Ingrese una contraseña: ")
        perfil = input("Ingrese su perfil (proveedor, comprador o visitante): ")
        fecha_nacimiento = input("Ingrese su fecha de nacimiento (YYYY-MM-DD): ")
        resultado = Usuario.registrar(id_usuario, correo, contraseña, perfil, fecha_nacimiento)
    elif opcion == "2":
        usuario = input("Ingrese si es visitante ,comprador,administrador o proveedor")
        if usuario == "visitante":
            correo_v = input("Ingrese el correo de visitante")
            contraseña_v = input("Ingrese su contraseña")
            if correo1 == correo_v and contraseña_v == contraseña:
                print("\nMenú principal:")
                print("1. mostrar vinos ")
                print("2. mostrar vinos mas baratos")
                print("3. mostrar advertencia")
                print("4. regresar al menu anterior")
                print("Correo atención al cliente: vinoteca.atencion.alcliente@gmail.com")
                opcion = input("Seleccione una opción: ")
                while True:
                    if opcion == "1":
                        print(visitante.mostrar_vinos(self))
                    elif opcion == "2":
                        print(visitante.mostrar_vinos_mas_baratos(self))
                    elif opcion == "3":
                        print(visitante.mostrar_advertencia(self))
                    elif opcion == "4":
                        break
            else:
                print("correo  o contaseña incorrecta")
        elif usuario == "comprador":
            correo_c = input("Ingrese el correo de comprador")
            contraseña_c = input("Ingrese su contraseña")
            if correo_c == correo and contraseña_c == contraseña:
                print("\nMenú principal:")
                print("1. mostrar vinos mas baratos")
                print("2. comprar vinos")
                print("3. dejar una reseña")
                print("4. regresar al menu anterior")
                print("Correo atención al cliente: vinoteca.atencion.alcliente@gmail.com")
                opcion = input("Seleccione una opción: ")
            while True:
                if opcion == "1":
                    print(comprador.mostrar_vinos(self))
                elif opcion == "2":
                    print(comprador.mostrar_vinos_mas_baratos(self))
                elif opcion == "3":
                    nombre = input("Ingrese el nombre del vino")
                    print(comprador.comprar_vinos(self, nombre))
                    print("vino comprado")
                elif opcion == "4":
                    comprador_id = input("Su usuario: ")
                    nombre = input("Ingrese el nombre del producto al que desea dejar una reseña: ")
                    valoracion = input("Ingrese una calificación (del 1 al 5): ")
                    likes = input("si o no")
                    opinion = input("Deje un comentario sobre el producto: ")
                    dejar_reseña_comprador = comprador.dejar_reseña(nombre, valoracion, likes, opinion, comprador_id)
                    print("reseña puesta:" + dejar_reseña_comprador)
                elif opcion == "5":
                    break
        elif usuario == "administrador":
            correo_a = input("Ingrese el correo de administrador")
            contraseña_a = input("Ingrese su contraseña")
            if correo_a == correo and contraseña_a == contraseña:
                print("\nMenú principal:")
                print("1. elimar usuario")
                print("2. regresar al menu anterior")
                opcion = input("Seleccione una opción: ")
            while True:
                if opcion == "1":
                    nombre_usuario = input("Ingrese el nombre del vino")
                    eliminar_usuario_admministrador = administrador.eliminar_usuario(nombre_usuario)
                    print(eliminar_usuario_admministrador + "eliminado")
                elif opcion == "2":
                    break
        elif usuario == "proveedor":
            correo_p = input("Ingrese el correo de administrador")
            contraseña_p = input("Ingrese su contraseña")
            if correo_p == correo and contraseña_p == contraseña:
                print("\nMenú de visitante:")
                print("1. mostrar vinos")
                print("2. agregar vino")
                print("3. eliminar vino")
                print("4. ver reseñas de los compradores")
                print("5. Salir del programa")
            while True:
                opcion = input("Seleccione una opción: ")
                if opcion == "1":
                    nombre = input("Ingrese el nombre del vino: ")
                    mostrar_vinos_proveedor1 = proveedor.mostrar_vinos_proveedor(nombre)
                    print(mostrar_vinos_proveedor1)
                elif opcion == "2":
                    nombre = input("Ingrese el nombre del vino: ")
                    bodega = input("Ingrese la bodega vino: ")
                    region = input("Ingrese la region dek vino")
                    uva = input("Ingrese el tipo de uva")
                    precio = input("Ingrese el precio del vino: ")
                    agregar_vino1 = agregar_vino1(nombre, bodega, region, uva, precio)
                    agregar_vino = agregar_vino1.agregar_vino()
                    print(agregar_vino + "vino agregado correctamente")
                elif opcion == "3":
                    nombre = input("Ingrese el nombre del vino: ")
                    bodega = input("Ingrese la bodega vino: ")
                    region = input("Ingrese la region dek vino")
                    uva = input("Ingrese el tipo de uva")
                    cantidad = input("Ingrese la cantidad disponible del vino: ")
                    eliminar_vino1 = proveedor.eliminar_vino(nombre, bodega, region, uva, cantidad)
                    print(eliminar_vino1 + "eliminado correctamente")
                elif opcion == "4":
                    id_usuario = input("ingrese el nombre ")
                    valoracion = input("ingrese la valoracion")
                    likes = input("ingrese el like")
                    opinion = input("ingrese la opinion")
                    ver_reseñas_compradores1 = proveedor.ver_reseñas_compradores(id_usuario, valoracion, likes, opinion)
                    print(ver_reseñas_compradores)
                elif opcion == "5":
                    break
        elif opcion == "3":
            break
if __name__ == "__main__":
    main()



