import file as fl
from metodos import *


def limpiar(string):
    string = string.replace("'", "")
    string = string.replace(",", "")
    return string

# Hacer un main con opciones.
def main():

    ver_tablas()

    print("Bienvenid@ al simulador de HBase \n")

    while True:
        #opciones = int(input("Ingrese una opción: "))
        comando = input()
        palabras = comando.split()

        if palabras[0] == "describe": # Imprimir las colum families.

            coma, nombre = comando.split(maxsplit=1)

            nombre = limpiar(nombre)

            describe(nombre)
        
        elif palabras[0] == "create": # Crear una tabla.
            coma, nombre, column_fam = comando.split(maxsplit=2)

            # Se usará tabla y resto.
            nombre = limpiar(nombre)
            column_fam = column_fam.replace("'", "")

            # Guardando las cf en una lista.
            column_families = column_fam.split(",")
            # Quitando espacios.
            column_families = [cf.strip() for cf in column_families]

            lista = []

            for cf in column_families:
                lista.append(cf)

            nombre = crear_tabla(nombre, column_families)
        
        elif palabras[0] == "drop": # Comando para eliminar una tabla.

            # Tiene que estar deshabilitada.

            coma, nombre = comando.split(maxsplit=1)

            nombre = limpiar(nombre)
            
            print("Eliminando tabla")

            eliminar_tabla(nombre) # Eliminando la tabla.
        
        elif palabras[0] == "drop_all":

            # Siempre siguiendo lo que están deshabilitados.

            print("Eliminando todas las tablas")
            
            # Eliminando las tablas.
            eliminar_todas_tablas()
        
        elif palabras[0] == "list":

            listar()

        elif palabras[0] == "put":

            # put 'tabla', 'id', 'familia:propiedad_llave', 'valor'

            coma, nombre_tabla, row_id, colfprop = comando.split(maxsplit=3)

            # Quitando la coma del nombre.
            nombre_tabla = limpiar(nombre_tabla)
            row_id = limpiar(row_id)
            colfprop = limpiar(colfprop)

            # Qui

            put(nombre_tabla, row_id, colfprop)

            print("Dato ingresado")
            
        elif palabras[0] == "disable":
            
            coma, nombre_tabla = comando.split(maxsplit=1)
            
            nombre_tabla = limpiar(nombre_tabla)
            
            disable(nombre_tabla)
        
        
        elif palabras[0] == "enable":
            
            coma, nombre_tabla = comando.split(maxsplit=1)
            
            nombre_tabla = limpiar(nombre_tabla)
            
            enable(nombre_tabla)

        
        elif palabras[0] == "is_enabled":
            
            coma, nombre_tabla = comando.split(maxsplit=1)
            
            nombre_tabla = limpiar(nombre_tabla)
            
            is_enabled(nombre_tabla)    

        elif palabras[0] == "truncate":
            coma, nombre_tabla = comando.split(maxsplit=1)
            
            nombre_tabla = limpiar(nombre_tabla)
            
            truncate(nombre_tabla)
    
        elif palabras[0] == "deleteall":
            coma, nombre_tabla, row_id = comando.split(maxsplit=2)

            # Quitando la coma del nombre.
            nombre_tabla = limpiar(nombre_tabla)
            row_id = limpiar(row_id)

            delete_all(nombre_tabla, row_id)

        elif palabras[0] == "quit": # Cerrar la simulación.

            print("Saliendo del simulador")
            break
            
main()