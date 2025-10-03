# Netmiko Send Show Commands

import netmiko
from netmiko import ConnectHandler

# Definir los parámetros de conexión
device = {
    'device_type': 'cisco_ios',
    'host': 'X.X.X.X',
    'username': 'xxxx',
    'password': 'xxxx',
    'ssh_config_file': '~/.ssh/config'
}

try:
    # Establecer la conexión SSH
    connection = ConnectHandler(**device)
    print("Conexión establecida con éxito.")
    if connection.is_alive():
        print("La conexión está activa.")
    else:
        print("La conexión no está activa.")
        exit(1)

    # Prompt al inicio
    print(f"Prompt inicial: {connection.find_prompt()}")
    
    # Entrar en modo privilegiado
    connection.enable()
    print ("Modo privilegiado habilitado.")
    print (f"Prompt modo privilegiado: {connection.find_prompt()}")

    if connection.check_enable_mode():
        # Modo de configuración global
        connection.config_mode()
        print("Modo de configuración global habilitado.")
        print(f"Prompt en modo de configuración: {connection.find_prompt()}")

        if "(config" in connection.find_prompt():
            print("Actualmente en modo de configuración, salir del mismo.")
            connection.exit_config_mode()
            print(f"Prompt después de salir del modo de configuración: {connection.find_prompt()}")

        # Enviar comandos
        commands = ["sh ip int brief"]
        for command in commands:
            output = connection.send_command(command, expect_string=r'#')
            if "GigabitEthernet0/0" in output:
                print(f"El comando '{command}' se ejecutó correctamente.")
            print(f"{'\n'}Salida del comando {command}: \n{output}\n")
    
    # Cerrar la conexión
    connection.disconnect()
except Exception as error:
    print(f"Error en Netmiko: {error}")
    exit(1)