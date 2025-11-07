# Validacion de modelo de datos de infraestructura de red con json schema
# Nombres de los archivos de datos y schema, se ingresan como parametros desde CLI

import json
import jsonschema
from jsonschema import FormatChecker
from jsonschema.exceptions import ValidationError
import yaml
import sys

def main(modelo: str, esquema: str) -> None:
    print (f"{'\n'}->Validando modelo de datos")

    # Cargar el esquema JSON
    try:
        with open(esquema) as schema_file:
            schema = json.load(schema_file)
    except FileNotFoundError:
        print(f"Error: El archivo {esquema} no fue encontrado.")
        sys.exit(1)
    print (f"Json schema: \n{json.dumps(schema, indent=3)}\n")
    
    # Cargar el modelo de datos
    try:
        with open(modelo) as data_file:
            data = yaml.safe_load(data_file)
        print (f"Modelo de datos: \n{json.dumps(data, indent=3)}\n")
    except FileNotFoundError:
        print(f"Error: El archivo {modelo} no fue encontrado.")
        sys.exit(1)

    # Validar el modelo de datos
    try:
        jsonschema.validate(instance=data, schema=schema, format_checker=FormatChecker())
        print(f"{' ' * 4}-> El modelo de datos es válido.")
    except ValidationError as error:
        print(f"{' ' * 4}-> El modelo de datos es inválido:\n{error.message}\nPath: {list(error.path)}\nValidator: {error.validator}")

if __name__ == "__main__":
    # Obtener los parámetros desde la línea de comandos, sys.argv[0] es el nombre del script
    params = sys.argv
    if len (params) != 3:
        print(f"Uso: python {params[0]} <archivo_modelo_datos.yaml> <archivo_modelo_schema.json>")
        sys.exit(1)
    main(modelo=params[1], esquema=params[2])
