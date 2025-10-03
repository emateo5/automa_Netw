# Integración de Netmiko y TextFSM y CiscoConfParse en una clase

import netmiko
from netmiko import ConnectHandler
from ciscoconfparse import CiscoConfParse

class NetmikoInicial():

    # Coneccion al dispositivo
    def connect(self, device_params: dict) -> ConnectHandler:
        try:
            print ("Estableciendo conexión...")
            self.connection = ConnectHandler(**device_params)
            print("Conexión establecida con éxito.")
            return self.connection
        except netmiko.NetmikoTimeoutException:
            print(f"Timeout al conectar con el dispositivo {device_params.get('host')}")
            return None
        except netmiko.NetmikoAuthenticationException:
            print(f"Error de autenticación con el dispositivo {device_params.get('host')}")
            return None
        except Exception as error:
            print(f"Error en Netmiko: {error}")
            return None
        
    # Modo privilegiado
    def enable_mode(self, connection: ConnectHandler) -> bool | None:
        try:
            connection.enable()
            print ("Modo privilegiado habilitado.")
            return connection.check_enable_mode()
        except Exception as error:
            print(f"Error al entrar en modo privilegiado: {error}")
            return None
        
    # Modo de configuración global
    def config_mode(self, connection: ConnectHandler) -> bool | None:
        try:
            connection.config_mode()
            print("Modo de configuración global habilitado.")
            return connection.check_config_mode()
        except Exception as error:
            print(f"Error al entrar en modo de configuración: {error}")
            return None
        
    # Obtiene el prompt actual
    def get_prompt(self, connection: ConnectHandler) -> str | None:
        try:
            return connection.find_prompt()
        except Exception as error:
            print(f"Error al obtener el prompt: {error}")
            return None

    # Enviar comandos
    def send_command(self, connection: ConnectHandler, command: str, expect_string: str = r'#', use_textfsm: bool = False) -> list | str | None:
        try:
            output = connection.send_command(command, expect_string=expect_string, use_textfsm=use_textfsm)
            print (f"Comando '{command}' ejecutado.")
            return output
        except Exception as error:
            print(f"Error al enviar el comando {command}: {error}")
            return None

    def connection_status(self, connection: ConnectHandler) -> bool | None:
        try:
            return connection.is_alive()
        except Exception as error:
            print(f"Error al verificar el estado de la conexión: {error}")
            return None

    def parse_running_config(self, config_output: str) -> list | None:
        try:
            output_list = config_output.splitlines()
            parse = CiscoConfParse(output_list, factory=True)
            interfaces = parse.find_objects(r"^interface") # Buscar todas las líneas que comienzan con "interface"
            interface_data = []
            for inter in interfaces:
                list_interfaces = inter.text.split(" ")
                interface_info = {"interface": list_interfaces[1], "ip_addresses": []}
                tiene_ip = inter.re_search_children(r"^\s+ip address") # Buscar líneas que contienen "ip address" dentro de la interfaz
                if tiene_ip:
                    for ip in tiene_ip:
                        interface_info["ip_addresses"].append(ip.text)
                else:
                    interface_info["ip_addresses"].append("No tiene IP asignada")
                interface_data.append(interface_info)
            return interface_data
        except Exception as error:
            print(f"Error al parsear la configuración: {error}")
            return None
        

    def disconnect(self, connection: ConnectHandler) -> bool | None:
        try:
            connection.disconnect()
            print("Conexión cerrada.")
            return connection.is_alive()
        except Exception as error:
            print(f"Error al cerrar la conexión: {error}")
            return None
        
    