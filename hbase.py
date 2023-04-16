import file as fl
from metodos import *
import json
import os

# Hacer un main con opciones.
def main():

    # Haciendo una carga por si se creó algún archivo anteriormente.
    ruta_carpeta = os.getcwd()
    archivos_txt = [archivo for archivo in os.listdir(ruta_carpeta) if archivo.endswith('.txt')]
    #print("Archivos: ", archivos_txt)
    cargar_archivos()
    ver_tablas()
    fl.cargar_archivos()

    print("Bienvenid@ al simulador de HBase \n")

    while True:
        #opciones = int(input("Ingrese una opción: "))
        comando = input()
        palabras = comando.split()

        if palabras[0] == "describe": # Imprimir las colum families.
            describe()
        
        elif palabras[0] == "create": # Crear una tabla.
            coma, nombre, tabla = comando.split(maxsplit=2)
            # Se usará tabla y resto.

            diccionario = json.loads(tabla)

            column_families = []

            for key, value in diccionario.items():
                for k in value.keys():
                    if isinstance(value[k], dict) and k not in column_families:
                        column_families.append(k)
            
            print(column_families)

            nombre, tabla = crear_tabla(nombre, column_families, diccionario)

            # print("Nombre: ", nombre)
            # print("Tabla: ", tabla)

            # Creando el archivo.
            archivo = fl.crear_archivo(nombre)

            # Escribiendo en el archivo.
            files = fl.escribir_archivo(archivo, tabla)

            # print("Archivo: ", archivo)
            # print("Contenido: ", files)

            print("Archivo creado")

            # Guardando el archivo.
            fl.escribir_txt(archivo, files)
        
        elif palabras[0] == "drop": # Comando para eliminar una tabla.
            coma, nombre = comando.split(maxsplit=1)
            
            print("Eliminando tabla")

            eliminar_tabla(nombre) # Eliminando la tabla.

            fl.eliminar_archivo(nombre) # Eliminando archivo.
        
        elif palabras[0] == "drop_all":

            print("Eliminando todas las tablas")
            
            # Eliminando las tablas.
            eliminar_todas_tablas()

            # Eliminando los archivos.
            fl.eliminar_archivos()
        
        elif palabras[0] == "quit": # Cerrar la simulación.

            print("Saliendo del simulador")
            break


        # if opciones == 1:
        #     nombre_tabla = input("Ingrese el nombre de la tabla: ")

        #     numcf = int(input("Ingrese la cantidad de column families que quiere tener en la tabla: "))

        #     column_families = crear_column_families(numcf) # Creando los column families.
            
        #     datosT = input("Ingrese los datos que se quieren meter a la tabla: ")

        #     datos = json.loads(datosT)

        #     nombre, tabla = crear_tabla(nombre_tabla, column_families, datos)

        #     print("Nombre: ", nombre)
        #     print("Tabla: ", tabla)

        #     # Creando el archivo.
        #     archivo = fl.crear_archivo(nombre)

        #     # Escribiendo en el archivo.
        #     files = fl.escribir_archivo(archivo, tabla)

        #     print("Archivo: ", archivo)
        #     print("Contenido: ", files)

        #     # Guardando el archivo.
        #     fl.escribir_txt(archivo, files)

        # # Listar las filas de una tabla.
        # elif opciones == 2:
        #     nombre_tabla = input("Ingrese el nombre de la tabla: ")

        #     # Listando las filas de la tabla en los métodos.
        #     filas = listar_filas(nombre_tabla)

        #     print("Filas: ", filas)
        
        # # Eliminar una tabla en la lista de tablas.
        # elif opciones == 3: 
        #     nombre_tabla = input("Ingrese el nombre de la tabla: ")

        #     # Eliminando la tabla.
        #     eliminar_tabla(nombre_tabla)

        #     # Eliminando el archivo también.
        #     fl.eliminar_archivo(nombre_tabla)
        
        # # Eliminar todas las tablas de HBase.
        # elif opciones == 4: 
            
        #     print("Eliminando todas las tablas de la base de datos")

        #     # Eliminando todas las tablas.
        #     eliminar_todas_tablas()

        #     # Eliminando todos los archivos.
        #     fl.eliminar_archivos()

        # # Describir todas las tablas de HBase.
        # elif opciones == 5: 
        #     describe()
            
main()