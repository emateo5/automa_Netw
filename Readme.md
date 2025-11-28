# Curso de Network Automation - UTN Academia

**Autor:** Ed Scrimaglia  
**Institución:** Universidad Tecnológica Nacional (UTN)  
**Curso:** Network Automation Engineer  
**Repositorio:** UTN-IaC

## Descripción General

Este repositorio contiene una colección completa de proyectos, ejemplos y casos de uso para la automatización de infraestructura de red. Los materiales cubren desde conceptos básicos de Python hasta implementaciones avanzadas de automatización utilizando herramientas estándar de la industria como Ansible, Netmiko, Jinja2 y YAML/JSON para modelado de datos.

El contenido está organizado de manera progresiva, permitiendo a los estudiantes avanzar desde fundamentos de programación hasta implementaciones profesionales de automatización de red.

## Objetivos del Curso

- Dominar fundamentos de Python para automatización
- Implementar automatización de red con Netmiko
- Gestionar configuraciones con Ansible
- Modelar infraestructura con YAML y validar con JSON Schema
- Desarrollar soluciones escalables y mantenibles
- Aplicar mejores prácticas de la industria

## Estructura del Repositorio

```
.
├── README.md                    # Este archivo
├── Python Basics/               # Fundamentos de Python
├── json/                        # Manejo de archivos JSON
├── yaml/                        # Manejo de archivos YAML
├── Modelado/                    # Modelado de datos con YAML/JSON Schema
├── Netmiko/                     # Automatización con Netmiko
│   ├── ejemplo1/               # Conceptos básicos de Netmiko
│   ├── ejemplo2/               # Netmiko con Jinja2
│   └── sim_caso/               # Caso de uso completo
└── Ansible/                     # Automatización con Ansible
    ├── ejemplo1/               # Variables y módulos básicos
    ├── ejemplo2/               # Estructuras de control
    └── ssh-config/             # Configuración SSH
```

## Módulos del Curso

### 1. Python Basics - Fundamentos de Programación

**Ubicación:** `Python Basics/`

**Descripción:** Introducción a conceptos fundamentales de Python orientados a automatización de redes.

**Contenido:**

- **`script_basic.py`**: Funciones básicas y estructuras
- **`class_basic_attr.py`**: Clases con atributos básicos
  - Clase `BasicMathAttr` con operaciones suma y resta
  - Manejo de atributos de instancia
- **`class_oper_basic_math.py`**: Operaciones matemáticas básicas
  - Clase `Basicas` con suma, resta, multiplicación, división
- **`class_oper_advance_math.py`**: Operaciones matemáticas avanzadas
  - Clase `Advance` con potencia y raíz cuadrada
- **`diccionario.py`**: Manejo de diccionarios y estructuras de datos
- **`main.py`**: Script integrador que utiliza todas las clases

**Conceptos clave:**

- Programación orientada a objetos (POO)
- Funciones y métodos
- Importación de módulos
- Estructuras de datos (diccionarios, listas)

**Ejecución:**

```bash
cd "Python Basics"
python main.py
```

---

### 2. JSON - Serialización y Deserialización

**Ubicación:** `json/`

**Descripción:** Manejo de archivos JSON para almacenamiento y transferencia de datos.

**Contenido:**

- **`diccionario.py`**: Definición de estructuras de datos (dispositivos de red)
- **`manage_json.py`**: Clase `JsonHandler` para operaciones JSON
  - Serialización: Convertir objetos Python a JSON
  - Deserialización: Convertir JSON a objetos Python
  - Lectura/escritura de archivos JSON
- **`devices.json`**: Archivo de datos de dispositivos generado

**Funcionalidades:**

- `create_json()`: Crear archivos JSON desde diccionarios
- `read_json()`: Leer y parsear archivos JSON
- Manipulación de JSON strings
- Acceso a datos específicos con `.get()`

**Ejemplo de uso:**

```python
handler = JsonHandler()
handler.create_json(devices, "devices.json")
data = handler.read_json("devices.json")
print(data.get("routers")[0].get("name"))
```

---

### 3. YAML - Configuración y Modelado

**Ubicación:** `yaml/`

**Descripción:** Trabajo con archivos YAML, formato preferido para configuraciones de automatización.

**Contenido:**

