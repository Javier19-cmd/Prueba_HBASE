import file as fl
from metodos import *

def limpiar(string):
    string = string.replace("'", "")
    string = string.replace(" ", "")
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
            comando = ''.join(palabras[1:])
            nombre = comando

            nombre = limpiar(nombre)

            describe(nombre)
        
        elif palabras[0] == "create": # Crear una tabla.
            comando = ''.join(palabras[1:])
            nombre, column_fam = comando.split(maxsplit=1)

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
            comando = ''.join(palabras[1:])
            nombre = comando

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
            comando = ''.join(palabras[1:])
            nombre_tabla, row_id, colfprop = comando.split(maxsplit=2)

            # Quitando la coma del nombre.
            nombre_tabla = limpiar(nombre_tabla)
            row_id = limpiar(row_id)
            colfprop = limpiar(colfprop)

            # Qui

            put(nombre_tabla, row_id, colfprop)

            print("Dato ingresado")
            
        elif palabras[0] == "disable":
            
            comando = ''.join(palabras[1:])
            nombre_tabla = comando
            
            nombre_tabla = limpiar(nombre_tabla)
            
            disable(nombre_tabla)
        
        
        elif palabras[0] == "enable":
            
            comando = ''.join(palabras[1:])
            nombre_tabla = comando
            
            nombre_tabla = limpiar(nombre_tabla)
            
            enable(nombre_tabla)

        
        elif palabras[0] == "is_enabled":
            
            comando = ''.join(palabras[1:])
            nombre_tabla = comando
            
            nombre_tabla = limpiar(nombre_tabla)
            
            print(is_enabled(nombre_tabla))
    
        
        elif palabras[0] == "get":
            
            comando = ''.join(palabras[1:])
            nombre_tabla, row_id = comando.split(",", maxsplit=1)
            
            nombre_tabla = limpiar(nombre_tabla)
            row_id = limpiar(row_id)
            
            get(nombre_tabla, row_id)  


        elif palabras[0] == "truncate":
            comando = ''.join(palabras[1:])
            coma, nombre_tabla = comando
            
            nombre_tabla = limpiar(nombre_tabla)
            
            truncate(nombre_tabla)
    
        elif palabras[0] == "deleteall":
            comando = ''.join(palabras[1:])
            nombre_tabla, row_id = comando.split(maxsplit=1)

            # Quitando la coma del nombre.
            nombre_tabla = limpiar(nombre_tabla)
            row_id = limpiar(row_id)

            eliminar_todo(nombre_tabla, row_id)
        
        elif palabras[0] == "delete":
            comando = ''.join(palabras[1:])
            nombre_tabla, row_id, colfprop = comando.split(maxsplit=2)

            # Quitando la coma del nombre.
            nombre_tabla = limpiar(nombre_tabla)
            row_id = limpiar(row_id)
            colfprop = limpiar(colfprop)

            # Qui

            delete(nombre_tabla, row_id, colfprop)
        
        elif palabras[0] == "alter":
            
            comando = ''.join(palabras[1:])
            nombre_tabla, params = comando.split(",", maxsplit=1)
            
            nombre_tabla = limpiar(nombre_tabla)
            params = limpiar(params.replace("{", "").replace("}", ""))
            
            params = params.split(",")
            
            
            if params[0].startswith("NAME"):
                nombre_cf = params[0].split("=>")[1]
                
                if len(params) > 1:
                    if params[1].startswith("METHOD") and params[1].endswith("delete"):
                        delete_column_family(nombre_tabla, nombre_cf)
                    else:
                        print("Comando incorrecto")
                else:
                    add_column_family(nombre_tabla, nombre_cf)
            else:
                print("Comando incorrecto")
            
        elif palabras[0] == "count":
            comando = ''.join(palabras[1:])
            nombre_tabla = comando
            
            nombre_tabla = limpiar(nombre_tabla)
            
            print(f"Total de filas: {contar(nombre_tabla)}")

        elif palabras[0] == "scan":
            comando = ''.join(palabras[1:])
            nombre_tabla = comando
            
            nombre_tabla = limpiar(nombre_tabla)
            
            scan(nombre_tabla)

        elif palabras[0] == "quit": # Cerrar la simulación.

            print("Saliendo del simulador")
            break
            
main()