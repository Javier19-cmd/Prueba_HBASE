import os

# Creando un diccionario vacío para poder simular un servidor de archivos.
files = {}

# Función para crear un archivo.
def crear_archivo(nombre):
    if nombre in files:
        print("El archivo ya existe.")
    else:
        files[nombre] = ""
    
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

        os.remove(nombre + ".txt")

    else:
        print("El archivo no existe.")