import threading
import time
import requests
import socket

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Unreachable ID address to force socket open
        s.connect(('10.254.254.254',1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    
    return IP

def check_dns_map(ip):
	
	ip_mapped = False
	config_line = f"address=/framecast.local/{ip}"
	with open("/etc/dnsmasq.conf","r") as file:
		lines = file.readlines()
		for line in lines:
			if config_line in line:
				ip_mapped = True
	
	return ip_mapped
    
def run_principal_manager():
	
	while True:
		
		current_ip = get_ip_address()
		print(current_ip)
		if not check_dns_map(current_ip):
			url = f"http://{current_ip}:5000/api/update_dns"
			try:
				response = requests.get(url)
				print(response)
			except requests.exceptions.RequestException as e:
				print("Error making API call:", e)
		
		time.sleep(5)	
			
if __name__ == '__main__':
	run_principal_manager()		
			
		
    
		
		
		
