import uuid
import time

# Diccionario para almacenar las tablas
tablas = {}

# Función para crear una tabla
def crear_tabla(nombre, column_families, datos):
    if nombre in tablas:
        print("La tabla ya existe.")
    else:
        tablas[nombre] = {}

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

    print(f"Celda ({column}, {row_key}, {value}, {timestamp}) agregada a la columna familiar {cf} de la tabla {nombre_tabla}.")


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
