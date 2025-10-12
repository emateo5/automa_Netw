# Script para generar y aplicar un template de configuración jinja de un dispositivo Cisco

from netmiko import ConnectHandler
from jinja2 import Environment, FileSystemLoader
from datos_config import datos

# Datos de conexion al dispositivo
cisco_device = {
    'device_type': 'cisco_ios',
    'host': '10.2.0.103',
    'username': 'netsim',
    'password': 'netsim1234',
    'ssh_config_file': '~/.ssh/config'
}

# Cargar el template desde el archivo
file_loader = FileSystemLoader('./templates')
# Crear el entorno jinja2
env = Environment(loader=file_loader)
# Cargar el template
template = env.get_template('temp_interfaces.j2')
# Renderizar el template con los datos
output = template.render(datos)

# Guardar la configuración generada en un archivo
with open('config.txt', 'w') as f:
    f.write(output)

# Conectar al dispositivo y enviar la configuración
connect = ConnectHandler(**cisco_device)
if connect.is_alive:
    print("Conexión exitosa al dispositivo Cisco")
    connect.save_config()
else:
    print("Error en la conexión al dispositivo Cisco")
    exit(1)
output = connect.send_config_from_file('config.txt')
# Verificar si hubo errores en la configuración enviada
if "Invalid input" in output:
    print("Error en la configuración enviada")
    output_list = output.splitlines()
    for ind, line in enumerate(output_list):
        if "^" in line:
            print (f"Error en el comando: {output_list[ind-1]}")
            exit(1)
else:
    print("Configuración enviada correctamente")


# Verificar la configuración
output = connect.send_command('show running-config')
print (output)

# Cerrar la conexión
connect.disconnect()