from class_device_config import ConfigDevices
from class_create_configs import CreateConfig
import json
import os
from datetime import datetime

def main():
    print (f"-> Iniciando proceso de automatización de configuración de dispositivos de red...")
    net_conf = ConfigDevices()
    create_config = CreateConfig()

    # Leer archivo modelo de datos
    dic_modelo = create_config.read_yaml("modelo_datos.yaml")
    print (json.dumps(dic_modelo, indent=4))

    # Generar archivos de configuracion por dispositivo
    print (f"{'\n'}-> Generando archivos de configuración...")
    for device in dic_modelo.get("modelo").get("infra_spec").get("devices"):
        hostname = device.get('hostname')
        for config in device.get("config_spec"):
            config_template = config.get("template")
            data_path = config.get("data_path")
            config_file_name = f"{hostname}_{config.get('config_file')}"

            # Renderizar template
            print(f"Creando archivo de configuración '{config_file_name}' usando plantilla '{config_template}' para dispositivo '{hostname}'")
            template = create_config.render_template(template_name=config_template, data={data_path: device.get(data_path)})
            create_config.guardar_config_file(config_file_name, template)
            print(f"Archivos de configuración para {hostname} creados.")

    # Almacenar archivos de configuracion generados
    print(f"{'\n'}-> Archivos de configuración disponibles:")
    config_files = os.listdir("./configs")
    [print (f) for f in sorted(config_files) if f.endswith(".cfg")]

    # Conectar y configurar cada dispositivo
    print (f"{'\n'}-> Conectando a dispositivos y aplicando configuraciones...")
    start_total_configuration_duration = datetime.now()
    start_time = datetime.now()
    for device in dic_modelo.get("modelo").get("infra_spec").get("devices"):
        connection_params = device.get("connection")
        host_ip = connection_params.get("host")
        hostname = device.get("hostname")

       # Conectar al dispositivo
        connection = net_conf.connect_device(connection_params)
        print(f"{'\n'}Conectado al dispositivo '{hostname}' en IP '{host_ip}'")

        # Leer archivos de configuracion y enviarlos a los dispositivos
        print (f"{'\n'}-> Procesando archivos de configuración para dispositivo '{hostname}'...")

        # Almacenar solo los archivos de configuracion correspondientes al dispositivo
        conf_file_list = [conf_file for conf_file in config_files if conf_file.startswith(hostname)]
        
        for config_file in conf_file_list:
            print(f"Aplicando configuración desde '{config_file}' para dispositivo '{hostname}'")
            output = net_conf.send_config_commands(connection=connection, config_file=config_file)
            
            # Verificar errores en la salida
            has_error = net_conf.check_output_error(output)
            if has_error:
                print(f"Errores encontrados en configuración para '{device.get('hostname')}'. Abortando configuraciones adicionales.")
                break
            else:
                print(f"Configuración desde '{config_file}' aplicada exitosamente al dispositivo '{hostname}'")

        # Guardar configuración
        if not has_error:
            net_conf.save_configuration(connection)
            print(f"{'->'} Configuración guardada exitosamente en dispositivo '{hostname}' en IP '{host_ip}'")
        end_time = datetime.now()
        
        # Calcular e imprimir duración de configuración del dispositivo
        duration = end_time - start_time
        print(f"{'->'} Tiempo tomado para configurar dispositivo '{hostname}': {duration}")

        # Desconectar del dispositivo
        net_conf.disconnect_device(connection)
        print(f"{'->'} Desconectado del dispositivo '{hostname}' en IP '{host_ip}'")
    
    # Imprimir duración total de configuración
    end_total_configuration_duration = datetime.now()
    total_configuration_duration = end_total_configuration_duration - start_total_configuration_duration
    print(f"{'\n'}-> Tiempo total tomado para configurar todos los dispositivos: {total_configuration_duration}")

if __name__ == "__main__":
    main()
