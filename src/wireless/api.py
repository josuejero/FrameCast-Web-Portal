from bluetooth_manager import BluetoothManager
from wifi_manager import WifiManager

class DigitalPhotoFrameAPI:
    @staticmethod
    def find_discoverable_bluetooth_devices():
        return BluetoothManager.find_discoverable_bluetooth_devices()

    @staticmethod
    def invite_discovered_devices_to_network(discovered_devices):
        return BluetoothManager.invite_discovered_device_to_network(discovered_devices)

    @staticmethod
    def enumerate_wifi_devices():
        return WifiManager.enumerate_wifi_devices()