- **`manage_yaml.py`**: Clase `YamlHandler` para operaciones YAML
  - Deserialización con `yaml.safe_load()`
  - Lectura de archivos YAML
  - Acceso a datos estructurados
- **`file.yaml`**: Archivo de ejemplo con datos de dispositivos

**Ventajas de YAML:**

- Más legible que JSON
- Soporta comentarios
- Ideal para archivos de configuración
- Usado por Ansible y otras herramientas

**Ejemplo de uso:**

```python
handler = YamlHandler()
data = handler.read_yaml("file.yaml")
router_name = data.get("routers")[0].get("name")
```

---

### 4. Modelado - Validación de Datos

**Ubicación:** `Modelado/`

**Descripción:** Modelado estructurado de infraestructura de red con validación mediante JSON Schema.

**Contenido:**

**Scripts principales:**

- **`main_schema.py`**: Validador de modelos de datos
  - Valida archivos YAML contra esquemas JSON
  - Usa `jsonschema` con `FormatChecker`
  - Reporta errores detallados con paths
- **`main_reutilizacion.py`**: Ejemplos de reutilización en YAML
  - Anchors y aliases
  - Merge keys (`<<`)

**Archivos de datos:**

- `modelo_datos.yaml`: Modelo principal de infraestructura
- `ejemplo1_datos.yaml`: Ejemplo básico de metadatos
- `ejemplo2_datos.yaml`: Ejemplo de dispositivos con IPs
- `reutilizacion_a.yaml`: Ejemplo de merge keys
- `reutilizacion_b.yaml`: Ejemplo de anchors/aliases
- `reutilizacion_c.yaml`: Ejemplo combinado

**Esquemas de validación:**

- `modelo_schema.json`: Schema completo de infraestructura
- `ejemplo1_schema.json`: Schema básico
- `ejemplo2_schema.json`: Schema para dispositivos
- `ejemplo3_schema.json`: Schema adicional

**Características:**

- Validación de tipos de datos
- Validación de formatos (IPv4, IPv6, fechas)
- Campos requeridos y opcionales
- Rangos y restricciones (ej: VLANs 1-4094)
- Enumeraciones (ej: modos de interfaces)

**Ejecución:**

```bash
cd Modelado
python main_schema.py modelo_datos.yaml modelo_schema.json
python main_reutilizacion.py reutilizacion_a.yaml
```

**Documentación:** Ver `Modelado/README.md`

---

### 5. Netmiko - Automatización SSH

**Ubicación:** `Netmiko/`

**Descripción:** Automatización de dispositivos de red mediante conexiones SSH usando la librería Netmiko.

#### 5.1 Ejemplo 1 - Conceptos Básicos

**Ubicación:** `Netmiko/ejemplo1/`

**Contenido:**

- **`netmiko_clase.py`**: Clase `NetmikoInicial` con funcionalidades core
  - Conexión SSH a dispositivos
  - Modo privilegiado (enable)
  - Modo de configuración
  - Envío de comandos
  - Integración con TextFSM (parsing estructurado)
  - Integración con CiscoConfParse
  - Manejo de errores de conexión y autenticación

- **Scripts de ejercicios:**
  - `netmiko_eje1.py`: Conexión básica y comandos simples
  - `netmiko_eje2.py`: Uso de TextFSM para parseo
  - `netmiko_eje3.py`: Comandos múltiples
  - `netmiko_eje4.py`: Configuración de dispositivos
  
- **`integrador1.py`**: Ejemplo completo integrando todas las funcionalidades
  - Conexión y validación
  - Ejecución de comandos con TextFSM
  - Parsing de configuración running
  - Extracción de información de interfaces

**Conceptos clave:**

- `ConnectHandler`: Gestor de conexiones Netmiko
- TextFSM: Parsing estructurado de salidas
- CiscoConfParse: Análisis de configuraciones
- Manejo robusto de excepciones

**Métodos principales:**

```python
connect(device_params)          # Conectar a dispositivo
enable_mode(connection)         # Entrar a modo privilegiado
config_mode(connection)         # Entrar a modo configuración
send_command(connection, cmd)   # Ejecutar comando
parse_running_config(config)    # Parsear configuración
disconnect(connection)          # Cerrar conexión
```

---

#### 5.2 Ejemplo 2 - Netmiko + Jinja2

**Ubicación:** `Netmiko/ejemplo2/`

