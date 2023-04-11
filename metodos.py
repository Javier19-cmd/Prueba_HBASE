import uuid
import time
import os
import ast

# Diccionario para almacenar las tablas
tablas = {}

# Diccionario que va a tener las column families de cada tabla.
column_familys = {}

# Guardando los nombres de los archivos anteriormente creados.
archivos_txt = []

ruta = os.getcwd()

archivos_txt = [archivo for archivo in os.listdir(ruta) if archivo.endswith('.txt')]

for i, nombre_archivo in enumerate(archivos_txt):
    if nombre_archivo.endswith('.txt'):
        archivos_txt[i] = nombre_archivo[:-4]  # elimina los últimos 4 caracteres (.txt)

# Método para cargar el contenido de los archivos ya creados en alguna simulación anterior.
def cargar_archivos():
    global tablas # Variable para cargar las tablas en un diccionario.

    for archivo in archivos_txt:
        with open(archivo + ".txt", "r") as f:
            contenido = f.read()
            #tablas = ast.literal_eval(contenido)

            # # Quitarle al string del archivo el .txt.
            # arch = archivo.split(".")[0]

            # Cargando primero el nombre de cada archivo en la tabla.
            tablas[archivo] = ast.literal_eval(contenido)

    dict = {}

    column_families = []

    for table_name in tablas:
        for column_family in tablas[table_name]:
            if column_family != 'timestamp':
                if column_family not in column_families:
                    column_families.append(column_family)

    column_familys[table_name] = column_families

    print(column_familys)

def ver_tablas():
    print(tablas)        


# Función para crear una tabla
def crear_tabla(nombre, column_families, datos):
    if nombre in tablas:
        print("La tabla ya existe.")
    else:
        tablas[nombre] = {}
        archivos_txt.append(nombre)

        # Guardando cada tabla con su column families en un diccionario aparte.
        #column_family[nombre] = column_families

        # Agregar column families a la tabla
        for cf in column_families:
            tablas[nombre][cf] = {}

        # Agregar los datos a la tabla
        for row_key, cf_data in datos.items():
            for cf_name, cf_values in cf_data.items():
                for column, value in cf_values.items():
                    agregar_celda(nombre, row_key, cf_name, column, value)

        # Generar un row key único y obtener el timestamp actual en milisegundos
        row_key = str(uuid.uuid4())
        timestamp = int(round(time.time() * 1000))

        # Agregar el row key y el timestamp a la tabla
        tablas[nombre]["timestamp"] = {row_key: timestamp}

        print(f"Tabla {nombre} creada exitosamente.")

    # Retornar el nombre de la tabla y la tabla
    return nombre, {cf_name: cf_data for cf_name, cf_data in tablas[nombre].items() if cf_data}


# Función para agregar una celda a una tabla
def agregar_celda(nombre_tabla, row_key, cf, column, value):
    # Verificar si la tabla existe
    if nombre_tabla not in tablas:
        print(f"La tabla {nombre_tabla} no existe.")
        return

    # Verificar si el row key existe en la tabla
    if row_key not in tablas[nombre_tabla]:
        # Si el row key no existe, agregarlo a la tabla
        tablas[nombre_tabla][row_key] = {}

    # Verificar si la columna familiar existe en la tabla
    if cf not in tablas[nombre_tabla]:
        print(f"La columna familiar {cf} no existe en la tabla {nombre_tabla}.")
        return

    # Generar un timestamp para la celda
    timestamp = int(round(time.time() * 1000))

    # Agregar la celda a la tabla con su respectivo timestamp
    tablas[nombre_tabla][cf][(column, row_key)] = (value, timestamp)

    #print(f"Celda ({column}, {row_key}, {value}, {timestamp}) agregada a la columna familiar {cf} de la tabla {nombre_tabla}.")

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

# Método para listar las filas de una tabla.
def listar_filas(nombre_tabla):
    # Verificar si la tabla existe
    if nombre_tabla not in tablas:
        print(f"La tabla {nombre_tabla} no existe.")
        return []

    # Crear una lista para almacenar las filas encontradas
    filas = []

    # Recorrer todas las filas de la tabla
    for row_key in tablas[nombre_tabla]:
        # Verificar que la fila no sea la fila de timestamp
        if row_key != "timestamp":
            # Verificar si la fila no es una column family
            if not any(row_key.startswith(cf + ":") for cf in tablas[nombre_tabla].keys()):
                # Agregar la fila a la lista
                filas.append(row_key)
        
    # Quitando de la lista todo lo que empiece con cf.
    filas = [elem for elem in filas if not elem.startswith('cf')]
    # Retornar la lista de filas
    return filas

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