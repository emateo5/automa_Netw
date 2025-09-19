import json
from pathlib import Path
from  diccionario import devices

path_file = Path(__file__).parent / "devices.json"

class JsonHandler:
    # Serializacion
    def create_json(self, data, path):
        with open(path, 'w') as f:
            json.dump(data, f, indent=3)
        print(f"Archivo JSON creado en: {path}")

    # Deserializacion
    def read_json(self, path):
        with open(path, 'r') as f:
            data = json.load(f)
        return data

if __name__ == "__main__":
    handler = JsonHandler()
    handler.create_json(devices, path_file)
    data = handler.read_json(path_file)
    print("Datos leídos del archivo JSON:")
    print(data)

    print(f"{"\n"}Accediendo a datos específicos:")
    print("Primer Router:")
    print("Nombre:", data.get("routers", [])[0].get("name", "No hay nombre"))
    print("IP:", data.get("routers", [])[0].get("ip", "No hay IP"))
    print("Máscara:", data.get("routers", [])[0].get("mask", "No hay máscara"))
    print("Vendor:", data.get("routers", [])[0].get("vendor", "No hay vendor"))
    print("Modelo:", data.get("routers", [])[0].get("model", "No hay modelo"))
    print("Ubicación:", data.get("routers", [])[0].get("location", "No hay ubicación"))
    print("Activo:", data.get("routers", [])[0].get("activo", "No hay estado"))

    # Manipulación de un json que esta en formato string y no en un json puro.
    json_string = '{"routers":[{"name":"Router1","ip":"192.168.1.1","mask":"255.255.255.0","vendor":"Cisco","model":"ISR","location":"Sala de servidores","activo":true}]}'
    json_data = json.loads(json_string)
    print(f"{"\n"}Datos del JSON en formato string:")
    print(json_data)

    # Serialización de un diccionario a un string JSON
    json_string = json.dumps(devices, indent=3)
    print(f"{"\n"}Diccionario serializado a string JSON:")
    print(json_string)

    ## Apertura de un archivo sin usar with open
    # f = open(path_file, 'r')
    # data = json.load(f)
    # f.close()