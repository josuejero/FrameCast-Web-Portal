import subprocess
import socket
from zeroconf import ServiceBrowser, Zeroconf
from typing import Dict


def get_self_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Unreachable ID address to force socket open
        s.connect(('10.254.254.254',1))
        ip_address = s.getsockname()[0]
    except Exception:
        ip_address = '127.0.0.1'
    finally:
        s.close()

    return ip_address

# This class handles wifi scanning and hostname lookups to check for DFP devices connected to the network
class WifiManager:
     
    # Ping network to ensure mDNS devices appear in ARP table to grab MAC Address
    @staticmethod
    def ping_device(ip):
        subprocess.run(['ping', '-c','1','-W','1',ip], stdout=subprocess.DEVNULL)
    
    # Get arp table to find ip and mac addresses
    @staticmethod
    def get_arp_table():
        result = subprocess.run(['arp', '-a'], capture_output=True, text=True)
        return result.stdout

    # Find mDNS services on network and get hostnames from devices, avahi-daemon must be running on rpi to register
    # hostname with mDNS service
    @staticmethod
    def get_hostname_from_mdns(timeout=5) -> Dict[str, str]:

        # Handles service discovery events
        class MyListener:
            def __init__(self):
                self.devices = {}

            # Place holder
            def remove_service(self, zeroconf, type, name):
                pass
            
            # Place holder
            def update_service(self, zeroconf, type, name):
                pass

            # Get detailed information about the service, extract hostname, check if DPF device and add to device
            # dictionary
            def add_service(self, zeroconf, type, name):
                info = zeroconf.get_service_info(type, name)
                #print(f"add_service info:\n{info}")
                if info:
                    # Convert ip address to string
                    if info.addresses:
                        address = socket.inet_ntoa(info.addresses[0])
                        # Extracting the hostname without domain
                        hostname = info.server.split('.')[0]
                        if 'FrameCast' in hostname:
                            self.devices[address] = hostname
                    else:
                        info = zeroconf.get_service_info(type, name)
                        if info:
                            # Convert ip address to string
                            if info.addresses:
                                address = socket.inet_ntoa(info.addresses[0])
                                # Extracting the hostname without domain
                                hostname = info.server.split('.')[0]
                                if 'FrameCast' in hostname:
                                    self.devices[address] = hostname

            def get_devices(self):
                return self.devices

        # Initialize zeroconf and a mylistener to handle discovery events, and start looking for services on the network
        zeroconf = Zeroconf()
        listener = MyListener()
        browser = ServiceBrowser(zeroconf, "_workstation._tcp.local.", listener)

        # Wait for services to be found, then stop zerconf
        import time
        time.sleep(timeout)

        zeroconf.close()

        # Return device dictionary<key=ip address, value=hostname>
        return listener.get_devices()

    # Look at devices currently connected to network, find the DFP devices, extract info from hostnames and return a
    # map of found DFP objects
    @staticmethod
    def enumerate_wifi_devices():
        
        # Get arp table and hostnames
        
        mdns_hosts = WifiManager.get_hostname_from_mdns()
        print(f"mDNS hosts:\n{mdns_hosts}")
        for ip, hostname in mdns_hosts.items():
            WifiManager.ping_device(ip)
    
        arp_output = WifiManager.get_arp_table()
        print(f"ARP Output:\n{arp_output}")

        # Store connected DFP objects
        # Principal adds self to dictionary since it won't appear in ARP table
        
        self_hostname = socket.gethostname()
        print(f"Self hostname: {self_hostname}")
        self_ip_address = get_self_ip_address()
        
        network_devices = [{
            "MAC Address":"NA",
            "Host Name": self_hostname,
            "IP Address":self_ip_address
            }]
        
        # Parse the ARP table
        for line in arp_output.splitlines():
            #if line.strip() and 'dynamic' in line:
            if line.strip():
                
                parts = line.split()
                print(parts)
                ip_address = parts[1].strip("()")
                mac_address = parts[3]

                # Check if the IP address is in the mDNS hostnames
                if ip_address in mdns_hosts:

                    # Extract hostname and serial number
                    hostname = mdns_hosts[ip_address]
                    device_sn = hostname.split('-')[-1]

                    # Make new dict object
                    deviceConfig = {
                        "MAC Address":mac_address,
                        "Host Name": hostname,
                        "IP Address":ip_address
                    }
                
                    network_devices.append(deviceConfig)

        return network_devices
