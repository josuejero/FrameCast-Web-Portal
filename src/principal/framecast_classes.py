from enum import Enum
import json
import os
import sys
import requests

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
device_config_path = os.path.join(parent_dir,'device_config.json')
photo_config_path = os.path.join(parent_dir,'photo_config.json')
photo_library_path = os.path.join(parent_dir,'photo_library')

import_dir = os.path.join(parent_dir,'principal')
sys.path.append(import_dir)

from scp_connection_manager import PersistentSCPConnection, is_host_alive, send_file_to_host

# New DPF objects are UNASSIGNED until given a type based on the discovered device name
class DeviceType(Enum):
    UNASSIGNED = "Unassigned"
    PRINCIPAL = "Principal"
    AGENT = "Agent"

# Core definitions for the DPF class including connection and file transfer functions.
class DigitalPhotoFrame:
    def __init__(self, mac_address, host_name, serial_number, device_type):
        self.mac_address = mac_address
        self.host_name = host_name
        self.serial_number = serial_number
        self.device_type = device_type
        self.name = f"My New Device (S/N: {serial_number})"
        self.ip_address = "0.0.0.0"
        self.connected = False
        self.photo_list = []
        self.update_freq = 15
        self.randomize = True
        
        self.last_photo_update = 0
        self.photo_order = 0
        self.scp_connection = None
    
    # Initiates a GET request to an Agent's HTTP server heartbeat route to establish the Agent is running and not just present on the network.
    def test_connection(self):
        
        return is_host_alive(self.ip_address)
    
    # Sets up the persistent SCP connection. Since the SCP connection takes several seconds, the connection is maintained.
    def connect_to_frame(self):
    
        # The user and password must configured to be the values below on each Agent device.
        print(f"Connection parameters in connect_to_frame:\n{self.ip_address} rpi0w raspberry")
        self.scp_connection = PersistentSCPConnection(self.ip_address,"rpi0w","raspberry")
        return self.scp_connection.connect()
    
    # Sends photo to an Agent if an SCP connection was set up.
    def send_photo_to_frame(self, photo_filepath):
        
        current_status = self.connected
        if self.test_connection():
            if not self.connected or self.scp_connection is None:
                self.connected = self.connect_to_frame()
            if self.connected:
                self.connected = send_file_to_host(self.scp_connection, photo_filepath)
        else:
            self.connected = False
            
        if current_status != self.connected:
            data = {
                'Host Name': self.host_name,
                'Connected': self.connected
            }
            update_device_connection_status(data)
            #response = requests.post('http://localhost:5000/api/update_connection_status',json=data)
            #print('POST response:', response.json())
        
        return self.connected

    
    def set_mac_address(self, mac_address):
        self.mac_address = mac_address
    
    def set_serial_number(self, serial_number):
        self.serial_number = serial_number
        
    def set_name(self, name):
        self.name = name
    
    def set_type(self, device_type):
        self.device_type = device_type
        
    def set_ip_address(self, ip_address):
        self.ip_address = ip_address
    
    def set_connected(self, connected):
        self.connected = connected
    
    def set_photo_list(self, photo_list):
        self.photo_list = photo_list
    
    def set_update_frequency(self, update_freq):
        self.update_freq = update_freq
    
    def set_randomize(self, randomize):
        self.randomize = randomize
    
    # This is used to construct the JSON config string.
    def get_object_dict(self):
        return {
            'MAC Address': self.mac_address,
            'Host Name': self.host_name,
            'Serial Number': self.serial_number,
            'Name': self.name,
            'Type': self.device_type.value,
            'IP Address': self.ip_address,
            'Connected': self.connected,
            'Update Frequency': self.update_freq,
            'Randomize': self.randomize,
            'Photo List': self.photo_list
        }
    
    # This is used to configure a DPF object based on the JSON config.
    @classmethod
    def set_object_from_dict(cls, data):
        
        #photo_list = [DigitalPhoto.set_object_from_dict(photo) for photo in data['Photo List']]
        device_type = DeviceType(data['Type'])
        
        frame = cls(
            mac_address=data['MAC Address'],
            host_name=data['Host Name'],
            serial_number = data['Serial Number'],
            device_type = device_type
        )
    
        #frame.set_serial_number(data['Serial Number'])
        frame.set_name(data['Name'])
        #frame.set_type(device_type)
        frame.set_ip_address(data['IP Address'])
        frame.set_connected(data['Connected'])
        frame.set_update_frequency(data['Update Frequency'])
        frame.set_randomize(data['Randomize'])
        frame.set_photo_list(data['Photo List'])
        
        return frame
      
    # This is only used for simulating a DPF collection by manually instantiating DP objects.
    def add_photo(self, photo):
        self.photo_list.append(photo)
        
