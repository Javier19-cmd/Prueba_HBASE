import os
import ast
import json

# Creando un diccionario vacío para poder simular un servidor de archivos.
files = {}

# Creando una lista para guardar los nombres de los archivos txt.
archivos_txt = []

# Guardando los nombres de los .txt ya creados en una simulación anterior.
root = os.path.dirname(os.path.relpath(__file__))
ruta = os.path.join(root, 'tables')

archivos_txt = [archivo for archivo in os.listdir(ruta) if archivo.endswith('.txt')]

for i, nombre_archivo in enumerate(archivos_txt):
    if nombre_archivo.endswith('.txt'):
        archivos_txt[i] = nombre_archivo[:-4]  # elimina los últimos 4 caracteres (.txt)

# Función para crear un archivo.
def crear_archivo(nombre, nombr):

    #print("Nombre en crear archivo: ", nombre)

    if nombre in files:
        print("El archivo ya existe.")
    else:
        files[nombre] = ""
        archivos_txt.append(nombr)

    
    #return nombre

# Función para escribir archivos.
def escribir_archivo(nombre):
    if nombre in files:
        files[nombre] = {}

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
def escribir_txt(nombre):

    # Guardando el diccionario en un archivo de texto.
    with open("./tables/" + nombre + ".txt", "w") as f:
        f.write("{}")


# Método para eliminar archivo.
def eliminar_archivo(nombre):

    global archivos_txt

    print("Nombre del archivo: ", nombre)
    print("Archivos: ", archivos_txt)

    if nombre in archivos_txt:
        # Eliminando el archivo de la lista también.
        archivos_txt.remove(nombre)

        # Verificando que la tabla si el enable en false.

        #os.remove("./tables/" + nombre + ".txt")

        print("Nombre: ", nombre)

        # Eliminando el archivo del directorio /tables.
        os.remove("./tables/" + nombre + ".txt")

    else:
        print("El archivo {nombre} no existe.")

# Método para eliminar todos los archivos.
def eliminar_archivos():

    global archivos_txt

    for file in list(archivos_txt):

        eliminar_archivo(file)
    
    print("Files: ", files)