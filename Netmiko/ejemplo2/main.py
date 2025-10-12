from netmiko_clase import ConfigurationClass
from datos_config import datos_config
from datos_device import datos_device

def config_from_file():
    config = ConfigurationClass()
    connection = config.connect(datos_device)
    config.create_config_template(template_file="temp_interfaces.j2", data=datos_config, config_file="config.txt", template_dir="./templates")
    output = config.send_config_from_file(connection, file_path="config.txt")
    has_errors = config.check_config_errors(output)
    if not has_errors:
        config.save_config(connection)
        show_output = config.send_command(connection, command="show running-config")
        print(show_output)
    config.disconnect(connection)

def config_from_set():
    config = ConfigurationClass()
    connection = config.connect(datos_device)
    config_commands = [
        'interface loopback3',
        ' ip address 10.1.0.3 255.255.255.255',
        ' description Loopback 3',
        ' no shutdown'
    ]
    output = config.send_config_set(connection, config_commands)
    has_errors = config.check_config_errors(output)
    if not has_errors:
        config.save_config(connection)
        show_output = config.send_command(connection, command="show running-config")
        print(show_output)
    config.disconnect(connection)

if __name__ == "__main__":
    print("Configuración desde archivo:")
    config_from_file()
    print("\nConfiguración desde lista de comandos:")
    config_from_set()
