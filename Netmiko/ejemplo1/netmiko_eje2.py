# Uso de TextFSM y expected_string para parsear la salida

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
    
    # Entrar en modo privilegiado
    connection.enable()
    print ("Modo privilegiado habilitado.")
    
    # Enviar comandos
    commands = ["sh version"]
    for command in commands:
        output = connection.send_command(command, expect_string=r'#', use_textfsm=True)
        print (f"Tipo de datos del output del {command}, es: {type(output)}")
        if isinstance(output, list): # Si la salida es una lista, se asume que TextFSM la ha parseado
            print(f"Longitud de la lista de salida: {len(output)}")
            for line in output:
                print (f"la Version de IOS es: {line.get('version', 'N/A')}")
        else:
            print (f"La salida del comando {command} es:\n{output}")
            print(f"La salida no esta en formato estructurado")
    
    # Cerrar la conexión
    connection.disconnect()
except Exception as error:
    print(f"Error en Netmiko: {error}")
    exit(1)