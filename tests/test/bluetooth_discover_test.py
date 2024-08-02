import bluetooth

nearby_devices = bluetooth.discover_devices(lookup_names=True)

print(f"Found {len(nearby_devices)} devices")

for addr, name in nearby_devices:
	print(f"	{addr} - {name}")
