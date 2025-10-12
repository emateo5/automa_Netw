# Script para configuración de un dispositivo Cisco usando Netmiko set_config_set

from netmiko import ConnectHandler

cisco_device = {
    'device_type': 'cisco_ios',
    'host': 'X.X.X.X',
    'username': 'xxxx',
    'password': 'xxxx',
    'ssh_config_file': '~/.ssh/config'
}

connect = ConnectHandler(**cisco_device)
if connect.is_alive:
    print("Conexión exitosa al dispositivo Cisco")
else:
    print("Error en la conexión al dispositivo Cisco")
    exit(1)

# Comandos de configuración
config_commands = ['no interface loopback0', 'interface loopback1', 'ip address 192.168.1.1 255.255.255.0']

output = connect.send_config_set(config_commands)
print(output)

# Verificar la configuración
output = connect.send_command('show running-config')
print(output)

# Cerrar la conexión
connect.disconnect()




