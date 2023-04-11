import file as fl
from metodos import *
import json

# Hacer un main con opciones.
def main():

    print("Bienvenid@ al simulador de HBase \n")

    print("Las opciones son: \n")
    print("1. Crear una tabla de HBase \n")
    print("2. Listar las filas de una tabla de HBase \n")


    opciones = 0
    while True:
        opciones = int(input("Ingrese una opción: "))

        if opciones == 1:
            nombre_tabla = input("Ingrese el nombre de la tabla: ")

            numcf = int(input("Ingrese la cantidad de column families que quiere tener en la tabla: "))

            column_families = crear_column_families(numcf) # Creando los column families.
            
            datosT = input("Ingrese los datos que se quieren meter a la tabla: ")

            datos = json.loads(datosT)

            nombre, tabla = crear_tabla(nombre_tabla, column_families, datos)

            print("Nombre: ", nombre)
            print("Tabla: ", tabla)

            # Creando el archivo.
            archivo = fl.crear_archivo(nombre)

            # Escribiendo en el archivo.
            files = fl.escribir_archivo(archivo, tabla)

            print("Archivo: ", archivo)
            print("Contenido: ", files)

            # Guardando el archivo.
            fl.escribir_txt(archivo, files)

        # Listar las filas de una tabla.
        elif opciones == 2:
            nombre_tabla = input("Ingrese el nombre de la tabla: ")

            # Listando las filas de la tabla en los métodos.
            filas = listar_filas(nombre_tabla)

            print("Filas: ", filas)
            
main()