import netmiko
from netmiko import ConnectHandler

# Definir los parámetros de conexión
device = {
    'device_type': 'cisco_ios',
    'host': '10.2.0.103',
    'username': 'netsim',
    'password': 'netsim1234',
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
    commands = ["sh ip int brief", "show ip route"]
    for command in commands:
        output = connection.send_command(command)
        print(f"{'\n'}Salida del comando {command}: {output}")
    
    # Cerrar la conexión
    connection.disconnect()
except Exception as error:
    print(f"Error al conectar: {error}")
    exit(1)