**Contenido:**

- **`netmiko_clase.py`**: Clase `ConfigurationClass` 
  - Conexión a dispositivos
  - Envío de configuración desde archivos
  - Envío de configuración desde listas
  - Verificación de errores de configuración
  - Guardado de configuraciones
  - Generación de configuraciones con Jinja2

- **`datos_device.py`**: Datos de dispositivos
- **`datos_config.py`**: Datos para templates
- **`config.txt`**: Archivo de configuración de ejemplo

- **Templates Jinja2** (`templates/`):
  - `temp_interfaces.j2`: Template para configuración de interfaces
  - Ejemplos de templates en `ejemplos_templates/`:
    - `filters.j2`: Uso de filtros Jinja2
    - `variables.j2`: Manejo de variables
    - `include.j2` / `included.j2`: Inclusión de templates
    - `namespace.j2`: Namespaces en Jinja2

- **Scripts de ejercicios:**
  - `netmiko_eje1.py`: Configuración desde archivo
  - `netmiko_eje2.py`: Configuración desde lista
  - `netmiko_eje3.py`: Uso de templates
  - `netmiko_eje4.py`: Validación de configuraciones
  
- **`integrador2.py`**: Integrador completo con templates

**Funcionalidades avanzadas:**

```python
send_config_from_file(conn, file)     # Configurar desde archivo
send_config_set(conn, commands)       # Configurar desde lista
check_config_errors(output)           # Validar configuración
create_config_template(template, data) # Generar con Jinja2
save_config(connection)               # Guardar configuración
```

---

#### 5.3 Simulacro de Caso - Solución Profesional

**Ubicación:** `Netmiko/sim_caso/`

**Descripción:** Sistema completo de automatización para configurar múltiples dispositivos de red de forma escalable y profesional.

**Componentes:**

- **`main.py`**: Orquestador principal
  - Lectura del modelo de datos
  - Generación de configuraciones
  - Conexión y configuración de dispositivos
  - Medición de tiempos
  - Logging detallado

- **`class_device_config.py`**: Clase `ConfigDevices`
  - Gestión de conexiones SSH
  - Aplicación de configuraciones
  - Validación de errores
  - Guardado de configuraciones

- **`class_create_configs.py`**: Clase `CreateConfig`
  - Renderizado de templates Jinja2
  - Creación de archivos de configuración
  - Lectura de archivos YAML
  - Serialización JSON

- **`modelo_datos.yaml`**: Modelo completo de infraestructura
  - Metadatos del proyecto
  - Dispositivos con configuración completa
  - Sección `config_spec` para configuración dinámica

- **Templates** (`templates/`):
  - `vlans.j2`: Configuración de VLANs
  - `int_access.j2`: Interfaces de acceso
  - `int_trunk.j2`: Interfaces trunk

- **Configuraciones generadas** (`configs/`):
  - Archivos `.cfg` generados automáticamente
  - Por dispositivo y tipo de configuración

**Innovaciones:**

1. **Config Spec Dinámico**: Define qué configuraciones generar

   ```yaml
   config_spec:
     - data_path: "vlans"
       template: "vlans.j2"
       config_file: "vlan.cfg"
   ```

2. **Arquitectura Modular**: Separación de responsabilidades
3. **Fail-Fast**: Aborta ante errores críticos
4. **Logging Detallado**: Feedback en cada paso
5. **Medición de Rendimiento**: Tiempo por dispositivo y total

**Topología configurada:**

- 2 switches (SW_Bld_A, SW_Bld_B)
- 3 VLANs (Ingenieria, Produccion, Finanzas)
- Interfaces trunk y access
- Conexiones a switches core

**Ejecución:**

```bash
cd Netmiko/sim_caso
python main.py
```

**Documentación completa:** Ver `Netmiko/sim_caso/README.md`

---

### 6. Ansible - Automatización Declarativa

**Ubicación:** `Ansible/`

**Descripción:** Automatización de red usando Ansible, herramienta líder de la industria para configuración y gestión de infraestructura.

#### 6.1 Ejemplo 1 - Variables y Módulos

**Ubicación:** `Ansible/ejemplo1/`

**Descripción:** Fundamentos de Ansible aplicados a redes Cisco IOS.

**Componentes:**

