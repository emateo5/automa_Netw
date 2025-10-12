# Configuración de un dispositivo Cisco usando Netmiko desde un archivo de configuración txt

from netmiko import ConnectHandler

# Leer archivo de configuración
with open('config.txt') as file:
    file_commands = file.read()

print (file_commands)

# Definir parámetros de conexión
cisco_device = {
    'device_type': 'cisco_ios',
    'host': '10.2.0.103',
    'username': 'netsim',
    'password': 'netsim1234',
    'ssh_config_file': '~/.ssh/config'
}

#Conectar al dispositivo
connect = ConnectHandler(**cisco_device)
if connect.is_alive:
    print("Conexión exitosa al dispositivo Cisco")
else:
    print("Error en la conexión al dispositivo Cisco")
    exit(1)

# Enviar comandos de configuración desde el archivo
output = connect.send_config_from_file('config.txt')
print(output)

# Verificar la configuración
output = connect.send_command('show running-config')
print(output)

# Cerrar la conexión
connect.disconnect()
