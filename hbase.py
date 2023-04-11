import file as fl
from metodos import *

# Eliminando archivo.
#fl.eliminar_archivo(archivo)
column_families = ["cf1", "cf2", "cf3"]
datos = {
    "1": {
        "cf1": {
            "A": "valor_1",
            "B": "valor_2"
        },
        "cf2": {
            "A": "valor_3",
            "B": "valor_4"
        }
    },
    "2": {
        "cf1": {
            "A": "valor_5",
            "B": "valor_6"
        },
        "cf3": {
            "A": "valor_7",
            "B": "valor_8"
        }
    }
}

nombre, tabla = crear_tabla("HBase", column_families, datos)

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