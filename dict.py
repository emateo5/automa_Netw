devices = {
    "routers": [
        {
            'name': "R1",
            'ip': "10.1.0.1",
            'mask': "255.255.255.0",
            'vendor': "Cisco",
            'model': 2911,
            'location': {'rack': "1", 'position': "1"},
            'activo': True
        },
        {
            'name': "R2",
            'ip': "10.1.0.2",
            'mask': "255.255.255.0",
            'vendor': "Cisco",
            'model': 2909,
            'location': {'rack': "1", 'position': "2"},
            'activo': False
        },
        {
            'name': "R3",
            'ip': "10.1.0.3",
            'mask': "255.255.255.0",
            'vendor': "Cisco",
            'model': 2907,
            'location': {'rack': "1", 'position': "3"},
            'activo': True
        }
    ]
}

print ("Diccionario: ", devices)

print ("Routers: ", devices["routers"])

print ("Primer Router: ", devices.get("routers", "No hay routers")[0].get("name", "No hay nombre"))


dic2 = {}
dic2["key1"] = devices.get("routers", "No hay routers")[0].get("name", "No hay nombre")
dic2["key2"] = devices.get("routers", "No hay routers")[0].get("ip", "No hay IP")

print ("Diccionario 2: ", dic2)
