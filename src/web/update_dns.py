import socket
import os

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
    
    print(IP)
    return IP
    
def update_dns(ip):
    ip_mapped = False
    config_line = f"address=/framecast.local/{ip}"
    with open("/etc/dnsmasq.conf","r") as file:
        lines = file.readlines()
    
    with open("/etc/dnsmasq.conf", "w") as file:
        for line in lines:
            print(line)
            if "address=/framecast.local/" in line:
                print("Replacing line...")
                file.write(config_line+"\n")
                ip_mapped = True
            else:
                file.write(line)
        if not ip_mapped:
            print("Adding line...")
            file.write(config_line + "\n")
    
    os.system("sudo systemctl restart dnsmasq")

if __name__ == '__main__':
	update_dns(get_ip_address())
