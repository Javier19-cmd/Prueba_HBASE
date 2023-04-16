# Comando create.

   El comando create se ejecuta de la siguiente manera: 

   create nombre_tabla {"1": {"cf1": {"A": "valor_1","B": "valor_2"},"cf2": {"A": "valor_3", "B": "valor_4"}},"2": {"cf1": {"A": "valor_5","B": "valor_6"},"cf3": {"A": "valor_7","B": "valor_8"}}}
   
   El código detecta el comando create, luego el nombre_tabla y por último la tabla.

# Comando describe.

    El comando describe lo que hace es imprimir en pantalla las column families que tiene cada columna existente en el directorio.

# Comando drop.

    El comando drop se ejecuta de la siguiente manera: 

    drop nombre_tabla

    El código detecta el comando drop y luego el nombre_tabla. Esta tabla se elimina de la lista de tablas y del directorio.