import bluetooth
import os
import subprocess

if os.geteuid() != 0:
	print("This script must be run as root")
	exit(1)

# Set socket to listen for bluetooth connection from app or web portal
server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

port = 1
server_socket.bind(("", port))

server_socket.listen(1)
port = server_socket.getsockname()[1]

server_socket.settimeout(180)

# Advertise service with UUID for bluetooth connection from app
bluetooth.advertise_service(server_socket, "Pi4Server",
							service_id = "00001101-0000-1000-8000-00805F9B34FB",
							service_classes = ["00001101-0000-1000-8000-00805F9B34FB", bluetooth.SERIAL_PORT_CLASS],
							profiles = [bluetooth.SERIAL_PORT_PROFILE])
							
print("Bluetooth service advertised. Waiting for connection...")							

try:
	# Get socket and address from device trying to connect
	client_socket, address = server_socket.accept()
except bluetooth.BluetoothError as e:
	print("No connection was made within the timeout period")
	server_socket.close()
	exit(1)

ssid = None
psk = None

try:

	# Read wifi credential info sent from connected device
	data = client_socket.recv(1024).decode('utf-8')
	if len(data) == 0:
		exit
	recieved_data = data.split("/n")

	ssid = recieved_data[0]
	psk = recieved_data[1]

except OSError:
	pass

print(f"WIFI: {ssid} {psk}")

client_socket.close()
server_socket.close()



