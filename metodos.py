import uuid
import time
import os
import json
import ast
from datetime import datetime

# Diccionario que va a tener las column families de cada tabla.
column_familys = {}

# Guardando los nombres de los archivos anteriormente creados.
archivos_txt = []

root = os.path.dirname(os.path.relpath(__file__))
ruta = os.path.join(root, 'tables')

archivos_txt = [archivo for archivo in os.listdir(ruta) if archivo.endswith('.txt')]

for i, nombre_archivo in enumerate(archivos_txt):
    if nombre_archivo.endswith('.txt'):
        archivos_txt[i] = nombre_archivo[:-4]  # elimina los últimos 4 caracteres (.txt)

def cargar_archivos():
    global tablas, column_familys # Variable para cargar las tablas en un diccionario.

    for archivo in archivos_txt:

        with open(archivo + ".txt", "r") as f:
            contenido = f.read()
            #tablas = ast.literal_eval(contenido)

            # # Quitarle al string del archivo el .txt.
            # arch = archivo.split(".")[0]

            # Cargando primero el nombre de cada archivo en la tabla.
            tablas[archivo] = ast.literal_eval(contenido)

    for table_name in tablas:
        column_familys[table_name] = []
        for column_family in tablas[table_name]:
            if column_family != 'timestamp':
                if column_family not in column_familys[table_name]:
                    column_familys[table_name].append(column_family)

    #print(column_familys)


def ver_tablas():
    print(archivos_txt)        


# Función para crear una tabla
def crear_tabla(nombre, column_families):
    if nombre in archivos_txt:
        print("La tabla ya existe.")
    else:
        archivos_txt.append(nombre)
    
        timestamp = int(round(time.time() * 1000))
        enable = True
        diccionario = {}

        with open("metadata.txt", "r") as f: 
            # Guardando lo que hay en el archivo de metadata en el diccionario.
            contenido = f.read()

        diccionario = json.loads(contenido)
        print(diccionario)

        # Agregando el nombre de la tabla, el timestamp y el enabled a un diccionario.
        diccionario[nombre] = {"timestamp": timestamp, "enabled": enable, "families": column_families}

        # Guardando esta data en el metadata.
        with open("metadata.txt", "w") as f:
            f.write(json.dumps(diccionario))
        
    # Retornar el nombre y la tabla entera.
    return nombre

# Función para agregar una celda a una tabla
def agregar_celda(diccionario, row_key, cf, column, value):
    # Verificar si la tabla existe
    
    fecha_hora_actual = datetime.now()

    if row_key not in diccionario:
        diccionario[row_key] = {}
    
    if cf not in diccionario[row_key]:
        diccionario[row_key][cf] = {}
    
    if column not in diccionario[row_key][cf]:
        diccionario[row_key][cf][column] = {}
    
    diccionario[row_key][cf][column]["value"] = value
    diccionario[row_key][cf][column]["timestamp"] = str(fecha_hora_actual)

    return diccionario

# Función para crear column families
def crear_column_families(num_cfs):
    cfs = ["cf" + str(i+1) for i in range(num_cfs)]
    return cfs

# Función para obtener las celdas agregadas a una columna familiar
def obtener_celdas_columna(nombre_tabla, cf):
    # Verificar si la tabla existe
    if nombre_tabla not in tablas:
        print(f"La tabla {nombre_tabla} no existe.")
        return

    # Verificar si la columna familiar existe en la tabla
    if cf not in tablas[nombre_tabla]:
        print(f"La columna familiar {cf} no existe en la tabla {nombre_tabla}.")
        return

    # Retornar las celdas agregadas a la columna familiar
    return tablas[nombre_tabla][cf]

# def listar_filas(nombre_tabla):
#     # Verificar si la tabla existe
#     if nombre_tabla not in tablas:
#         print(f"La tabla {nombre_tabla} no existe.")
#         return []

#     # Crear una lista para almacenar las filas encontradas
#     filas = []

#     # Recorrer todas las filas de la tabla
#     for row_key in tablas[nombre_tabla]:
#         # Verificar que la fila no sea la fila de timestamp
#         if row_key != "timestamp":
#             # Verificar si la fila tiene celdas
#             tiene_celdas = False
#             for cf_name, cf_data in tablas[nombre_tabla][row_key].items():
#                 if cf_data:
#                     tiene_celdas = True
#                     break
            
#             # Si la fila tiene celdas, agregarla a la lista
#             if tiene_celdas:
#                 filas.append(row_key)

#     # Retornar la lista de filas
#     return filas

def listar():

    global tablas

    # Lista para almacenar los nombres de las tablas.
    nombre_tablas = []

    # Recorrer el diccionario de tablas.
    for tabla in tablas:
        nombre_tablas.append(tabla)

    return nombre_tablas

# Función para eliminar una tabla de HBase.
def eliminar_tabla(nombre):

    # Verificando si la tabla existe en el diccionario.
    if nombre in tablas:
        # Eliminando la tabla del diccionario.
        del tablas[nombre]
        print(f"Tabla {nombre} eliminada exitosamente.")

        # Eliminando la tabla también de la lista.
        archivos_txt.remove(nombre)

    else:
        print(f"La tabla {nombre} no existe.")

# Función para elimintar todas las tablas de la base de datos.
def eliminar_todas_tablas():

    print("Archivos: ", type(archivos_txt))

    # Quitarle la extensión .txt a los nombres en archivos_txt, si algún 
    # string lo tiene.
    

    # Recorrer todas las tablas en la base de datos
    for tabla in list(tablas.keys()):
        # Eliminar todas las filas de la tabla
        del tablas[tabla]

        # Si el nombre no tiene .txt, agregárselo.
        if not tabla.endswith(".txt"):
            tabla += ".txt"

        #print("Tabla: ", tabla)

        # Si en caso el nombre tiene extensión, se le quita y se elimina de la lista.
        if tabla.endswith(".txt"):
            nombre_sin_extension = tabla.split(".")[0]

            if nombre_sin_extension in archivos_txt:
                #del tablas[nombre_sin_extension]
                archivos_txt.remove(nombre_sin_extension)
        else: 
            
            del tablas[tabla]

            archivos_txt.remove(tabla)
    
    # Eliminar todas las tablas de la base de datos
    tablas.clear()

    print("Todas las tablas han sido eliminadas.")
    print("Tablas: ", tablas)

# Método para describir las tablas que se tienen.
def describe():

    print("Column family: ", column_familys)

    for table in column_familys:
        print("Tabla:", table)
        print("Column Families:")
        for cf in column_familys[table]:
            print("\t", cf)

def put(tabla, fila, colf):
    # nombre_tabla, row_key, cf, column, value
    global archivos_txt

    #print(archivos_txt)

    # Verificando si la tabla existe en el diccionario.
    if tabla in archivos_txt:
        # Agregando la celda a la tabla.
        
        s = colf.split()

        diccionario = {}
        respuesta = None

        with open("./tables/" + tabla + ".txt", "r") as f:
            diccionario = json.load(f)
            for i in range(0, len(s), 2):
                colfs = s[i].split(":")
                valor = s[i+1]

                # Agregando la celda a la tabla.
                respuesta = agregar_celda(diccionario, fila, colfs[0], colfs[1], valor)
                
        with open("./tables/" + tabla + ".txt", 'w') as f:
            json.dump(respuesta, f)

    else:
        print(f"La tabla {tabla} no existe.")