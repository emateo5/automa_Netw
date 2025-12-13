# Proyecto Ansible - Automatización de Configuración de Red Cisco IOS

**Autor:** Ed Scrimaglia  
**Versión:** 1.0  
**Fecha de Creación:** 12 de Dic de 2025  
**Proyecto:** Ansible Vault example project

## Descripción del Proyecto

Este proyecto implementa una solución completa de automatización de red utilizando Ansible para gestionar dispositivos Cisco IOS. El proyecto sigue un enfoque de **Infrastructure as Code (IaC)** y utiliza **Ansible Vault** para el manejo seguro de credenciales.

### Características Principales

- Configuración automatizada de interfaces de acceso en switches Cisco
- Gestión segura de credenciales con Ansible Vault
- Generación de configuraciones mediante templates Jinja2
- Modelo de datos centralizado para toda la infraestructura

## Arquitectura de Red

El proyecto gestiona una infraestructura de red que incluye:

### Dispositivos Gestionados

| Dispositivo | IP Management | Grupo | Función |
|------------|--------------|--------|---------|
| SW-Bld_A | 10.2.0.10X | cisco_ios_access_bsas | Switch de Acceso - Edificio A |
| SW-Bld_B | 10.2.0.10X | cisco_ios_access_cba | Switch de Acceso - Edificio B |
| SW-Data_Center | 10.2.0.10X | cisco_ios_datacenter | Switch Data Center |
| SW-CORE_1 | 10.2.0.10X | cisco_ios_core | Switch Core Principal |
| SW-CORE_2 | 10.2.0.10X | cisco_ios_core | Switch Core Secundario |

### VLANs Configuradas

| VLAN ID | Nombre | Gateway | Uso |
|---------|--------|---------|-----|
| 10 | Ingenieria | 192.168.10.254 | Usuarios departamento Ingeniería |
| 20 | Produccion | 192.168.20.254 | Usuarios departamento Producción |
| 30 | Finanzas | 192.168.30.254 | Servidores y usuarios Finanzas |

## Estructura del Proyecto

```
ejemplo4/
├── README.md                          # Este archivo
├── pyproject.toml                     # Dependencias del proyecto (Python/Ansible)
│
├── inventario/
│   └── inventario.ini                 # Inventario de dispositivos de red
│
├── group_vars/
│   └── cisco_ios/
│       └── vault.yaml                 # Credenciales encriptadas con Ansible Vault
│
├── modelo/
│   └── modelo.yaml                    # Modelo de datos de la infraestructura
│
├── templates/
│   └── inter_access_cfg.j2            # Template Jinja2 para interfaces de acceso
│
├── configs/                           # Archivos de configuración generados
│   ├── SW-Bld_A_int_access.cfg
│   └── SW-Bld_B_int_access.cfg
│
└── playbooks/ (en raíz del proyecto)
    ├── .vault-pass                    # Contraseña del vault (¡NO VERSIONAR!)
    ├── play_create_codigo.yaml        # Playbook para generar configuraciones
    └── play_config_devices.yaml       # Playbook para aplicar configuraciones
```

## Componentes Principales

### 1. Inventario (`inventario/inventario.ini`)

Define todos los dispositivos de red organizados por grupos y sus variables de conexión:

- **Grupos de switches:**
  - `cisco_ios_access_bsas` - Switches de acceso en Buenos Aires
  - `cisco_ios_access_cba` - Switches de acceso en Córdoba
  - `cisco_ios_core` - Switches del core de red
  - `cisco_ios_datacenter` - Switches del datacenter

- **Variables globales:**
  - Conexión: `ansible.netcommon.network_cli`
  - Usuario: `netsim`
  - Network OS: `cisco.ios.ios`
  - Autenticación: Contraseña (sin clave pública SSH)

### 2. Ansible Vault (`group_vars/cisco_ios/vault.yaml`)

Almacena credenciales encriptadas para el grupo `cisco_ios`:

```yaml
ansible_password: [ENCRIPTADO]
ansible_become_password: [ENCRIPTADO]
```