# Defines the portion of the unedited photo to be displayed on the LCD.
class PhotoViewWindow:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def set_x(self, x):
        this.x=x
    
    def set_y(self, y):
        this.x=x
        
    @classmethod
    def set_object_from_dict(cls, data):
        
        window = cls(x=data['x'],y=data['y'])
        
        return window
    
    def get_object_dict(self):
        return {
            'x': self.x,
            'y': self.y,
        }
        
class DigitalPhoto:
    def __init__(self, unique_id):
        self.unique_id = unique_id
        self.name = unique_id
        self.rotation = 0
        self.scaling = 100
        self.window = PhotoViewWindow(0,0)
        
    def set_name(self, name):
        self.name = name
    
    def get_name(self):
        return self.name
    
    def set_rotation(self, rotation):
        self.rotation = rotation
    
    def set_scaling(self, scaling):
        self.scaling = scaling
    
    def get_scaling(self):
        return self.scaling
    
    def set_window(self, window):
        self.window = PhotoViewWindow.set_object_from_dict(window)
        
    def get_object_dict(self):
        
        return {
            'Unique ID': self.unique_id,
            'Name': self.name,
            'Rotation': self.rotation,
            'Scaling': self.scaling,
            'Window': self.window.get_object_dict()
        }
    
    @classmethod
    def set_object_from_dict(cls, data):
        
        photo = cls(unique_id=data['Unique ID'])
        
        photo.set_name(data['Name'])
        photo.set_rotation(data['Rotation'])
        photo.set_scaling(data['Scaling'])
        photo.set_window(data['Window'])
        
        return photo

digital_photo_frame_collection = []
digital_photo_collection = []

'''def write_test(photo_config_file, device_config_file):
    
    frame1 = DigitalPhotoFrame("ABC", "Frame1")
    frame2 = DigitalPhotoFrame("DEF", "Frame2")
    photo1 = DigitalPhoto("1")
    photo2 = DigitalPhoto("2")
    photo3 = DigitalPhoto("3")
    
    digital_photo_frame_collection.append(frame1)
    digital_photo_frame_collection.append(frame2)
    digital_photo_collection.append(photo1)
    digital_photo_collection.append(photo2)
    digital_photo_collection.append(photo3)
     
    json_device_dict = [frame.get_object_dict() for frame in digital_photo_frame_collection]
    json_photo_dict = [photo.get_object_dict() for photo in digital_photo_collection]
    json_device_string = json.dumps(json_device_dict, indent=4)
    json_photo_string = json.dumps(json_photo_dict, indent=4)
        
    print(json_device_string)
    print(json_photo_string)
    
    with open(photo_config_file, 'w') as file:
        file.write(json_photo_string)
    
    with open(device_config_file, 'w') as file:
        file.write(json_device_string)'''

def save_device_collection():
    
    json_device_string = json_parse_device_collection()
    
    with open(device_config_path, 'w') as file:
        file.write(json_device_string)
    
def save_photo_collection():
    
    json_photo_string = json_parse_photo_collection()
    
    with open(photo_config_path, 'w') as file:
        file.write(json_photo_string)

'''def get_simulated_collection():
    
    frame1 = DigitalPhotoFrame("ABC", "Frame1")
    frame2 = DigitalPhotoFrame("DEF", "Frame2")
    photo1 = DigitalPhoto("1")
    photo2 = DigitalPhoto("2")
    photo3 = DigitalPhoto("3")
    
    digital_photo_frame_collection.append(frame1)
    digital_photo_frame_collection.append(frame2)
    digital_photo_collection.append(photo1)
    digital_photo_collection.append(photo2)
    digital_photo_collection.append(photo3)
        
    return digital_photo_frame_collection'''

def json_parse_device_collection():
    
    json_dict = [frame.get_object_dict() for frame in digital_photo_frame_collection]
    json_string = json.dumps(json_dict, indent=4)
    
    return json_string
    
def json_parse_photo_collection():
    
    json_dict = [photo.get_object_dict() for photo in digital_photo_collection]
    json_string = json.dumps(json_dict, indent=4)
    
    return json_string
        
'''def read_test(filename):
    
    with open(filename,'r') as file:
        json_string = file.read()
    
    print(json_string)
    
    build_collection_from_json(json_string)
    
    #json_dict = json.loads(json_string)
     
    #digital_photo_frame_collection = [DigitalPhotoFrame.set_object_from_dict(frame) for frame in json_dict]
    
    #json_parse_device_collection(digital_photo_frame_collection)'''

def build_device_collection_from_json(json_string):
    
    json_dict = json.loads(json_string)
    global digital_photo_frame_collection
    digital_photo_frame_collection = [DigitalPhotoFrame.set_object_from_dict(frame) for frame in json_dict]
    #print(json_parse_device_collection())
    
