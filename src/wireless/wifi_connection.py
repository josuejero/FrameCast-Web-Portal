import os
import subprocess
import sys

def main(args):
	
	print("Running wireless script")
	
	if len(args) != 2:
		print("Error: Expected two arguments")
		exit(1)
	if os.geteuid() != 0:
		print("Error: This script must be run as root")
		exit(1)

	ssid = args[0]
	psk = args[1]
	
	print(f"Received arguments: {ssid} and {psk}")
	
	# Run command to connect to wifi network
	try:
			print("Connecting...")
			subprocess.run(['nmcli', 'dev', 'wifi', 'connect', ssid, 'password', psk], check=True)
			#client_socket.send("OK")

	except subprocess.CalledProcessError as e:
			print('Failed to connect')
			#client_socket.send("Failed to connect")
			exit(1)

	#client_socket.close()
	#server_socket.close()

	# Restart avahi-daemon just in case to make sure rpi hostname is advertised so enumerate_wifi_devices can read it
	subprocess.run(['sudo', 'systemctl', 'restart', 'avahi-daemon'], check=True)

if __name__ == '__main__':
	main(sys.argv[1:])




