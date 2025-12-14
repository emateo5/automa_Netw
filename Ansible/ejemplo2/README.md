# Proyecto de Automatización de Redes con Ansible

**Autor:** Ed Scrimaglia  
**Proyecto:** Estructuras de Programación - Ansible  
**Versión:** 1.0  
**Fecha de Creación:** 28 de noviembre de 2025

## Descripción General

Este proyecto es una colección de playbooks de Ansible diseñados para automatizar la configuración y gestión de dispositivos de red Cisco IOS. El proyecto demuestra diferentes conceptos y técnicas de Ansible aplicadas a la automatización de redes, incluyendo:

- Estructuras condicionales
- Manejo de variables y hostvars
- Loops e iteraciones
- Manejo de errores con block/rescue
- Validación de modelos de datos con JSON Schema
- Gestión de configuraciones mediante modelo de datos centralizado

## Estructura del Proyecto

```tree
.
├── README.md                      # Este archivo
├── inventario.ini                 # Inventario de dispositivos de red
├── pyproject.toml                 # Configuración del proyecto Python
├── cfg/
│   └── ansible.cfg               # Configuración de Ansible
├── modelo_datos/
│   └── modelo_datos.yaml         # Modelo de datos centralizado
├── json_files/
│   └── validador_modelo.json     # Esquema JSON para validación
├── tasks/
│   ├── validate.yaml             # Tarea reutilizable de validación
│   └── timestamp.yaml            # Tarea para obtener timestamp
└── playbooks:
    ├── playbook1.yaml            # Condicionales básicas
    ├── playbook2.yaml            # Hostvars y variables compartidas
    ├── playbook3.yaml            # Loops con modelo de datos
    ├── playbook4.yaml            # Loops con lista estática
    ├── playbook5.yaml            # Manejo de errores (block/rescue)
    └── playbook6.yaml            # Validación con JSON Schema
```

## Configuración del Entorno

### Archivo de Configuración (`cfg/ansible.cfg`)

```ini
[defaults]
transport = ssh
timeout = 30
forks = 10
host_key_checking = False
deprecation_warnings = False

[ssh_connection]
ssh_args = -o ControlMaster=auto -o ControlPersist=60s
pipelining = True
```

**Características clave:**

- Conexiones persistentes para mejorar el rendimiento
- Pipelining habilitado para reducir overhead
- Verificación de host_key deshabilitada para entornos de laboratorio

### Inventario (`inventario.ini`)

El inventario define cuatro grupos de dispositivos Cisco IOS:

- **cisco_ios_access_bsas**: Switch de acceso Buenos Aires (SW-Bld_A)
- **cisco_ios_access_cba**: Switch de acceso Córdoba (SW-Bld_B)
- **cisco_ios_datacenter**: Switch de datacenter (SW-Data_Center)
- **cisco_ios_core**: Switch core (SW-CORE_1)
- **cisco_ios**: Grupo padre que incluye todos los switches de acceso y datacenter

**Credenciales:**

- Usuario: `netsim`
- Password: `****`
- Network OS: `cisco.ios.ios`
- Método de escalada: `ansible.netcommon.enable`

## Modelo de Datos

### Estructura del Modelo (`modelo_datos/modelo_datos.yaml`)

El modelo de datos centralizado contiene:

#### Metadatos

```yaml
metadatos:
  proyecto: "Estructuras de programación de Ansible"
  version: "1.0"
  autor: "Ed Scrimaglia"
  fecha_creacion: "2025-11-28"
  time_zone: "America/Argentina/Buenos_Aires"
```

#### Especificación de Infraestructura

- **hosts_group**: Grupo de hosts objetivo (cisco_ios)
- **devices**: Lista de dispositivos con:
  - Hostname y dirección de gestión
  - Parámetros de conexión
  - Configuración de interfaces (trunk/access)
  - VLANs configuradas
  - Especificaciones de configuración (templates y archivos)

### Validación del Modelo (`json_files/validador_modelo.json`)

Esquema JSON que valida:

- **Metadatos:** proyecto, versión, autor, fecha de creación, zona horaria
- **Infraestructura:**
  - Direcciones IP (IPv4/IPv6)
  - Interfaces con modos (access/trunk)
  - VLANs (rango 1-4094)
  - Credenciales de conexión

## Playbooks

### Playbook 1: Estructuras Condicionales (`playbook1.yaml`)

**Propósito:** Demostrar el uso de condicionales básicas en Ansible.

**Características:**

