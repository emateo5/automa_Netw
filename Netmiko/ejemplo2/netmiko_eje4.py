# Uso de send_config_multiline para enviar configuración multilínea
# Casos especiales donde se espera una interacción, ejemplo: borrar un archivo

from netmiko import ConnectHandler
from datetime import datetime

cisco_device = {
    'device_type': 'cisco_ios',
    'host': '10.2.0.103',
    'username': 'netsim',
    'password': 'netsim1234',
    'ssh_config_file': '~/.ssh/config'
}

# Send multiline configuration using timing
commands = [
        f"del flash:/eje1.txt",
        "\n",
        "y"
    ]

start = datetime.now()
print ("Usando send_multiline_timing")
connection = ConnectHandler(**cisco_device)
connection.enable()
output = connection.send_multiline_timing(commands)
end = datetime.now()
print (f"Tiempo de ejecución: {end - start}")
print (f"Output: \n{output}\n")
connection.disconnect()

# Send multiline configuration using patterns
commands = [
        [f"del flash:/eje2.txt", r"Delete filename"],
        ["\n", r"confirm"],
        ["y", ""],
    ]
start = datetime.now()
print ("Usando send_multiline and patterns")
connection = ConnectHandler(**cisco_device)
connection.enable()
output = connection.send_multiline(commands)
end = datetime.now()
print (f"Tiempo de ejecución: {end - start}")
print (f"Output: \n{output}\n")
connection.disconnect()
