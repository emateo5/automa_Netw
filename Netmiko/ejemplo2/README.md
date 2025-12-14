# Proyecto de Automatización de Redes con Netmiko y Jinja2

## Descripción del Proyecto

Este proyecto implementa una solución completa de automatización para la configuración de dispositivos de red Cisco IOS utilizando Python, Netmiko y templates Jinja2. El objetivo es simplificar y estandarizar la gestión de configuraciones de red mediante scripts modulares y reutilizables.

**Autor:** Ed Scrimaglia  
**Versión:** 1.0  
**Fecha de Creación:** 13 de Septiembre de 2025
**Descripción**: Ejemplo con Netmiko, configuración y renderización de templates jinja2

---

## Características Principales

- Conexión SSH automatizada a dispositivos Cisco IOS
- Configuración mediante comandos directos (`send_config_set`)
- Configuración desde archivos de texto (`send_config_from_file`)
- Generación dinámica de configuraciones usando templates Jinja2
- Validación automática de errores de configuración
- Gestión de comandos multilínea con patrones de interacción
- Clase reutilizable para operaciones de red (`ConfigurationClass`)
- Manejo robusto de excepciones de conexión

---

## Dependencias

El proyecto utiliza las siguientes librerías Python:

```toml
[dependencies]
netmiko >= 4.6.0    # Librería para conexiones SSH a dispositivos de red
jinja2 >= 3.1.6     # Motor de templates para generación de configuraciones
```

Para instalar las dependencias:

```bash
uv add netmiko jinja2
```

---

## Estructura del Proyecto

```tree
ejemplo2/
├── config.txt                      # Archivo de configuración generado
├── datos_config.py                 # Datos para templates (interfaces)
├── datos_device.py                 # Parámetros de conexión al dispositivo
├── integrador2.py                  # Script principal integrador
├── netmiko_clase.py                # Clase ConfigurationClass
├── netmiko_eje1.py                 # Ejemplo 1: send_config_set
├── netmiko_eje2.py                 # Ejemplo 2: send_config_from_file
├── netmiko_eje3.py                 # Ejemplo 3: Templates Jinja2
├── netmiko_eje4.py                 # Ejemplo 4: send_multiline
├── pyproject.toml                  # Configuración del proyecto
├── README.md                       # Este archivo
└── templates/
    ├── temp_interfaces.j2          # Template principal de interfaces
    └── ejemplos_templates/
        ├── filters.j2              # Ejemplos de filtros Jinja2
        ├── include.j2              # Ejemplo de inclusión de templates
        ├── included.j2             # Template incluido
        ├── namespace.j2            # Ejemplo de namespaces
        └── variables.j2            # Ejemplos de variables
```

---

## Componentes del Proyecto

### 1. **Clase ConfigurationClass** (`netmiko_clase.py`)

Clase principal que encapsula todas las operaciones de configuración de dispositivos de red.

**Métodos principales:**

| Método | Descripción |
|--------|-------------|
| `connect(device_params)` | Establece conexión SSH al dispositivo |
| `send_config_from_file(connection, file_path)` | Envía configuración desde archivo |
| `send_config_set(connection, config_commands)` | Envía lista de comandos de configuración |
| `check_config_errors(output)` | Valida errores en la salida de configuración |
| `send_command(connection, command)` | Ejecuta comando show con soporte TextFSM |
| `save_config(connection)` | Guarda la configuración del dispositivo |
| `disconnect(connection)` | Cierra la conexión SSH |
| `create_config_template(template_file, data, config_file)` | Genera configuración desde template Jinja2 |

### 2. **Archivos de Datos**

**`datos_device.py`:** Define los parámetros de conexión al dispositivo:

```python
datos_device = {
    'device_type': 'cisco_ios',
    'host': '10.2.0.10X',
    'username': 'netsim',
    'password': 'password',
    'ssh_config_file': '~/.ssh/config'
}
```

**`datos_config.py`:** Estructura de datos para renderizar templates:

```python
datos_config = {
    'interfaces': [
        {
            'name': 'loopback1',
            'ip': '10.1.0.X',
            'mask': '255.255.255.255',
            'description': 'Loopback 1',
            'shutdown': False
        },
        # ... más interfaces
    ]
}
```

### 3. **Templates Jinja2**