- Ejecuta comandos solo cuando `ejecuta = true`
- Valida la versión del modelo de datos (`version == '1.0'`)
- Obtiene el estado de interfaces IP con `show ip interface brief`
- Registra la salida y la muestra condicionalmente

**Variables:**

- `ejecuta`: Booleano para controlar la ejecución
- `device`: Nombre del dispositivo objetivo

**Ejecución:**

```bash
ansible-playbook -i inventario.ini playbook1.yaml
```

---

### Playbook 2: Hostvars y Variables Compartidas (`playbook2.yaml`)

**Propósito:** Demostrar el uso de `hostvars` para compartir variables entre hosts.

**Flujo:**

1. **Play 1 (localhost):** Define variables desde el modelo de datos
   - version
   - autor
   - fecha_de_creacion
   - zona_horaria

2. **Play 2 (cisco_ios):** Consume las variables de localhost usando `hostvars['localhost']`
   - Ejecuta comandos solo si la versión coincide
   - Muestra la salida de interfaces

**Concepto clave:** Las variables definidas en un host pueden ser accedidas por otros hosts mediante `hostvars`.

**Ejecución:**

```bash
ansible-playbook -i inventario.ini playbook2.yaml
```

---

### Playbook 3: Loops con Modelo de Datos (`playbook3.yaml`)

**Propósito:** Iterar sobre estructuras complejas del modelo de datos.

**Características:**

- Carga la lista de dispositivos desde el modelo
- Itera sobre cada dispositivo usando `loop`
- Muestra las interfaces de cada dispositivo
- Usa `loop_control` con `label` para simplificar la salida

**Ventaja:** Permite trabajar con datos estructurados y complejos de manera eficiente.

**Ejecución:**

```bash
ansible-playbook -i inventario.ini playbook3.yaml
```

---

### Playbook 4: Loops con Lista Estática (`playbook4.yaml`)

**Propósito:** Demostrar iteración sobre una lista simple y estática.

**Características:**

- Define una lista de dispositivos directamente en el playbook
- Itera sobre cada elemento
- Muestra un mensaje personalizado por cada dispositivo

**Dispositivos en el loop:**

- Router-1
- SW-Bld_A
- SW-Bld_B
- SW-Data_Center
- SW-CORE_1

**Ejecución:**

```bash
ansible-playbook -i inventario.ini playbook4.yaml
```

---

### Playbook 5: Manejo de Errores (`playbook5.yaml`)

**Propósito:** Implementar manejo robusto de errores con `block/rescue/always`.

**Estructura:**

- **Block:** Intenta ejecutar comandos en los dispositivos
  - Obtiene interfaces con `show ip interface brief`
  - Imprime el resultado
  
- **Rescue:** Se ejecuta si hay un error
  - Muestra mensaje de error de conexión
  - Sugiere verificar conectividad y credenciales
  
- **Always:** Se ejecuta siempre
  - Muestra mensaje de finalización
  - Útil para limpieza o logging

**Ventaja:** Garantiza que los errores de conexión no detengan toda la ejecución.

**Ejecución:**

```bash
ansible-playbook -i inventario.ini playbook5.yaml
```

---

### Playbook 6: Validación con JSON Schema (`playbook6.yaml`)

**Propósito:** Validar el modelo de datos contra un esquema JSON antes de usarlo.

**Características:**

- Define rutas al modelo de datos y al esquema
- Incluye la tarea reutilizable `tasks/validate.yaml`
- Valida estructura, tipos de datos y restricciones

**Variables:**

- `modelo_datos_path`: Ruta al archivo YAML del modelo
- `schema_path`: Ruta al esquema JSON de validación

**Proceso de validación:**

1. Carga el modelo de datos YAML
2. Carga el esquema JSON
3. Valida usando `ansible.utils.validate` con motor `jsonschema`
4. Muestra el resultado de la validación

**Ejecución:**

```bash
ansible-playbook -i inventario.ini playbook6.yaml
```

## Tareas Reutilizables

### `tasks/validate.yaml`

Tarea modular para validar modelos de datos contra esquemas JSON.

**Entrada:**

- `modelo_datos_path`: Ruta al archivo YAML
- `schema_path`: Ruta al esquema JSON

**Proceso:**

1. Lee el archivo YAML y lo convierte a objeto
2. Lee el esquema JSON
3. Valida usando el motor `ansible.utils.jsonschema`
4. Registra el resultado en `validation_result`

**Ventaja:** Puede ser incluida en múltiples playbooks sin duplicar código.

---

### `tasks/timestamp.yaml`

Obtiene timestamps en diferentes zonas horarias.