def build_photo_collection_from_json(json_string):
    
    json_dict = json.loads(json_string)
    global digital_photo_collection
    digital_photo_collection = [DigitalPhoto.set_object_from_dict(photo) for photo in json_dict]
    #print(json_parse_photo_collection(digital_photo_collection))
    
def get_device_config(file_path):
    
    if os.path.exists(file_path):
        with open(file_path,'r') as file:
            json_string = file.read()
            print(json_string)
            build_device_collection_from_json(json_string)
            return json_string
    else:
        print("Config file not found")
        return ''

def get_photo_config(file_path):
    
    if os.path.exists(file_path):
        with open(file_path,'r') as file:
            json_string = file.read()
            print(json_string)
            build_photo_collection_from_json(json_string)
            return json_string
    else:
        print("Config file not found")
        return ''
    
def get_device_collection(file_path):
    
    print_module_id()
    
    if os.path.exists(file_path):
        with open(file_path,'r') as file:
            json_string = file.read()
            print(f"JSON string after reading file during get_device_collection\n{json_string}")
    else:
        print("Config file not found")
        return digital_photo_frame_collection
    
    #json_dict = json.loads(json_string)
    
    #return [DigitalPhotoFrame.set_object_from_dict(frame) for frame in json_dict]
    
    build_device_collection_from_json(json_string)
    print(f"DPF collection after reading file during get_device_collection\n{digital_photo_frame_collection}")
    
    return digital_photo_frame_collection

def get_photo_collection(file_path):
    
    if os.path.exists(file_path):
        with open(file_path,'r') as file:
            json_string = file.read()
            print(json_string)
    else:
        print("Config file not found")
        return null
    
    #json_dict = json.loads(json_string)
    
    #return [DigitalPhoto.set_object_from_dict(photo) for photo in json_dict]
    
    build_photo_collection_from_json(json_string)
    
    return digital_photo_collection

# Called whenever web portal has an update
def update_device(data):
    
    index = data["Device Index"]
    print(index)
    print(len(digital_photo_frame_collection))
    
    if index != -1 and len(digital_photo_frame_collection) != 0:
        digital_photo_frame_collection[index].set_name(data["Device Name"])
        digital_photo_frame_collection[index].set_update_frequency(data["Update Frequency"])
        digital_photo_frame_collection[index].set_randomize(data["Randomize"])
        digital_photo_frame_collection[index].set_photo_list(data["Photo List"])
        print (digital_photo_frame_collection[index])
        
        save_device_collection()
    
    return json_parse_device_collection()

def update_photo(data):
    
    index = data["Photo Index"]
    print(index)
    print(len(digital_photo_collection))
    
    if index != -1 and len(digital_photo_collection) != 0:
        digital_photo_collection[index].set_window(data["Window"])
        digital_photo_collection[index].set_scaling((int)(data["Scaling"]))
        print (digital_photo_collection[index])
        
        save_photo_collection()
    
    return json_parse_photo_collection()
    
'''def get_single_photo_config(photo_name):

    for photo in digital_photo_collection:
        print(photo.get_name())
        if photo.get_name() == photo_name:
            return photo
            
    return null'''

def add_new_devices(discovered_devices):
    
    for discovered_device in discovered_devices:
        mac_address = discovered_device["MAC Address"]
        host_name = discovered_device["Host Name"]
        serial_number = discovered_device["Serial Number"]
        device_type = discovered_device["Type"]
        match = False
        for existing_device in digital_photo_frame_collection:
            if existing_device.host_name == host_name:
                match = True
                break
        if not match:
            new_device = DigitalPhotoFrame(
                mac_address,
                host_name,
                serial_number,
                DeviceType.PRINCIPAL if device_type == "Principal" else DeviceType.AGENT
            )
            digital_photo_frame_collection.append(new_device)
    
    save_device_collection()
    
    return json_parse_device_collection()

def remove_devices(devices_to_delete):
    
    print_module_id()
    print(f"Devices_to_delete when entering remove_devices:\n{devices_to_delete}")
    print(f"DPF Collection when entering remove_devices:\n{digital_photo_frame_collection}")
    for device_to_delete in devices_to_delete:
        index = 0
        for existing_device in digital_photo_frame_collection:
            if existing_device.host_name == device_to_delete["Host Name"]:
                print(f"Device to delete:\n{digital_photo_frame_collection[index]}")
                del digital_photo_frame_collection[index]
                break
            index += 1
    
    save_device_collection()
    
    return json_parse_device_collection()

