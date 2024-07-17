import bluetooth
import os
import subprocess
from base64 import b64decode, b64encode
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import unpad

def decrypt(encrypted_text, key):
	
	encrypted_bytes = b64decode(encrypted_text)
	key_bytes = b64decode(key)
	
	cipher = AES.new(key_bytes, AES.MODE_ECB)
	
	decrypted_bytes = unpad(cipher.decrypt(encrypted_bytes), AES.block_size)
	
	return decrypted_bytes.decode('utf-8')



subprocess.run(['sudo', 'hciconfig', 'hci0', 'up'], check=True)
subprocess.run(['sudo', 'hciconfig', 'hci0', 'piscan'], check=True)
subprocess.run(['sudo', 'btmgmt', 'io-cap', '3'], check=True)

server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

port = 1
server_socket.bind(("", port))
print ("Socket Bound")
server_socket.listen(1)
port = server_socket.getsockname()[1]
print (f"Socket Listening on RFCOMM channel {port}")
print ("Socket: %s" %server_socket)

bluetooth.advertise_service(server_socket, "Pi4Server",
							service_id = "00001101-0000-1000-8000-00805F9B34FB",
							service_classes = ["00001101-0000-1000-8000-00805F9B34FB", bluetooth.SERIAL_PORT_CLASS],
							profiles = [bluetooth.SERIAL_PORT_PROFILE])
							
print ("Service advertised")
client_socket, address = server_socket.accept()
print ("Accepted connection from", address)

ssid = None
psk = None
encrypted_password = None
secret_key = None

try:
	while True:
		data = client_socket.recv(1024).decode('utf-8')
		if len(data) == 0:
			exit
		print(f"Recieved: {data}")
		recieved_data = data.split("/n")
		print(f"Recieved: {recieved_data}")
		
		ssid = recieved_data[0]
		print("SSID: ", ssid)
		encrypted_password = recieved_data[1]
		secret_key = recieved_data[2]
		
		print(encrypted_password)
		print(secret_key)
		if (ssid and encrypted_password and secret_key):
			break
	
except OSError:
	pass

if os.geteuid() != 0:
		print("This script must be run as root")
		exit(1)

psk = decrypt(encrypted_password, secret_key)
print("Decrypted password: ", psk)

try:
		print("connecting...")
		subprocess.run(['nmcli', 'dev', 'wifi', 'connect', ssid, 'password', psk], check=True)
		connected = True

except subprocess.CalledProcessError as e:
		print('Failed to connect')
		connect = False
		exit(1)

if (connected):
	try:
		print("Sending confirmation")
		while True:
			print("Sending ok")
			client_socket.send("OK")
			print("OK Sent")
	except OSError as e:
		print("OSError: ", e)
	except bluetooth.btcomm.BluetoothError as e:
		print("Bluetooth error: ", e)
else:
	try:
		print("Sending Failure")
		while True:
			client_socket.send("FAIL")
			print("Fail sent")
	except OSError:
		pass
	
print("closing sockets")
client_socket.close()
server_socket.close()

subprocess.run(['sudo', 'systemctl', 'restart', 'avahi-daemon'], check=True)

def decrypt(encrypted_text, key):
	
	encrypted_bytes = b64decode(encrypted_text)
	key_bytes = b64decode(key)
	
	cipher = AES.new(key_bytes, AES.MODE_ECB)
	
	decrypted_bytes = unpad(cipher.decrypt(encrypted_bytes), AES.block_size)
	
	return decrypted_bytes.decode('utf-8')



