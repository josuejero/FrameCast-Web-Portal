import time
import requests
import paramiko
from scp import SCPClient

class PersistentSCPConnection:
    def __init__(self, hostname,username,password):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.ssh = None
        self.scp = None
        #self.connect()
    
    def connect(self):
        try:
            self.ssh = paramiko.SSHClient()
            self.ssh.load_system_host_keys()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(self.hostname, username=self.username, password=self.password, compress=True)
            self.scp = SCPClient(self.ssh.get_transport())
            return True
        except Exception as e:
            print(f"Failed to establish SCP connection: {e}")
            return False
        
    def close(self):
        if self.scp:
            self.scp.close()
        if self.ssh:
            self.ssh.close()
            
    def send_file(self, local_path, remote_path):
        try:
            self.scp.put(local_path, remote_path)
            return True
        except Exception as e:
            print(f"Failed to establish SCP connection: {e}")
            return False

file_path = "current.jpg"
destination_path = "/home/rpi0w/Desktop/FrameCast/controller/displayed_photo/next.jpg"

def is_host_alive(hostname):
    try:
        response = requests.get(f"http://{hostname}:5000/heartbeat", timeout=5)
        if response.status_code == 200:
            print(response.text)
            return True
    except requests.RequestException:
        pass
    return False

def send_file_to_host(scp_connection, photo_filepath):
    
    try:
        scp_connection.send_file(photo_filepath, destination_path)
        print("File sent successfully")
        return True
    except Exception as e:
        print("File not sent successfully")
        return False

if __name__ == '__main__':
        
    if is_host_alive("10.0.0.38"):
        print("Host alive")
    else:
        print("Host not alive")
    
    '''print("Checkpoint 1")
    scp_connection = PersistentSCPConnection("172.20.10.9","rpi0w","raspberry")
    print("Checkpoint 2")
    scp_connection.connect()
    print("Checkpoint 3")
    send_file_to_host(scp_connection,file_path)
    print("Checkpoint 4")
    send_file_to_host(scp_connection,file_path)
    print("Checkpoint 5")
    send_file_to_host(scp_connection,file_path)
    print("Checkpoint 6")'''
    

            
        