- **`inventario.ini`**: Inventario de dispositivos
  - Grupos: `cisco_ios_access_bsas`, `cisco_ios_access_cba`, `cisco_ios_datacenter`, `cisco_ios_core`
  - Variables de conexión y autenticación

- **Variables:**
  - `group_vars/cisco_ios.yaml`: Variables comunes
  - `host_vars/`: Variables por dispositivo (SW-Bld_A, SW-Bld_B)

- **Modelo de datos:**
  - `modelo_datos/modelo_datos.yaml`: Infraestructura completa
  - `json_files/validador_modelo.json`: JSON Schema

**Playbooks:**

1. **`playbook1.yaml`**: Consultas básicas
   - Ejecuta `show ip interface brief`
   - Muestra salidas de comandos
   - Múltiples plays para diferentes grupos

2. **`playbook2.yaml`**: Manipulación de variables
   - Carga de modelo de datos
   - Visualización con Jinja2
   - Lectura de JSON Schema
   - Uso de `set_fact`
   - Acceso a `hostvars`

3. **`playbook3.yaml`**: Hosts dinámicos
   - Hosts desde variables del modelo
   - Iteración sobre dispositivos
   - Loop control con labels

**Conceptos clave:**

- `vars_files`: Carga de datos externos
- `hostvars`: Variables compartidas entre hosts
- Módulo `cisco.ios.ios_command`
- Templates Jinja2 para formateo
- Validación con JSON Schema

**Ejecución:**

```bash
cd Ansible/ejemplo1
ansible-playbook -i inventario.ini playbook1.yaml
ansible-playbook -i inventario.ini playbook2.yaml -v
```

**Documentación completa:** Ver `Ansible/ejemplo1/README.md`

---

#### 6.2 Ejemplo 2 - Estructuras de Control

**Ubicación:** `Ansible/ejemplo2/`

**Descripción:** Estructuras de programación en Ansible: condicionales, loops, manejo de errores.

**Configuración:**

- `cfg/ansible.cfg`: Configuración de Ansible
  - Conexiones persistentes
  - Pipelining habilitado
  - Timeouts optimizados

**Tareas reutilizables** (`tasks/`):

- `validate.yaml`: Validación con JSON Schema
- `timestamp.yaml`: Obtención de timestamps

**Playbooks:**

1. **`playbook1.yaml`**: Condicionales básicas
   - `when` con variables booleanas
   - Validación de versión del modelo
   - Ejecución condicional de comandos

2. **`playbook2.yaml`**: Hostvars
   - Definición de variables en localhost
   - Consumo desde otros hosts con `hostvars['localhost']`
   - Compartir datos entre plays

3. **`playbook3.yaml`**: Loops con modelo de datos
   - Iteración sobre estructuras complejas
   - `loop_control` con labels
   - Acceso a datos anidados

4. **`playbook4.yaml`**: Loops con lista estática
   - Iteración sobre lista simple
   - Mensajes personalizados por elemento

5. **`playbook5.yaml`**: Manejo de errores
   - Bloques `block/rescue/always`
   - Captura de errores de conexión
   - Mensajes de diagnóstico
   - Limpieza garantizada con `always`

6. **`playbook6.yaml`**: Validación con JSON Schema
   - Inclusión de tareas reutilizables
   - Validación del modelo antes de usar
   - Engine `jsonschema`

**Conceptos demostrados:**

- Condicionales (`when`)
- Loops (`loop`, `loop_control`)
- Manejo de errores (`block/rescue/always`)
- Validación de datos (`ansible.utils.validate`)
- Tareas incluibles (`include_tasks`)
- Variables compartidas (`hostvars`)

**Ejecución:**

```bash
cd Ansible/ejemplo2
ansible-playbook -i inventario.ini playbook5.yaml
ansible-playbook -i inventario.ini playbook6.yaml
```

**Documentación completa:** Ver `Ansible/ejemplo2/README.md`

---

#### 6.3 Configuración SSH para dispositivos con version de SSH antigua

**Ubicación:** `Ansible/ssh-config/`

**Contenido:**

- `config`: Archivo de configuración SSH
  - Configuraciones por host
  - Opciones de conexión optimizadas
  - Reutilizado por Netmiko y Ansible

---

## Tecnologías y Herramientas

### Lenguajes y Formatos

