import bluetooth
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad
from Cryptodome.Random import get_random_bytes
from base64 import b64encode, b64decode
import subprocess

def encrypt(text, key):
    key_bytes = b64decode(key)
    cipher = AES.new(key_bytes, AES.MODE_ECB)
    encrypted_bytes = cipher.encrypt(pad(text.encode('utf-8'),AES.block_size))
    return b64encode(encrypted_bytes).decode('utf-8')

# Get SSID for currently connected network
def get_ssid():
    try:
        # Run nmcli command to get the active Wi-Fi SSID
        result = subprocess.run(
            ['nmcli', '-t', '-f', 'active,ssid', 'dev', 'wifi'],
            capture_output=True,
            text=True,
            check=True
        )
        # Filter the active connections
        for line in result.stdout.splitlines():
            if line.startswith('yes:'):
                return line.split(':')[1]
        return None
    except subprocess.CalledProcessError as e:
        print(f"Error getting SSID: {e}")
        return None


# Get PSK for currently connected network
def get_password(ssid):
    try:
        # Run nmcli command to get the connection details for the SSID
        result = subprocess.run(
            ['nmcli', '-s', 'connection', 'show', ssid],
            capture_output=True,
            text=True,
            check=True
        )
        # Extract the PSK (password) from the connection details
        for line in result.stdout.splitlines():
            if '802-11-wireless-security.psk:' in line:
                return line.split(':')[1].strip()
        return None
    except subprocess.CalledProcessError as e:
        print(f"Error getting password: {e}")
        return None


# This class handles bluetooth scanning and communication
class BluetoothManager:

    # List nearby DPF devices
    @staticmethod
    def find_discoverable_bluetooth_devices():

        # Scan and store nearby discoverable bluetooth devices
        #nearby_devices = bluetooth.discover_devices(lookup_names=True, device_id=True, flush_cache=True)
        nearby_devices = bluetooth.discover_devices(duration=8,lookup_names=True,flush_cache=True)

        # Found DPF device objects will be stored here
        discovered_devices = []

        # Loop through found bluetooth devices and check for DPF devices, if found make a new DPF object and add it
        # to list
        for addr, name in nearby_devices:

            print(f"{addr} - {name}")
            # Check if DPF device
            if name.startswith("FrameCast"):

                parts = name.split("-")

                # If DPF device found extract info from device name and make new DPF object
                if len(parts) == 4 and (parts[2] == "Principal" or parts[2] == "Agent"):

                    device_sn = parts[3]
                    device_type = parts[2]

                deviceConfig = {
                    "Serial Number":device_sn,
                    "Host Name": name,
                    "Type":device_type,
                    "MAC Address":addr
                };
                
                discovered_devices.append(deviceConfig)

        return discovered_devices

    # Loop through discovered DPF devices and send wifi credentials to each, recieving and actual connection to
    # network will be handled on the DPF device side
    @staticmethod
    def invite_discovered_device_to_network(invited_devices):

        # List to hold values for if a device was connected
        connected_list = []

        # Get wifi credentials from currently connected network
        ssid = get_ssid()
        psk = get_password(ssid)
        secret_key = b64encode(get_random_bytes(16)).decode('utf-8')
        encrypted_password = encrypt(psk,secret_key)
        print(f"SSID: {ssid}\npsk: {psk}\nSecret Key: {secret_key}")

        # Loop through discovered devices, connect over bluetooth and send credentials
        for device in invited_devices:
            
            mac_addr = device["MAC Address"]

            try:
                port = 1  # Commonly used port for Bluetooth communication

                # Setup socket for communication and connect to DFP device.  DFP device must have socket setup to
                # listen, will be handled by script running on DFP device
                sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
                sock.connect((mac_addr, port))

                # Send credentials and wait a bit for DFP devices to connect to network
                sock.send(f"{ssid}/n{encrypted_password}/n{secret_key}")
                sock.settimeout(15)

                # Listen for confirmation of successful connection from DFP devices, if received update connected
                # list with true.  If no confirmation or an error update list with false
                try:
                    confirmation = sock.recv(1024).decode('utf-8').strip()
                    if confirmation == "OK":
                        sock.close()
                        connected_list.append(True)
                    else:
                        sock.close()
                        connected_list.append(False)

                except bluetooth.btcommon.BluetoothError as e:
                    print(f"Failed to receive confirmation from {mac_addr}: {e}")
                    sock.close()
                    connected_list.append(False)
            except bluetooth.BluetoothError as e:
                print(f"Failed to send SSID and password to {mac_addr}: {e}")
                connected_list.append(False)

        return connected_list