def remove_photos(photos_to_delete):
    
    print_module_id()
    print(f"Devices_to_delete when entering remove_photos:\n{photos_to_delete}")
    print(f"DP Collection when entering remove_photos:\n{digital_photo_collection}")
    for photo_to_delete in photos_to_delete:
        index = 0
        for existing_photo in digital_photo_collection:
            if existing_photo.name == photo_to_delete:
                #print(f"Photo to delete:\n{digital_photo_collection[index]}")
                del digital_photo_collection[index]
                photo_filepath = os.path.join(photo_library_path,photo_to_delete)
                print(f"Photo file path to delete:\n{photo_filepath}")
                if os.path.exists(photo_filepath):
                    os.remove(photo_filepath)
                break
            index += 1
    
    save_photo_collection()
    
    return json_parse_photo_collection()
    
def get_connection_status(networked_devices):
    
    print_module_id()
    
    print(f"DPF Collection when entering get_connection_status:\n{digital_photo_frame_collection}")
    for existing_device in digital_photo_frame_collection:
        match = False
        for networked_device in networked_devices:
            if existing_device.host_name == networked_device["Host Name"]:
                #existing_device.set_connected(True)
                existing_device.set_mac_address(networked_device["MAC Address"])
                existing_device.set_ip_address(networked_device["IP Address"])
                match = True
                break
        #if not match:
            #existing_device.set_connected(False)
    
    save_device_collection()
    
    return json_parse_device_collection()

def update_device_connection_status(data):
    
    print_module_id()
    
    print(f"DPF Collection when entering update_device_connection_status:\n{digital_photo_frame_collection}")
    print_module_id()
    for existing_device in digital_photo_frame_collection:
        if existing_device.host_name == data['Host Name']:
            existing_device.set_connected(data['Connected'])
            break
    
    save_device_collection()
    
    return json_parse_device_collection()

def update_devices_from_mobile(device_config):
    
    device = json.loads(device_config)
    print(device)
    #for device in device_config:
    mac_address = device["MAC Address"]
    host_name = device["Host Name"]
    serial_number = device["Serial Number"]
    device_type = DeviceType.PRINCIPAL if device["Type"] == "Principal" else DeviceType.AGENT
    match = False
    for existing_device in digital_photo_frame_collection:
        if existing_device.host_name == host_name:
            match = True
            existing_device.set_name(device["Name"])
            existing_device.set_ip_address(device["IP Address"])
            existing_device.set_connected(device["Connected"])
            existing_device.set_photo_list(device["Photo List"])
            existing_device.set_update_frequency(device["Update Frequency"])
            existing_device.set_randomize(device["Randomize"])
            break
    if not match:
        new_device = DigitalPhotoFrame(
            mac_address,
            host_name,
            serial_number,
            DeviceType.PRINCIPAL if device_type == "Principal" else DeviceType.AGENT
        )
        new_device.set_name(device["Name"])
        new_device.set_ip_address(device["IP Address"])
        new_device.set_connected(device["Connected"])
        new_device.set_photo_list(device["Photo List"])
        new_device.set_update_frequency(device["Update Frequency"])
        new_device.set_randomize(device["Randomize"])
        digital_photo_frame_collection.append(new_device)
    
    save_device_collection()
    
    return json_parse_device_collection()
    
def update_photos_from_mobile(photo_config):
    
    for photo in photo_config:
        unique_id = photo["Unique ID"]
        match = False
        for existing_photo in digital_photo_collection:
            if existing_photo.unique_id == unique_id:
                match = True
                existing_photo.set_name(photo["Name"])
                existing_photo.set_scaling(photo["Scaling"])
                existing_photo.set_rotation(photo["Rotation"])
                existing_photo.set_window(photo["Window"])
                break
        if not match:
            new_photo = DigitalPhoto(
                unique_id
            )
            existing_photo.set_name(photo["Name"])
            existing_photo.set_scaling(photo["Scaling"])
            existing_photo.set_rotation(photo["Rotation"])
            existing_photo.set_window(photo["Window"])
            digital_photo_collection.append(new_photo)
    
    save_photo_collection()
    
    return json_parse_photo_collection()

def add_new_photos(photo_names):
    
    print("Initial call of add_new_photos function:")
    print(digital_photo_collection)
    
    for photo in photo_names:
        match = False
        for existing_photo in digital_photo_collection:
            if existing_photo.unique_id == photo:
                match = True
                break
        if not match:
            new_photo = DigitalPhoto(photo)
            digital_photo_collection.append(new_photo)
    
    save_photo_collection()
    
    return json_parse_photo_collection()

#For debugging purposes only
def print_module_id():

    print(f"Module memory ID: {id(__import__(__name__))}")

if __name__ == '__main__':
    #write_test('jsonPhotoConfigTest.json','jsonDeviceConfigTest.json')
    read_test('jsonDeviceConfigTest.json')
    
        
    
    
