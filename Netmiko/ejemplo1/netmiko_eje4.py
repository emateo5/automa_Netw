# Uso de CiscoConfParse para parsear la salida

import netmiko
from netmiko import ConnectHandler
from ciscoconfparse import CiscoConfParse


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
    commands = ["sh running-config"]
    for command in commands:
        output = connection.send_command(command, expect_string=r'#')
        output_list = output.splitlines()
        parse = CiscoConfParse(output_list, factory=True)
        interfaces = parse.find_objects(r"^interface") # Buscar todas las líneas que comienzan con "interface"
        for inter in interfaces:
            list_interfaces = inter.text.split(" ")
            print (f"Interfaz: {list_interfaces[1]}")
            tiene_ip = inter.re_search_children(r"^\s+ip address") # Buscar líneas que contienen "ip address" dentro de la interfaz
            if tiene_ip:
                for ip in tiene_ip:
                    print (f"  {ip.text}")
            else:
                print ("  No tiene IP asignada")
        
    # Cerrar la conexión
    connection.disconnect()
except Exception as error:
    print(f"Error en Netmiko: {error}")
    exit(1)
