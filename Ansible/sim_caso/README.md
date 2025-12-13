# Simulacro de Caso de Uso - Ansible Network Automation

**Autor:** Ed Scrimaglia  
**Versión:** 1.0  
**Fecha de Creación:** 12 de Dic de 2025  
**Proyecto:** Simulación Caso de Uso integral

---

## Descripción General

Este proyecto implementa una solución completa de automatización de infraestructura de red utilizando Ansible. El sistema está diseñado para generar configuraciones de dispositivos Cisco IOS de manera automática, aplicarlas a los equipos de red y generar documentación técnica exhaustiva del proceso.

El proyecto sigue el paradigma de **Infraestructura como Código (IaC)**, donde toda la configuración de red se define en un modelo de datos centralizado y se renderiza mediante templates Jinja2, garantizando consistencia, reproducibilidad y trazabilidad en las operaciones de red.

---

## Arquitectura de la Infraestructura

### Topología de Red

La infraestructura simulada incluye:

- **2 Switches Core (SW-CORE_1, SW-CORE_2)**: Switches de núcleo con routing EIGRP y redundancia VRRP
- **2 Switches de Acceso (SW-Bld_A, SW-Bld_B)**: Switches de acceso para edificios A y B
- **1 Switch de Data Center (SW-Data_Center)**: Switch de acceso para el centro de datos

### VLANs Configuradas

- **VLAN 10 - Ingenieria**: Red del departamento de ingeniería (192.168.10.0/24)
- **VLAN 20 - Produccion**: Red del departamento de producción (192.168.20.0/24)
- **VLAN 30 - Finanzas**: Red del departamento de finanzas/data center (192.168.30.0/24)

### Características de Alta Disponibilidad

- **VRRP (Virtual Router Redundancy Protocol)**: Implementado en los switches core para gateway redundante
- **EIGRP (Enhanced Interior Gateway Routing Protocol)**: Protocolo de routing dinámico (AS 10)
- **Trunk Ports**: Enlaces troncales con modos dinámicos para intercambio de VLANs

---

## Estructura del Proyecto

```tree
sim_caso/
├── pyproject.toml                   # Definición del proyecto y dependencias Python
├── README.md                        # Este archivo
├── configs/                         # Configuraciones generadas automáticamente
│   ├── SW-Bld_A_int_access.cfg      # Config de interfaces de acceso
│   ├── SW-Bld_A_int_trunk.cfg       # Config de interfaces troncales
│   ├── SW-Bld_A_vlans.cfg           # Config de VLANs
│   └── ...                          # (Archivos similares por dispositivo)
├── documentacion/                   # Documentación técnica del proyecto
│   ├── Reporte Simulacro...md       # Reporte completo generado
│   └── modulos/                     # Módulos de documentación por componente
├── inventario/                      # Inventario de dispositivos Ansible
│   └── inventario.ini               # Definición de hosts y grupos
├── jsons/                           # Esquemas de validación
│   └── json-schema-model.json       # JSON Schema para validar modelo de datos
├── modelo_datos/                    # Modelo de datos centralizado
│   └── modelo.yaml                  # Definición completa de la infraestructura
├── playbooks/                       # Playbooks de Ansible
│   ├── play_config_devices.yaml     # Aplica configuraciones a dispositivos
│   ├── play_create_codigo.yaml      # Genera configuraciones desde templates
│   └── play_create_documentacion.yaml # Genera documentación del proyecto
├── tasks/                           # Tareas reutilizables
│   ├── task_check_empty_dir.yaml    # Verifica existencia de archivos
│   ├── task_timestamp.yaml          # Obtiene timestamp del sistema
│   └── task_validator.yaml          # Validación de esquemas
└── templates/                       # Templates Jinja2
    ├── eigrp_cfg.j2                 # Template para EIGRP
    ├── inter_access_cfg.j2          # Template para interfaces de acceso
    ├── inter_svi_cfg.j2             # Template para SVIs (Switched Virtual Interfaces)
    ├── inter_trunk_cfg.j2           # Template para interfaces troncales
    ├── vlans_cfg.j2                 # Template para VLANs
    └── *_doc.j2                     # Templates de documentación
```

---

## Componentes Principales