- **Python 3.12+**: Lenguaje principal
- **YAML**: Modelado de datos y configuración
- **JSON**: Intercambio de datos y esquemas
- **Jinja2**: Templates para generación de configuraciones

### Librerías Python

- **Netmiko 4.6.0+**: Conexiones SSH a dispositivos de red
- **Ansible 12.2.0+**: Automatización de infraestructura
- **Jinja2 3.1.6+**: Motor de templates
- **PyYAML 6.0.3+**: Procesamiento de YAML
- **jsonschema 4.25.1+**: Validación de datos
- **TextFSM**: Parsing de salidas de comandos
- **CiscoConfParse**: Análisis de configuraciones Cisco

### Colecciones Ansible urlizadas

- `cisco.ios`: Módulos para Cisco IOS
- `ansible.netcommon`: Módulos comunes de red
- `ansible.utils`: Utilidades (validación, filtros)

### Plataformas

- **Cisco IOS**: Switches y routers Cisco
- **SSH**: Protocolo de conexión
- **GNS3/EVE-NG**: Entornos de laboratorio (opcional)

---

## Instalación y Configuración

### Prerrequisitos

- Python 3.12 o superior
- Git
- Acceso SSH a dispositivos de red (o simuladores)

### Instalación

```bash
# Clonar el repositorio
git clone https://github.com/escrimaglia/UTN-IaC.git
cd UTN-IaC
```

### Configuración de Ansible

```bash
# Instalar Ansible
uv add ansible

# Instalar colecciones necesarias
ansible-galaxy collection install cisco.ios
ansible-galaxy collection install ansible.netcommon
ansible-galaxy collection install ansible.utils
```

### Configuración de Dispositivos

1. **Editar credenciales** en archivos de configuración:
   - `Netmiko/*/datos_device.py`
   - `Ansible/*/inventario.ini`
   - `Ansible/*/host_vars/*.yaml`

2. **Configurar SSH**: Editar `Ansible/ssh-config/config` con tus dispositivos

3. **Validar conectividad**:

   ```bash
   # Con Ansible
   ansible -i inventario.ini all -m ping
   
   # Con SSH directo
   ssh netsim@<ip_dispositivo>
   ```

---

## Guía de Uso

### Ingresar el entorno virtual correspondiente

### Ejecutar Ejemplos de Python

```bash
# Fundamentos
cd "Python Basics"
python main.py

# JSON
cd json
python manage_json.py

# YAML
cd yaml
python manage_yaml.py
```

### Validar Modelos de Datos

```bash
cd Modelado
python main_schema.py modelo_datos.yaml modelo_schema.json
python main_reutilizacion.py reutilizacion_a.yaml
```

### Ejecutar Scripts Netmiko

```bash
# Ejemplo básico
cd Netmiko/ejemplo1
python integrador1.py

# Con templates
cd ../ejemplo2
python integrador2.py

# Caso completo
cd ../sim_caso
python main.py
```

### Ejecutar Playbooks Ansible

```bash
# Ejemplo 1 - Variables
cd Ansible/ejemplo1
ansible-playbook -i inventario.ini playbook1.yaml
ansible-playbook -i inventario.ini playbook2.yaml -v

# Ejemplo 2 - Estructuras de control
cd ../ejemplo2
ansible-playbook -i inventario.ini playbook5.yaml
ansible-playbook -i inventario.ini playbook6.yaml

# Modo check (dry-run)
ansible-playbook -i inventario.ini playbook1.yaml --check

# Limitar a hosts específicos
ansible-playbook -i inventario.ini playbook1.yaml --limit SW-Bld_A
```

---

## Progresión del Aprendizaje

### Nivel 1: Fundamentos

1. `Python Basics/` - Sintaxis y POO
2. `json/` - Serialización de datos
3. `yaml/` - Configuración estructurada

### Nivel 2: Modelado

1. `Modelado/` - Estructuras de datos y validación

### Nivel 3: Automatización Básica

1. `Netmiko/ejemplo1/` - Conexiones SSH y comandos
2. `Ansible/ejemplo1/` - Playbooks básicos

### Nivel 4: Automatización Intermedia

1. `Netmiko/ejemplo2/` - Templates Jinja2
2. `Ansible/ejemplo2/` - Estructuras de control

### Nivel 5: Soluciones Profesionales

1. `Netmiko/sim_caso/` - Sistema completo de automatización

---