**Template principal** (`templates/temp_interfaces.j2`):

```jinja
{% for inter in interfaces -%}
interface {{ inter.name }} 
  ip address {{ inter.ip }} {{ inter.mask }}
  description {{ inter.description }}
{%- if inter.shutdown %}
  shutdown
{%- else %}
  no shutdown
{%- endif %}
{% endfor %}
```

El directorio `ejemplos_templates/` contiene ejemplos didácticos de:

- Uso de filtros Jinja2 (upper, lower, join, etc.)
- Variables y alcance
- Inclusión de templates
- Namespaces

---

## Ejemplos de Uso

### **Ejemplo 1: Configuración con send_config_set** (`netmiko_eje1.py`)

Envía comandos directamente como lista:

```python
config_commands = [
    'no interface loopback0',
    'interface loopback1',
    'ip address 192.168.1.1 255.255.255.0'
]
output = connect.send_config_set(config_commands)
```

### **Ejemplo 2: Configuración desde archivo** (`netmiko_eje2.py`)

Lee configuración desde `config.txt` y la aplica:

```python
output = connect.send_config_from_file('config.txt')
```

### **Ejemplo 3: Templates Jinja2** (`netmiko_eje3.py`)

Genera configuración dinámica desde template:

```python
template = env.get_template('temp_interfaces.j2')
output = template.render(datos)
```

### **Ejemplo 4: Comandos Multilínea** (`netmiko_eje4.py`)

Maneja interacciones complejas (ej: borrado de archivos):

```python
# Usando timing
commands = ["del flash:/eje1.txt", "\n", "y"]
output = connection.send_multiline_timing(commands)

# Usando patrones
commands = [
    ["del flash:/eje2.txt", r"Delete filename"],
    ["\n", r"confirm"],
    ["y", ""]
]
output = connection.send_multiline(commands)
```

### **Script Integrador** (`integrador2.py`)

Combina todas las funcionalidades en flujos completos:

**Flujo 1: Configuración desde template**

1. Conecta al dispositivo
2. Genera configuración desde template Jinja2
3. Aplica la configuración
4. Valida errores
5. Guarda cambios
6. Verifica configuración final
7. Guarda

---

## Casos de Uso

1. **Provisioning Masivo**: Configurar múltiples dispositivos con parámetros personalizados
2. **Estandarización**: Aplicar configuraciones base consistentes
3. **Migraciones**: Actualizar configuraciones de forma controlada
4. **Troubleshooting**: Ejecutar comandos show y análisis con TextFSM
5. **Configuraciones Complejas**: Usar templates para BGP, OSPF, VLANs, etc.

---

## Manejo de Errores

El proyecto implementa:

- **Excepciones de conexión**: `NetmikoTimeoutException`, `NetmikoAuthenticationException`
- **Validación de sintaxis**: Detección de "Invalid input" con indicación de línea exacta
- **Verificación de estado**: Comprobación de conexión activa antes de operaciones
- **Logging informativo**: Mensajes claros de éxito/error en cada operación

Ejemplo de validación:

```python
if "Invalid input" in output:
    print("Error en la configuración enviada")
    output_list = output.splitlines()
    for ind, line in enumerate(output_list):
        if "^" in line:
            print(f"Error en el comando: '{output_list[ind-1]}'")
```

---

## Seguridad

- Las credenciales se almacenan en `datos_device.py` (no incluir en control de versiones)
- Uso de `ssh_config_file` para configuración SSH personalizada
- Se recomienda uso de variables de entorno para credenciales en producción

---

## Referencias y Recursos

- [Documentación de Netmiko](https://github.com/ktbyers/netmiko)
- [Jinja2 Documentation](https://jinja.palletsprojects.com/)
- [Cisco IOS Command Reference](https://www.cisco.com/c/en/us/support/ios-nx-os-software/ios-15-4m-t/products-command-reference-list.html)

---

## Aprendizaje

Este proyecto es ideal para:

- Estudiantes de redes y automatización
- Ingenieros de red que inician en DevOps
- Práctica de Python aplicado a redes
- Comprensión de templates dinámicos con Jinja2

---

## Licencia

Proyecto educativo - UTN-FRC Academia Cisco - Network Automation Engineer Course

---

**Última actualización**: Diciembre 2025
