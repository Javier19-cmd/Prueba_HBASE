import time
import os
import json
import ast
from datetime import datetime
import file as fl
import copy
from prettytable import PrettyTable

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

        fl.crear_archivo("./tables/" + nombre, nombre)

        fl.escribir_txt(nombre)
    
    #print("Nombre antes de ser retornado: ", nombre)
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

def listar(): # Método para listar las tablas de la metadata.

    # Abriendo el archivo de metadata.
    with open("metadata.txt", "r") as f:
        diccionario = json.load(f)
        
        for tabla in diccionario.keys():
            print(tabla)

# Función para eliminar una tabla de HBase.
def eliminar_tabla(nombre):
    global archivos_txt

    # print("Archivos: ", archivos_txt)

    # print("Nombre: ", nombre in archivos_txt)

    # Verificando si la tabla existe en el diccionario.
    if nombre in archivos_txt:
        # Eliminando la tabla también de la lista.
        #archivos_txt.remove(nombre)

        # Eliminando la tabla del archivo metadata.
        with open("metadata.txt", "r") as f:
            diccionario = json.load(f)

        # Verificando que el enable de la tabla en false.
        if is_enabled(nombre):
            print("La tabla no está deshabilitada.")

        else: 
            
            del diccionario[nombre]

            # Eliminando de la lista de archivos el nombre del archivo.
            if nombre in archivos_txt:
                
                archivos_txt.remove(nombre)

                fl.eliminar_archivo(nombre)
            
            return

        with open("metadata.txt", "w") as f:
            f.write(json.dumps(diccionario))
            

    else:
        print(f"La tabla {nombre} no existe.")

# Función para elimintar todas las tablas de la base de datos.
def eliminar_todas_tablas():

    global archivos_txt

    for tabla in archivos_txt:
        eliminar_tabla(tabla)

        if len(archivos_txt) > 0:
            eliminar_todas_tablas()

    print("Archivos: ", archivos_txt)

# Método para describir las tablas que se tienen.
def describe(tabla):
    print("Tabla: ", tabla)

    # Abriendo el metadata.txt.
    with open("metadata.txt", "r") as f:
        diccionario = json.load(f)

        #print("Diccionario: ", diccionario)

        if tabla in diccionario:
            #print("Column families: ", diccionario[tabla]["families"])

            lista = diccionario[tabla]["families"]

            for i in lista:
                print("Familia: ", i)
            
            print(len(lista), " row(s)")
        
        else:
            print(f"La tabla {tabla} no existe.")

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
        
def disable(tabla):
    if tabla in archivos_txt:
        with open("metadata.txt", "r") as f:
            diccionario = json.load(f)
        
        diccionario[tabla]["enabled"] = False
        
        with open("metadata.txt", 'w') as f:
            json.dump(diccionario, f)
        
    else:
        print(f"La tabla {tabla} no existe.")
    
def enable(tabla):
    if tabla in archivos_txt:
        with open("metadata.txt", "r") as f:
            diccionario = json.load(f)
        
        diccionario[tabla]["enabled"] = True
        
        with open("metadata.txt", 'w') as f:
            json.dump(diccionario, f)
        
    else:
        print(f"La tabla {tabla} no existe.")
        
def is_enabled(tabla):
    if tabla in archivos_txt:
        with open("metadata.txt", "r") as f:
            diccionario = json.load(f)
        
        return diccionario[tabla]["enabled"]
        
    else:
        print(f"La tabla {tabla} no existe.")

def get(tabla, fila):
    if tabla in archivos_txt:
        with open("./tables/" + tabla + ".txt", "r") as f:
            diccionario = json.load(f)
        
        print(diccionario[fila])
        
    else:
        print(f"La tabla {tabla} no existe.")
        
def add_column_family(tabla, cf):
    if tabla in archivos_txt:
        with open("metadata.txt", "r") as f:
            diccionario = json.load(f)
        
        familias = diccionario[tabla]["families"]
        familias.append(cf)
        diccionario[tabla]["families"] = list(set(familias))
        
        with open("metadata.txt", 'w') as f:
            json.dump(diccionario, f)
        
    else:
        print(f"La tabla {tabla} no existe.")
        