### 1. Modelo de Datos (`modelo_datos/modelo.yaml`)

Archivo YAML centralizado que define toda la infraestructura de red:

- **Metadatos del proyecto**: Nombre, versión, autor, zona horaria
- **Grupos de hosts**: Definición de categorías de dispositivos
- **Especificaciones de infraestructura**: Por cada dispositivo:
  - Interfaces físicas (trunk/access)
  - VLANs
  - SVIs con direccionamiento IP
  - Configuración VRRP
  - Routing EIGRP

**Características destacadas:**

- Uso de **YAML anchors** (`&` y `<<:`) para reutilización de configuraciones comunes
- Definición declarativa de la infraestructura completa
- Separación de configuración de la lógica de implementación

### 2. Templates Jinja2 (`templates/`)

Los templates permiten generar dos tipos de salida:

- **Configuraciones (`.cfg`)**: Código Cisco IOS ejecutable
- **Documentación (`.md`)**: Documentación técnica en Markdown

**Templates disponibles:**

- `inter_trunk_cfg.j2`: Configuración de puertos troncales (802.1Q, DTP)
- `inter_access_cfg.j2`: Configuración de puertos de acceso
- `vlans_cfg.j2`: Creación y nombramiento de VLANs
- `inter_svi_cfg.j2`: Configuración de SVIs con VRRP
- `eigrp_cfg.j2`: Configuración del routing EIGRP

### 3. Playbooks (`playbooks/`)

#### `play_create_codigo.yaml`

Genera todas las configuraciones y documentación desde templates:

- Renderiza templates Jinja2 con datos del modelo
- Crea archivos `.cfg` en directorio `configs/`
- Crea archivos `.md` en directorio `documentacion/modulos/`
- Ejecuta en paralelo para diferentes tipos de dispositivos

#### `play_config_devices.yaml`

Aplica configuraciones a dispositivos reales/simulados:

- Configura interfaces troncales en todos los switches
- Configura interfaces de acceso en switches access/datacenter
- Configura VLANs en todos los switches
- Configura SVIs y VRRP en switches core
- Guarda cambios automáticamente mediante handlers

#### `play_create_documentacion.yaml`

Ensambla documentación técnica completa:

- Genera título del reporte con timestamp
- Ensambla módulos de documentación ordenados
- Crea reporte final con fecha/hora

### 4. Inventario (`inventario/inventario.ini`)

Define hosts y credenciales:

- **Grupos de dispositivos**: cisco_ios, cisco_ios_core, cisco_ios_datacenter
- **Subgrupos**: cisco_ios_access_bsas, cisco_ios_access_cba
- **Variables de conexión**: Credenciales, método de elevación, network_os
- **Direcciones IP de gestión**: Rango 10.2.0.101-105

### 5. Tareas Reutilizables (`tasks/`)

- **`task_timestamp.yaml`**: Obtiene fecha/hora UTC y local con zona horaria configurable
- **`task_check_empty_dir.yaml`**: Verifica existencia de archivos para ensamblaje
- **`task_validator.yaml`**: Valida modelo de datos contra JSON Schema

### 6. JSON Schema (`jsons/json-schema-model.json`)

Esquema de validación que define:

- Estructura obligatoria del modelo de datos
- Tipos de datos permitidos
- Propiedades requeridas vs opcionales
- Validaciones de formato

---

## Uso del Proyecto

### Requisitos Previos

```bash
# Python >= 3.12
# Ansible >= 13.0.0
# ansible-pylibssh >= 1.3.0
```

### Instalación

```bash
# Instalar dependencias con uv
uv sync
```

### Flujo de Trabajo Típico

#### 1. Generar Configuraciones

```bash
cd playbooks
ansible-playbook -i ../inventario/inventario.ini play_create_codigo.yaml
```

Esto generará:

- Archivos `.cfg` en `configs/`
- Archivos `.md` en `documentacion/modulos/`

#### 2. Validar Configuraciones

Revisar los archivos generados en `configs/` antes de aplicar.

#### 3. Aplicar Configuraciones a Dispositivos

```bash
ansible-playbook -i ../inventario/inventario.ini play_config_devices.yaml
```

**Nota**: Requiere conectividad con dispositivos reales o simulador.

