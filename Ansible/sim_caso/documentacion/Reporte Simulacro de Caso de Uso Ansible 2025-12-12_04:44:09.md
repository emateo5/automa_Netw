# Reporte de automatizacion de configuraciones de red

## Servicio: Simulacro de Caso de Uso Ansible

Date: 2025-12-12 -  Time: 04:44:08  
User: netsim

### Network Automation Engineer - UTN-FRC
...............................................................................................

# Device - SW-Bld_A

## Configuraciónes interfaces tipo Access

### hostname: SW-Bld_A

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
...............................................................................................

# Device - SW-Bld_B

## Configuraciónes interfaces tipo Access

### hostname: SW-Bld_B

```
!
interface GigabitEthernet1/1
 description Conexion a PC_ING_2
 switchport mode access
 switchport access vlan 10
!
interface GigabitEthernet1/2
 description Conexion a PC_PROD_2
 switchport mode access
 switchport access vlan 20
!
```
...............................................................................................

# Device - SW-Data_Center

## Configuraciónes interfaces tipo Access

### hostname: SW-Data_Center

```
!
interface GigabitEthernet1/1
 description Conexion a Servidor_WEB
 switchport mode access
 switchport access vlan 30
!
```
...............................................................................................

# Device - SW-Bld_A

## Configuraciónes interfaces tipo Trunks

### hostname: SW-Bld_A

```
!
interface GigabitEthernet0/1
 description Conexion a SW_CORE_1
 switchport trunk encapsulation dot1q
 switchport mode dynamic auto
 switchport trunk allowed vlan 10,20
!
interface GigabitEthernet0/2
 description Conexion a SW_CORE_2
 switchport trunk encapsulation dot1q
 switchport mode dynamic auto
 switchport trunk allowed vlan 10,20
!
```
...............................................................................................

# Device - SW-Bld_B

## Configuraciónes interfaces tipo Trunks

### hostname: SW-Bld_B

```
!
interface GigabitEthernet0/1
 description Conexion a SW_CORE_1
 switchport trunk encapsulation dot1q
 switchport mode dynamic auto
 switchport trunk allowed vlan 10,20
!
interface GigabitEthernet0/2
 description Conexion a SW_CORE_2
 switchport trunk encapsulation dot1q
 switchport mode dynamic auto
 switchport trunk allowed vlan 10,20
!
```
...............................................................................................

# Device - SW-CORE_1

## Configuraciónes interfaces tipo Trunks

### hostname: SW-CORE_1

```
!
interface GigabitEthernet0/1
 description Conexion a SW-Bld_A
 switchport trunk encapsulation dot1q
 switchport mode dynamic desirable
 switchport trunk allowed vlan 10,20,30
!
interface GigabitEthernet0/2
 description Conexion a SW-Bld_B
 switchport trunk encapsulation dot1q
 switchport mode dynamic desirable
 switchport trunk allowed vlan 10,20,30
!
interface GigabitEthernet0/3
 description Conexion a SW-Data_Center
 switchport trunk encapsulation dot1q
 switchport mode dynamic desirable
 switchport trunk allowed vlan 10,20,30
!
```
...............................................................................................

# Device - SW-CORE_2

## Configuraciónes interfaces tipo Trunks

### hostname: SW-CORE_2

```
!
interface GigabitEthernet0/1
 description Conexion a SW-Bld_B
 switchport trunk encapsulation dot1q
 switchport mode dynamic desirable
 switchport trunk allowed vlan 10,20,30
!
interface GigabitEthernet0/2
 description Conexion a SW-Bld_A
 switchport trunk encapsulation dot1q
 switchport mode dynamic desirable
 switchport trunk allowed vlan 10,20,30
!
interface GigabitEthernet0/3
 description Conexion a SW-Data_Center
 switchport trunk encapsulation dot1q
 switchport mode dynamic desirable
 switchport trunk allowed vlan 10,20,30
!
```
...............................................................................................

# Device - SW-Data_Center

## Configuraciónes interfaces tipo Trunks

### hostname: SW-Data_Center

```
!
interface GigabitEthernet0/1
 description Conexion a SW-CORE_1
 switchport trunk encapsulation dot1q
 switchport mode dynamic auto
 switchport trunk allowed vlan 30
!
interface GigabitEthernet0/2
 description Conexion a SW-CORE_2
 switchport trunk encapsulation dot1q
 switchport mode dynamic auto
 switchport trunk allowed vlan 30
!
```
...............................................................................................

# Device - SW-Bld_A

## Configuraciónes de VLANs

### hostname: SW-Bld_A

```
!
vlan 10
 name Ingenieria
!
vlan 20
 name Produccion
!
```
...............................................................................................

# Device - SW-Bld_B

## Configuraciónes de VLANs

### hostname: SW-Bld_B

```
!
vlan 10
 name Ingenieria
!
vlan 20
 name Produccion
!
```
...............................................................................................

# Device - SW-CORE_1

## Configuraciónes de VLANs

### hostname: SW-CORE_1

```
!
vlan 10
 name Ingenieria
!
vlan 20
 name Produccion
!
vlan 30
 name Finanzas
!
```
...............................................................................................

# Device - SW-CORE_2

## Configuraciónes de VLANs

### hostname: SW-CORE_2

```
!
vlan 10
 name Ingenieria
!
vlan 20
 name Produccion
!
vlan 30
 name Finanzas
!
```
...............................................................................................

# Device - SW-Data_Center

## Configuraciónes de VLANs

### hostname: SW-Data_Center

```
!
vlan 30
 name Finanzas
!
```
...............................................................................................

...............................................................................................
