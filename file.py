import os
import ast

# Creando un diccionario vacío para poder simular un servidor de archivos.
files = {}

# Creando una lista para guardar los nombres de los archivos txt.
archivos_txt = []

# Guardando los nombres de los .txt ya creados en una simulación anterior.
carpeta = os.getcwd()
archivos_txt = [archivo for archivo in os.listdir(carpeta) if archivo.endswith('.txt')]

for i, nombre_archivo in enumerate(archivos_txt):
    if nombre_archivo.endswith('.txt'):
        archivos_txt[i] = nombre_archivo[:-4]  # elimina los últimos 4 caracteres (.txt)

def cargar_archivos():
    global files

    for archivo in archivos_txt:
        with open(archivo + ".txt", "r") as f:
            contenido = f.read()
            #tablas = ast.literal_eval(contenido)

            # # Quitarle al string del archivo el .txt.
            # arch = archivo.split(".")[0]

            # Cargando primero el nombre de cada archivo en la tabla.
            files[archivo] = ast.literal_eval(contenido)

# Función para crear un archivo.
def crear_archivo(nombre):
    if nombre in files:
        print("El archivo ya existe.")
    else:
        files[nombre] = ""
        archivos_txt.append(nombre)

    
    return nombre

# Función para escribir archivos.
def escribir_archivo(nombre, datos):
    if nombre in files:
        files[nombre] = datos

        return files

    else:
        print("El archivo no existe.")

# Función para leer archivos.
def leer_archivo(nombre):
    if nombre in files:
        return files[nombre]
    else:
        print("El archivo no existe.")

# Función para escribir el .txt.
def escribir_txt(nombre, datos):
    # # Creando un nuevo archivo con el nombre de la tabla.
    # crear_archivo(nombre + ".txt")

    # Escribiendo los datos en el archivo.
    for rowk, rowd in datos.items():

        print("Rowk: ", rowk)

        if rowk in files: 
            row_str = str(rowd) + "\n"
            escribir_archivo(nombre, row_str)
    
    # Guardando el contenido del archvio en un archivo de texto.
    with open(nombre + ".txt", "w") as f:
        f.write(leer_archivo(nombre))

# Método para eliminar archivo.
def eliminar_archivo(nombre):
    if nombre in files:
        del files[nombre]

        # Eliminando el archivo de la lista también.
        archivos_txt.remove(nombre)

        os.remove(nombre + ".txt")

    else:
        print("El archivo {nombre} no existe.")

# Método para eliminar todos los archivos.
def eliminar_archivos():

    for file in list(files):

        eliminar_archivo(file)
    
    print("Files: ", files)