#### 4. Generar Documentación

```bash
ansible-playbook -i ../inventario/inventario.ini play_create_documentacion.yaml
```

Crea un reporte consolidado en `documentacion/` con timestamp.

---

## Configuración

### Modificar la Infraestructura

Editar `modelo_datos/modelo.yaml`:

```yaml
devices:
  SW-Nuevo:
    management:
      ip: "10.2.0.106"
      interface: "GigabitEthernet0/0"
    interfaces:
      - name: "GigabitEthernet0/1"
        description: "Conexion a SW-CORE_1"
        mode: trunk
        trunk_mode: auto
        allowed_vlans: 10,20
    vlans:
      - id: 10
        name: "Ingenieria"
```

### Actualizar Inventario

Editar `inventario/inventario.ini`:

```ini
[cisco_ios_nuevo_grupo]
SW-Nuevo ansible_host=10.2.0.106
```

### Crear Nuevos Templates

1. Crear archivo `.j2` en `templates/`
2. Usar sintaxis Jinja2 con acceso a variables del modelo
3. Referenciar en playbooks con bucle para generar cfg y doc

---

## Características Técnicas

### Gestión de Configuración

- **Idempotencia**: Los playbooks pueden ejecutarse múltiples veces sin efectos adversos
- **Handlers**: Guardan configuración solo si hay cambios
- **Templates modulares**: Cada aspecto de configuración es independiente

### Validación de Datos

- JSON Schema para validación estructural
- Separación de datos y lógica (modelo YAML vs templates)

### Generación de Documentación

- Documentación como código
- Sincronización automática entre configuración y documentación
- Reportes con timestamps únicos

### Conectividad

- Uso de `network_cli` connection plugin
- Soporte para elevación de privilegios (enable mode)
- Configuración de credenciales centralizada

---

## Casos de Uso

1. **Provisioning inicial**: Configurar múltiples switches desde cero
2. **Cambios masivos**: Modificar VLANs en toda la infraestructura
3. **Auditoría**: Generar documentación actualizada del estado de red
4. **Disaster Recovery**: Restaurar configuraciones desde modelo de datos
5. **Entornos de desarrollo**: Replicar configuraciones en lab/simuladores

---

## Outputs Generados

### Archivos de Configuración (`.cfg`)

- Sintaxis Cisco IOS nativa
- Listos para copy-paste o `ios_config`
- Separados por función (vlans, trunk, access, svi)

### Documentación (`.md`)

- Formato Markdown legible
- Incluye metadatos y timestamps
- Estructura modular ensamblable

### Reportes Consolidados

- Documento único con toda la configuración
- Nomenclatura con fecha/hora: `Reporte Simulacro de Caso de Uso Ansible 2025-12-12_05:05:56.md`

---

## Mantenimiento y Extensión

### Agregar Nuevo Tipo de Configuración

1. Crear template en `templates/` (ej: `ospf_cfg.j2`)
2. Agregar datos al modelo YAML
3. Crear play en playbook para renderizar template
4. Actualizar JSON Schema si es necesario

### Soportar Otros Vendors

1. Crear templates específicos del vendor
2. Ajustar variables en inventario (`ansible_network_os`)
3. Modificar playbooks para usar módulos apropiados

---

## Consideraciones de Seguridad

- **Credenciales**: Usar Ansible Vault para cifrar passwords
- **Control de versiones**: No commitear credenciales en Git
- **Acceso limitado**: Restringir permisos de ejecución de playbooks
- **Backups**: Realizar respaldo antes de aplicar cambios masivos

---

## Referencias

- [Documentación Ansible](https://docs.ansible.com/)
- [Cisco IOS Collection](https://galaxy.ansible.com/cisco/ios)
- [Jinja2 Templates](https://jinja.palletsprojects.com/)
- [VRRP Protocol RFC 5798](https://tools.ietf.org/html/rfc5798)
- [EIGRP Protocol](https://www.cisco.com/c/en/us/support/docs/ip/enhanced-interior-gateway-routing-protocol-eigrp/16406-eigrp-toc.html)

---

## Licencia

Proyecto educativo - UTN-FRC Academia Cisco - Network Automation Engineer Course

---

**Última actualización**: Diciembre 2025  
