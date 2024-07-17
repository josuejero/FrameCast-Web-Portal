import time
import os
import shutil
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

if __name__ == '__main__':

	sys.path.insert(0,parent_dir)
	run_agent_manager()	

from principal.framecast_classes import DigitalPhoto, DigitalPhotoFrame, DeviceType, PhotoViewWindow
from principal.framecast_classes import get_device_collection, get_photo_collection
from principal.photo_formatter import format_for_display

device_config_path = os.path.join(parent_dir,'device_config.json')
photo_config_path = os.path.join(parent_dir,'photo_config.json')
#print(parent_dir)
photo_library_path = os.path.join(parent_dir, 'photo_library')
#print(photo_library_path)
displayed_photo_path = os.path.join(parent_dir,'controller','displayed_photo','next.jpg')
formatted_photo_path = os.path.join(parent_dir,'principal','formatted_photos')

def run_agent_manager():
		
	frame_collection = get_device_collection(device_config_path)
	photo_collection = get_photo_collection(photo_config_path)
	last_device_config_mod_time = get_file_modification_time(device_config_path)
	last_photo_config_mod_time = get_file_modification_time(photo_config_path)
	
	while True:
		
		#Check config file for updates
		current_device_config_mod_time = get_file_modification_time(device_config_path)
		current_photo_config_mod_time = get_file_modification_time(photo_config_path)
		
		if current_device_config_mod_time != last_device_config_mod_time:
			print("Device Config Updated")
			last_device_config_mod_time = current_device_config_mod_time
			frame_collection = get_device_collection(device_config_path)
			
		if current_photo_config_mod_time != last_photo_config_mod_time:
			print("Photo Config Updated")
			last_photo_config_mod_time = current_photo_config_mod_time
			photo_collection = get_photo_collection(photo_config_path)
			
		
		current_time = time.time()
		for frame in frame_collection:
			if current_time - frame.last_photo_update > frame.update_freq:
				photo_name = frame.photo_list[frame.photo_order]
				
				next_photo = next((photo for photo in photo_collection if photo.name == photo_name), None)
				
				original_file_path = os.path.join(photo_library_path,next_photo.name)
				print(original_file_path)
				formatted_file_path = os.path.join(formatted_photo_path,next_photo.name)
				format_for_display(next_photo, original_file_path, formatted_file_path)			
				
				if frame.device_type == DeviceType.PRINCIPAL:				
					shutil.copy2(formatted_file_path,displayed_photo_path)
					os.remove(formatted_file_path)
				elif frame.device_type == DeviceType.AGENT:	
					print(frame.ip_address)									
					if frame.test_connection():					
						frame.connect_to_frame()
						if frame.send_photo_to_frame(formatted_file_path):
							os.remove(formatted_file_path)
							
				if frame.photo_order < len(frame.photo_list)-1:
					frame.photo_order = frame.photo_order + 1
				else:
					frame.photo_order = 0				
				
				frame.last_photo_update = current_time
				
				#print(next_photo.name)

		#print(current_time)
		time.sleep(1)

def get_file_modification_time(file_path):
	return os.path.getmtime(file_path)
		
	
			