## Mejores Prácticas Implementadas

### 1. Separación de Datos y Lógica

- Modelos de datos en archivos YAML separados
- Templates Jinja2 para configuraciones
- Credenciales en variables de inventario

### 2. Validación de Datos

- JSON Schema para todos los modelos
- Validación antes de aplicar configuraciones
- Verificación de errores en salidas

### 3. Código Reutilizable

- Clases modulares y bien documentadas
- Tareas Ansible incluibles
- Templates parametrizados

### 4. Manejo Robusto de Errores

- Try/except en todas las conexiones
- Block/rescue en Ansible
- Fail-fast ante errores críticos

### 5. Documentación

- README.md en cada proyecto
- Comentarios en código
- Ejemplos de uso

### 6. Versionado

- Uso de Git para control de versiones
- `.gitignore` apropiado
- Metadatos con versión en modelos

### 7. Seguridad

- No hardcodear credenciales
- Uso de Ansible Vault (recomendado en producción)
- SSH con configuración segura

---

## Troubleshooting

### Problemas Comunes

#### 1. Error de conexión SSH

```
NetmikoTimeoutException: TCP connection to device failed
```

**Solución:**

- Verificar conectividad: `ping <ip_dispositivo>`
- Verificar que SSH esté habilitado en el dispositivo
- Revisar configuración de firewall

#### 2. Error de autenticación

```
NetmikoAuthenticationException: Authentication failed
```

**Solución:**

- Verificar credenciales en archivos de configuración
- Verificar que el usuario tenga permisos
- Revisar `ssh-config` si se usa

#### 3. Ansible no encuentra módulos

```
ERROR! couldn't resolve module/action 'cisco.ios.ios_command'
```

**Solución:**

```bash
ansible-galaxy collection install cisco.ios
ansible-galaxy collection list
```

#### 4. Error de validación JSON Schema

```
ValidationError: 'X' is a required property
```

**Solución:**

- Revisar el modelo YAML contra el schema
- Verificar campos requeridos
- Validar tipos de datos

#### 5. Template Jinja2 no encontrado

```
TemplateNotFound: vlans.j2
```

**Solución:**

- Verificar que el archivo existe en `templates/`
- Revisar el path en el código
- Verificar permisos de lectura

---

## Extensiones Futuras

### Funcionalidades Planeadas

- [ ] Soporte para más vendors (Juniper, Arista)
- [ ] Integración con APIs REST
- [ ] Backup automático de configuraciones
- [ ] Rollback de configuraciones
- [ ] Dashboard web de monitoreo
- [ ] CI/CD con GitHub Actions
- [ ] Contenedores Docker para entornos
- [ ] Tests unitarios y de integración

### Mejoras Planificadas

- [ ] Paralelización de configuraciones
- [ ] Métricas y telemetría
- [ ] Logging avanzado
- [ ] Integración con sistemas de ticketing
- [ ] Notificaciones (email, Slack)
- [ ] Documentación interactiva

---

## Referencias y Recursos

### Documentación Oficial

- [Ansible Documentation](https://docs.ansible.com/)
- [Netmiko Documentation](https://github.com/ktbyers/netmiko)
- [Jinja2 Documentation](https://jinja.palletsprojects.com/)
- [JSON Schema](https://json-schema.org/)
- [PyYAML Documentation](https://pyyaml.org/)

### Colecciones Ansible

- [Cisco IOS Collection](https://galaxy.ansible.com/cisco/ios)
- [Network Common Collection](https://galaxy.ansible.com/ansible/netcommon)
- [Ansible Utils](https://galaxy.ansible.com/ansible/utils)

### Herramientas Relacionadas

- [TextFSM Templates](https://github.com/networktocode/ntc-templates)
- [CiscoConfParse](https://github.com/mpenning/ciscoconfparse)

---

## Autor

### Ed Scrimaglia

- Profesor en UTN Cisco Academy
- Network Automation Engineer
- GitHub: [@escrimaglia](https://github.com/escrimaglia)

---

## Licencia

Este proyecto es de código abierto y está disponible para fines educativos.

---

## Agradecimientos

- Universidad Tecnológica Nacional (UTN) - Facultad Regional Córdoba
- Comunidad de Network Automation
- Contribuidores de librerías open source

---

**Última actualización:** 28 de noviembre de 2025
