import time
import requests
import paramiko
from scp import SCPClient
import os

class SCPConnection:
    def __init__(self, hostname,username,password):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.ssh = None
        self.scp = None
        self.connect()
    
    def connect(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.load_system_host_keys()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(self.hostname, username=self.username, password=self.password, compress=True)
        self.scp = SCPClient(self.ssh.get_transport())
        
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
    
    def get_file(self, remote_path, local_path):
        try:
            self.scp.get(remote_path,local_path)
            print(f"File {remote_path} copied to {local_path}")
        except Exception as e:
            print(f"Failed to establish SCP connection: {e}")
            
    def make_directory(self, directory):
        stdin, stdout, stderr = self.ssh.exec_command(f'mkdir -p {directory}')
        exit_status = stdout.channel.recv_exit_status()
        print(f"Stdout: {stdout.read().decode()}")
        if exit_status != 0:
            print(f"Error creating directory {directory}: {stderr.read().decode()}")


remote_framecast_dir = "/home/rpi0w/Desktop/FrameCast"
local_framecast_dir = os.path.dirname(__file__)
#agent_controller_dir = os.path.join(agent_framecast_dir,'..','controller')
#principal_controller_dir = os.path.join(principal_framecast_dir,'..','controller')
#agent_wireless_dir = os.path.join(agent_dir,'..','wireless')
#principal_wireless_dir = os.path.join(principal_dir,'..','wireless')
#web_dir = os.path.join(agent_dir,'..','web')
#top_dir = os.path.join(current_dir,'..')

files = [
    #'run.py',
    #'controller/frame_controller.py'
    #'controller/logo.jpg',
    'wireless/bluetooth_connection.py'
    #'wireless/wifi_connection.py',
    #'web/web_server.py'

]

directories = [
    'controller',
    'controller/displayed_photo',
    'wireless'
    'web'
]

def distribute_files():
    
    for filepath in files:
        remote_filepath = os.path.join(remote_framecast_dir,filepath)
        local_filepath = os.path.join(local_framecast_dir,filepath)
        print(f"Sending local file {local_filepath} to {remote_filepath}")
        scp_connection.send_file(local_filepath, remote_filepath)
    
    
def retrieve_files():
    
    for filepath in files:
        remote_filepath = os.path.join(remote_framecast_dir,filepath)
        local_filepath = os.path.join(local_framecast_dir,filepath)
        scp_connection.get_file(remote_filepath,local_filepath)

if __name__ == '__main__':
    
    scp_connection = SCPConnection("172.20.10.9","rpi0w","raspberry")
    scp_connection.connect()
    distribute_files()
    scp_connection.close()
    

            
        



