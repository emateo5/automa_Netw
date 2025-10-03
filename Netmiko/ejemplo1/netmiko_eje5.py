# Utilizacion de la clase NetmikoInicial para un solo dispositivo

from netmiko_clase import NetmikoInicial
import json

def main(): # Función principal para un solo dispositivo
    device_params = {
        "device_type": "cisco_ios",
        "host": "X.X.X.X",
        "username": "xxxx",
        "password": "xxxx",
        "ssh_config_file": "~/.ssh/config"
    }

    net_instance = NetmikoInicial()
    connection = net_instance.connect(device_params)
    if not net_instance.connection_status(connection):
        print ("La conexión no está activa.")
        return # Salir si la conexión no está activa
    if not net_instance.enable_mode(connection):
        print ("No se pudo entrar en modo privilegiado.")
        return # Salir si no se puede entrar en modo privilegiado
    prompt = net_instance.get_prompt(connection)
    print(f"Prompt actual: {prompt}")
    commands = ["sh ip int brief", "sh version"]
    for command in commands:
        output = net_instance.send_command(connection, command, expect_string=r'#', use_textfsm=True)
        if isinstance(output, list): # Si la salida es una lista, se asume que TextFSM la ha parseado
            print(f"-> Salida estructurada '{command}': \n{json.dumps(output, indent=3)}\n")
        elif isinstance(output, str): # Si la salida es una cadena, se asume que no fue parseada
            print(f"-> Salida no estructurada '{command}': \n{output}\n")

    command = "sh running-config"
    output = net_instance.send_command(connection, command, expect_string=r'#', use_textfsm=False)
    response = net_instance.parse_running_config(output)
    print (f"-> Configuración parseada: \n{json.dumps(response, indent=3)}\n")

    net_instance.disconnect(connection)

main()