**Funcionalidad:**

- Obtiene fecha/hora UTC
- Obtiene fecha/hora en la zona horaria del modelo
- Usa variables de entorno (`TZ`)
- Delega ejecución a localhost

**Variables requeridas:**

- `model.metadatos.time_zone`: Zona horaria del proyecto

## Guía de Uso

### Prerrequisitos

1. **Colecciones de Ansible:**

   ```bash
   ansible-galaxy collection install cisco.ios
   ansible-galaxy collection install ansible.utils
   ansible-galaxy collection install ansible.netcommon
   ```

2. **Conectividad de red:**
   - Acceso SSH a los dispositivos definidos en el inventario
   - Credenciales correctas configuradas

### Ejecución de Playbooks

**Ejecutar un playbook específico:**

```bash
ansible-playbook -i inventario.ini playbook1.yaml
```

**Ejecutar con verbosidad:**

```bash
ansible-playbook -i inventario.ini playbook1.yaml -v
```

**Ejecutar en modo check (dry-run):**

```bash
ansible-playbook -i inventario.ini playbook1.yaml --check
```

**Ejecutar solo en hosts específicos:**

```bash
ansible-playbook -i inventario.ini playbook1.yaml --limit SW-Bld_A
```

### Validación del Modelo de Datos

Antes de ejecutar cualquier playbook de configuración, es recomendable validar el modelo:

```bash
ansible-playbook -i inventario.ini playbook6.yaml
```

## Conceptos de Ansible Demostrados

### 1. **Variables y Facts**

- Variables locales (`vars`)
- Variables desde archivos (`vars_files`)
- Variables compartidas entre hosts (`hostvars`)
- Variables de inventario

### 2. **Estructuras Condicionales**

- Condición simple: `when: ejecuta`
- Condiciones compuestas: `when: ejecuta and modelo.metadatos.version == '1.0'`
- Uso de `hostvars` en condiciones

### 3. **Loops e Iteraciones**

- Loop simple sobre listas estáticas
- Loop sobre estructuras complejas del modelo
- Control de salida con `loop_control` y `label`

### 4. **Manejo de Errores**

- Bloques `block/rescue/always`
- Registro de salidas con `register`
- Mensajes de error personalizados

### 5. **Validación de Datos**

- Validación con JSON Schema
- Motor `ansible.utils.jsonschema`
- Conversión de formatos (`from_yaml`, `from_json`)

### 6. **Reutilización de Código**

- Tareas incluibles con `include_tasks`
- Separación de lógica en archivos independientes
- Modelo de datos centralizado

### 7. **Módulos de Red**

- `cisco.ios.ios_command`: Ejecutar comandos en dispositivos Cisco
- Registro y visualización de salidas
- Conexión mediante `network_cli`

## Mejores Prácticas Implementadas

1. **Separación de datos y lógica:** Modelo de datos centralizado
2. **Validación de datos:** JSON Schema para garantizar integridad
3. **Código reutilizable:** Tareas en directorio `tasks/`
4. **Manejo de errores:** Bloques rescue para robustez
5. **Documentación:** Comentarios en cada playbook y tarea
6. **Organización:** Estructura de directorios clara
7. **Versionado:** Metadatos con versión y autor

## Troubleshooting

### Error de conexión SSH

Si ves errores de conexión, verifica:

```bash
# Probar conectividad
ping 10.2.0.10X

# Probar SSH manual
ssh netsim@10.2.0.10X

# Verificar credenciales en inventario
ansible-inventory -i inventario.ini --list
```

### Error de validación del modelo

Si la validación falla:

1. Verifica la sintaxis YAML del modelo
2. Revisa los requisitos del esquema JSON
3. Ejecuta solo la validación para ver detalles:

   ```bash
   ansible-playbook -i inventario.ini playbook6.yaml -v
   ```

### Colecciones faltantes

Si Ansible no encuentra módulos:

```bash
# Listar colecciones instaladas
ansible-galaxy collection list

# Instalar colecciones faltantes
ansible-galaxy collection install cisco.ios ansible.utils ansible.netcommon
```

## Referencias

- [Documentación oficial de Ansible](https://docs.ansible.com/)
- [Cisco IOS Collection](https://galaxy.ansible.com/cisco/ios)
- [Ansible Network Automation](https://docs.ansible.com/ansible/latest/network/index.html)
- [JSON Schema](https://json-schema.org/)

## Licencia

Proyecto educativo - UTN-FRC Academia Cisco - Network Automation Engineer Course

---

**Última actualización**: Diciembre 2025