def delete_column_family(tabla, cf):
    if tabla in archivos_txt:
        with open("metadata.txt", "r") as f:
            diccionario = json.load(f)

        # Verificando que el enable de la tabla en false.
        if is_enabled(tabla):
            familias = diccionario[tabla]["families"]
            familias.remove(cf)
            diccionario[tabla]["families"] = familias
            
            with open("metadata.txt", 'w') as f:
                json.dump(diccionario, f)
                
            with open("./tables/" + tabla + ".txt", "r") as f:
                diccionario = json.load(f)
            
            for key, value in diccionario.items():
                if cf in value:
                    del diccionario[key][cf]
            
            with open("./tables/" + tabla + ".txt", "w") as f:
                diccionario = json.dump(diccionario, f)

def truncate(tabla):
    if tabla in archivos_txt:
        # with open("./tables/" + tabla + ".txt", "w") as f:
        #     f.write("{}")
        
        # print("Tabla truncada.")


        # Abriendo el archivo de metadata para guardar localemente 
        # los column families.
        with open("metadata.txt", "r") as f:
            diccionario = json.load(f)

        # Obteniendo los column families de la tabla.
        column_families = diccionario[tabla]["families"]

        #print("Column families: ", column_families)

        # Deshabilitando la tabla.
        print("Deshabilitando la tabla")
        disable(tabla)

        # Eliminando la tabla.
        print("Eliminando la tabla")
        eliminar_tabla(tabla)

        # Creando la tabla de nuevo.
        print("Creando la tabla de nuevo")
        crear_tabla(tabla, column_families)

    else:
        print(f"La tabla {tabla} no existe.")

def eliminar_fila(diccionario, row):
    if row not in diccionario:
        print("No existe esta fila, row_key inválido.")
        return diccionario
    del diccionario[row]
    return diccionario

def eliminar_todo(tabla, id):
    # nombre_tabla, row_key, cf, column, value
    global archivos_txt

    #print(archivos_txt)

    # Verificando si la tabla existe en el diccionario.
    if tabla in archivos_txt:
        # Agregando la celda a la tabla.
        diccionario = {}

        with open("./tables/" + tabla + ".txt", "r") as f:
            diccionario = json.load(f)
            
            # Eliminando la celda a la tabla.
            diccionario = eliminar_fila(diccionario, id)
                
        with open("./tables/" + tabla + ".txt", 'w') as f:
            json.dump(diccionario, f)
        print("Fila eliminada")

    else:
        print(f"La tabla {tabla} no existe.")

def contar(tabla):
    if tabla in archivos_txt:
        diccionario = {}

        with open("./tables/" + tabla + ".txt", "r") as f:
            diccionario = json.load(f)
            
            # Eliminando la celda a la tabla.
            return len(diccionario)
    else:
        print(f"La tabla {tabla} no existe.")

def scan(tabla):
    if tabla in archivos_txt:
        diccionario = {}
        print_table = PrettyTable()
        print_table.field_names = ["ROW", "COLUMN+CELL"]

        with open("./tables/" + tabla + ".txt", "r") as f:
            diccionario = json.load(f)
            for id, dicc in diccionario.items():
                for familia, dicc2 in dicc.items():
                    for propiedad, dicc3 in dicc2.items():
                        print(propiedad)
                        timestamp = dicc3["timestamp"]
                        value = dicc3["value"]
                        print_table.add_row([id, f"column={familia}:{propiedad}, timestamp={timestamp}, value={value}"])

            #column=Personal info:Name, timestamp=1504600767520, value=Alex  
        print(print_table)
    else:
        print(f"La tabla {tabla} no existe.")       


def delete(tabla, fila, colf):
    # nombre_tabla, row_key, cf, column, value
    global archivos_txt

    #print(archivos_txt)

    # Verificando si la tabla existe en el diccionario.
    if tabla in archivos_txt:
        # Agregando la celda a la tabla.
        
        s = colf.split()

        diccionario = {}

        with open("./tables/" + tabla + ".txt", "r") as f:
            diccionario = json.load(f)
            diccionario_copy = copy.deepcopy(diccionario)
            eliminar = True
            for i in s:
                colfs = i.split(":")

                # Agregando la celda a la tabla.
                if fila not in diccionario_copy:
                    print("Fila inválida")
                    eliminar = False
                    break
                
                if colfs[0] not in diccionario_copy[fila]:
                    print("Familia inválida")
                    eliminar = False
                    break
                
                if colfs[1] not in diccionario_copy[fila][colfs[0]]:
                    print("Propiedad inválida")
                    eliminar = False
                    break
                
                del diccionario_copy[fila][colfs[0]][colfs[1]]
                
        if eliminar == True:
            diccionario = diccionario_copy
            print("Propiedad eliminada")

        with open("./tables/" + tabla + ".txt", 'w') as f:
            json.dump(diccionario, f)

    else:
        print(f"La tabla {tabla} no existe.")
