# Reutilizacion de codigo en modelo de datos en YAML
# El nombre del archivos de datos se ingresa como parametro desde CLI

import yaml
import json
import sys

def main(modelo: str) -> None:
    print (f"{'\n'}->Reutilizacion de codigo en modelo de datos")
    
    # Cargar el modelo de datos
    try:
        with open(modelo) as data_file:
            data = yaml.safe_load(data_file)
        print (f"Modelo de datos: \n{json.dumps(data, indent=3)}\n")
    except FileNotFoundError:
        print(f"Error: El archivo {modelo} no fue encontrado.")

if __name__ == "__main__":
    # Obtener los parámetros desde la línea de comandos, sys.argv[0] es el nombre del script
    params = sys.argv
    if len (params) != 2:
        print(f"Uso: python {params[0]} <archivo_modelo_datos.yaml>")
        sys.exit(1)
    main(modelo=params[1])
