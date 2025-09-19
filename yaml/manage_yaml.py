import yaml
from pathlib import Path
path_file = Path(__file__).parent / "file.yaml"

class YamlHandler:
    # Deserializacion
    def read_yaml(self, path):
        with open(path, 'r') as f:
            data = yaml.safe_load(f)
        return data
    
if __name__ == "__main__":
    handler = YamlHandler()
    data = handler.read_yaml(path_file)
    print("Datos leídos del archivo YAML:")
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