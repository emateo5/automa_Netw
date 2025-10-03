# Global delay factor y fast_cli en Netmiko

import netmiko
from netmiko import ConnectHandler

# Definir los parámetros de conexión
device = [
    {
        'device_type': 'cisco_ios',
        'host': 'X.X.X.X',
        'username': 'xxxx',
        'password': 'xxxx',
        'ssh_config_file': '~/.ssh/config',
        'global_delay_factor': .1 #fast_cli=True
    },
    {
        'device_type': 'cisco_ios',
        'host': 'X.X.X.X',
        'username': 'xxxx',
        'password': 'xxxx',
        'ssh_config_file': '~/.ssh/config',
        'global_delay_factor': 1.5
    }
]

try:
    for dev in device:
        # Establecer la conexión SSH
        connection = ConnectHandler(**dev)
        print ("*"*80)

        print("Conexión establecida con éxito.")
        if connection.is_alive():
            print("La conexión está activa.")
        else:
            print("La conexión no está activa.")
            exit(1)
        
        # Entrar en modo privilegiado
        connection.enable()
        print ("Modo privilegiado habilitado.")
        
        # Enviar comandos
        commands = ["sh version"]
        for command in commands:
            output = connection.send_command(command, expect_string=r'#', use_textfsm=True)
            if isinstance(output, list): # Si la salida es una lista, se asume que TextFSM la ha parseado
                print(f"Longitud de la lista de salida: {len(output)}")
                for line in output:
                    print (f"la Version de IOS es: {line.get('version', 'N/A')}")
                    print (f"El Hostname es: {line.get('hostname', 'N/A')}")
            else:
                print (f"La salida del comando {command} es:\n{output}")
                print(f"La salida no esta en formato estructurado")
        
        # Cerrar la conexión
        connection.disconnect()
except Exception as error:
    print(f"Error en Netmiko: {error}")
    exit(1)