**Comando para ver el contenido:**

```bash
ansible-vault view group_vars/cisco_ios/vault.yaml --vault-password-file .vault-pass
```

### 3. Modelo de Datos (`modelo/modelo.yaml`)

Archivo centralizado que define toda la infraestructura de red usando el patrón **Source of Truth**:

**Estructura:**

- **Metadatos:** Información del proyecto
- **hosts_groups:** Mapeo de grupos de hosts
- **infra_spec.devices:** Especificación detallada de cada dispositivo
  - Management (IP, interface)
  - Interfaces físicas y SVIs
  - VLANs
  - Routing (para switches core)

**Características:**

- Utiliza YAML anchors (`&`) y aliases (`<<: *`) para reutilización de configuraciones
- Define plantillas de interfaces: `int_trunk_access`, `int_trunk_core`, `int_access`, `int_svi`

### 4. Template Jinja2 (`templates/inter_access_cfg.j2`)

Template que genera configuración de interfaces de acceso para Cisco IOS:

```jinja
!
{% for interface in interfaces -%}
{% if interface.mode == "access" -%}
interface {{ interface.name }}
  description {{ interface.description }}
  switchport mode {{ interface.mode }}
  switchport access vlan {{ interface.vlan }}
!
{% endif -%}
{% endfor -%}
```

**Salida generada** (ejemplo para SW-Bld_A):

```
!
interface GigabitEthernet1/1
  description Conexion a PC_ING_1
  switchport mode access
  switchport access vlan 10
!
interface GigabitEthernet1/2
  description Conexion a PC_PROD_1
  switchport mode access
  switchport access vlan 20
!
```

## Playbooks

### Playbook 1: `play_create_codigo.yaml`

**Propósito:** Genera archivos de configuración desde templates Jinja2

**Proceso:**

1. Lee el modelo de datos de `modelo/modelo.yaml`
2. Ejecuta sobre el grupo `cisco_ios` (switches de acceso)
3. Extrae las interfaces del dispositivo del modelo
4. Renderiza el template `inter_access_cfg.j2`
5. Guarda el resultado en `configs/{{ hostname }}_int_access.cfg`

**Uso:**

```bash
ansible-playbook ansible-playbook -i inventario/inventario.ini ./play_create_codigo.yaml --vault-password-file ./.vault-pass
```

**Salida:**

- `configs/SW-Bld_A_int_access.cfg`
- `configs/SW-Bld_B_int_access.cfg`

### Playbook 2: `play_config_devices.yaml`

**Propósito:** Aplica las configuraciones generadas a los dispositivos reales

**Proceso:**

1. Lee el modelo de datos de `modelo/modelo.yaml`
2. Ejecuta sobre el grupo `cisco_ios`
3. Lee el archivo de configuración generado para cada dispositivo
4. Aplica la configuración usando el módulo `cisco.ios.ios_config`
5. Si hay cambios, ejecuta el handler para guardar la configuración

**Características:**

- Requiere autenticación mediante Ansible Vault
- Solo guarda si hay cambios (handler condicional)
- Conexión segura por SSH con autenticación por contraseña

## Guía de Uso

1. **Archivo `.vault-pass`** en el directorio raíz con la contraseña del vault

### Workflow Completo

#### Paso 1: Generar Configuraciones

```bash
ansible-playbook -i inventario/inventario.ini ./play_create_codigo.yaml --vault-password-file ./.vault-pass
```

**Verifica la salida:**

```bash
cat configs/SW-Bld_A_int_access.cfg
cat configs/SW-Bld_B_int_access.cfg
```

#### Paso 2: Aplicar Configuraciones a Dispositivos

```bash
aansible-playbook -i inventario/inventario.ini ./play_config_devices.yaml --vault-password-file ./.vault-pass
```

### Verificación del Inventario

```bash
# Listar todos los hosts
ansible-inventory -i ./inventario/inventario.ini --list --vault-password-file .vault-pass

# Ver variables de un host específico (con vault desencriptado)
ansible-inventory -i ./inventario/inventario.ini \
  --host SW-Bld_A \
  --vault-password-file .vault-pass
```

