# Clase para manejo de configuración de dispositivos de red usando Netmiko y Jinja2

from netmiko import ConnectHandler
from netmiko import NetmikoTimeoutException, NetmikoAuthenticationException
from jinja2 import Environment, FileSystemLoader

class ConfigurationClass():
    # Connect to the device
    def connect(self, device_params: dict) -> ConnectHandler:
        try:
            connection = ConnectHandler(**device_params)
            if connection.is_alive:
                print(f"Conexión exitosa al dispositivo '{device_params.get('host')}'")
            else:
                print("Conexión no establecida.")
                exit(1)
            return connection
        except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
            print(f"Error de conexión: '{error}'")
            exit(1)
        except Exception as error:
            print(f"Error inesperado: '{error}'")
            exit(1)

    # Send configuration from a file
    def send_config_from_file(self, connection: ConnectHandler, file_path: str) -> str:
        if connection:
            output = connection.send_config_from_file(file_path)
            print (f"Configuración enviada desde el archivo '{file_path}'")
            return output
        else:
            print("No hay conexión establecida.")
            return None

    # Send configuration from a list of commands
    def send_config_set(self, connection: ConnectHandler, config_commands: list) -> str:
        if connection:
            output = connection.send_config_set(config_commands)
            print ("Configuración enviada desde la lista de comandos")
            return output
        else:
            print("No hay conexión establecida.")
            return None

    # Send configuration from a list of commands with multiline support
    def send_config_multiline(self, connection: ConnectHandler, config_commands: list) -> str:
        pass

    # Check for configuration errors in the output
    def check_config_errors(self, output: str) -> bool:
        if "Invalid input" in output:
            print("Error en la configuración enviada")
            output_list = output.splitlines()
            for ind, line in enumerate(output_list):
                if "^" in line:
                    print (f"Error en el comando: '{output_list[ind-1]}'")
            return True
        else:
            print("Configuración enviada correctamente")
            return False

    # Send a show command to the device
    def send_command(self, connection: ConnectHandler, command: str) -> str:
        if connection:
            output = connection.send_command(command, expect_string=r'#', use_textfsm=True)
            return output
        else:
            print("No hay conexión establecida.")
            return None

    # Save the device configuration
    def save_config(self, connection: ConnectHandler):
        if connection:
            connection.save_config()
            print("Configuración guardada.")
        else:
            print("No hay conexión establecida.")

    # Disconnect from the device
    def disconnect(self, connection: ConnectHandler):
        if connection:
            connection.disconnect()
            print ("Conexión cerrada.")
        else:
            print("No hay conexión establecida.")

    # Create configuration file from a Jinja2 template
    def create_config_template(self, template_file: str, data: dict, config_file: str, template_dir: str = "./templates") -> None:
        # Cargar el template desde el archivo
        file_loader = FileSystemLoader(template_dir)
        # Crear el entorno jinja2
        env = Environment(loader=file_loader)
        # Cargar el template
        template = env.get_template(template_file)
        # Renderizar el template con los datos
        output = template.render(data)
        # Guardar la configuración generada en un archivo
        try:
            with open(config_file, 'w') as f:
                f.write(output)
            print(f"Configuración generada desde '{template_file}' y guardada en el archivo '{config_file}'")
        except Exception as error:
            print(f"Error al guardar el archivo: '{error}'")
            exit(1)