## Gestión de Ansible Vault

### Crear archivo vault

```bash
ansible-vault create group_vars/cisco_ios/vault.yaml --vault-password-file .vault-pass
```

### Editar archivo vault

```bash
ansible-vault edit group_vars/cisco_ios/vault.yaml --vault-password-file .vault-pass
```

### Ver contenido del vault

```bash
ansible-vault view group_vars/cisco_ios/vault.yaml --vault-password-file .vault-pass
```

### Cambiar contraseña del vault

```bash
ansible-vault rekey group_vars/cisco_ios/vault.yaml
```

### Contenido esperado del vault

```yaml
ansible_password: password
ansible_become_password: password
```

## Troubleshooting

### Problema 1: Error de autenticación SSH

**Error:**

```txt
Failed to authenticate public key: Access denied for 'publickey'
```

**Solución:**
Asegúrate de que en `inventario.ini` está configurado:

```ini
[cisco_ios:vars]
ansible_ssh_common_args="-o PubkeyAuthentication=no -o PreferredAuthentications=password"
```

### Problema 2: Variables del vault no se cargan

**Error:** Ansible no puede conectarse, credenciales no encontradas

**Solución:**
Ejecuta los playbooks desde el **directorio raíz del proyecto**, no desde subdirectorios:

```bash
cd /path/to/ejemplo4
ansible-playbook play_config_devices.yaml -i inventario/inventario.ini --vault-password-file .vault-pass
```

### Problema 3: Archivo vault-pass no encontrado

**Error:**

```txt
ERROR! The vault password file ./.vault-pass was not found
```

**Solución:**
Crea el archivo `.vault-pass` con la contraseña:

```bash
echo "tu_contraseña_vault" > .vault-pass
chmod 600 .vault-pass
```

### Problema 4: Módulo cisco.ios no encontrado

**Error:**

```text
ERROR! couldn't resolve module/action 'cisco.ios.ios_config'
```

**Solución:**

```bash
ansible-galaxy collection install cisco.ios
```

## Mejores Prácticas Implementadas

### 1. Infrastructure as Code (IaC)

- Toda la configuración de red está definida en código
- Versionable con Git
- Reproducible en cualquier entorno

### 2. Separación de Datos y Lógica

- Modelo de datos centralizado (`modelo.yaml`)
- Templates reutilizables (`inter_access_cfg.j2`)
- Playbooks simples y legibles

### 3. Seguridad

- Credenciales encriptadas con Ansible Vault
- Archivo `.vault-pass` no versionado (añadir a `.gitignore`)
- Autenticación por contraseña sin claves SSH expuestas

### 4. Idempotencia

- Los playbooks pueden ejecutarse múltiples veces sin efectos adversos
- Solo se guardan cambios si hay modificaciones

### 5. DRY (Don't Repeat Yourself)

- Uso de YAML anchors y aliases para reutilización
- Templates Jinja2 para generación de código
- Variables centralizadas

## Flujo de Trabajo del Proyecto

```
┌──────────────────┐
│  modelo.yaml     │  ← Source of Truth
│  (Datos)         │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Template Jinja2  │
│ (Lógica)         │
└────────┬─────────┘
         │
         ▼ play_create_codigo.yaml
┌──────────────────┐
│ Configs/*.cfg    │  ← Configuraciones generadas
└────────┬─────────┘
         │
         ▼ play_config_devices.yaml
┌──────────────────┐
│ Dispositivos     │  ← Switches Cisco IOS
│ de Red           │
└──────────────────┘
```

## Referencias

- [Ansible Documentation](https://docs.ansible.com/)
- [Cisco IOS Collection](https://galaxy.ansible.com/cisco/ios)
- [Ansible Vault Guide](https://docs.ansible.com/ansible/latest/user_guide/vault.html)
- [Jinja2 Templates](https://jinja.palletsprojects.com/)

## Licencia

Proyecto educativo - UTN-FRC Academia Cisco - Network Automation Engineer Course

---

**Última actualización**: Diciembre 2025
