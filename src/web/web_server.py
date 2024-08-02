from flask import Flask, request, jsonify, send_file, render_template, redirect, url_for, send_from_directory
import os
import sys
import socket
import subprocess
import json
import secrets
import string
#import netifaces as ni
#from OpenSSL import SSL

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
device_config_path = os.path.join(parent_dir,'device_config.json')
photo_config_path = os.path.join(parent_dir,'photo_config.json')
principal_dir = os.path.join(parent_dir,'principal')
photo_library_path = os.path.join(parent_dir,'photo_library')
wireless_dir = os.path.join(parent_dir,'wireless')
upate_dns_script_path = os.path.join(current_dir,'update_dns.py')
sys.path.append(principal_dir)
sys.path.append(wireless_dir)

from framecast_classes import json_parse_device_collection, json_parse_photo_collection, build_device_collection_from_json, build_photo_collection_from_json, get_device_config, get_photo_config, update_device, update_photo, add_new_devices, get_connection_status, add_new_photos, update_device_connection_status, update_photos_from_mobile, update_devices_from_mobile, remove_devices, remove_photos
from photo_formatter import format_photo_for_edit_window, format_photo_for_preview
from api import DigitalPhotoFrameAPI

app = Flask(__name__)

# External API calls from mobile app

@app.route('/send_device_config', methods=['POST'])
def receive_device_config():
    #print(request.headers)
    #print(request.data.decode('utf-8'))
    data = request.data.decode('utf-8')
    print(data)
    update_devices_from_mobile(data)
        
    return jsonify({'status':'String received','data':data}), 200
    
@app.route('/send_photo_config', methods=['POST'])
def receive_photo_config():
    data = request.data.decode('utf-8')
    update_photos_from_mobile(data)
        
    return jsonify({'status':'String received','data':data}), 200

@app.route('/send_photo', methods=['POST'])
def receive_image():
    if 'image' not in request.files:
        return jsonify({'status':'No file part'}), 400
    file = request.files['image']
    print(file.filename)
    if file.filename == '':
        return jsonify({'status':'No selected file'}), 400
    photo_path = os.path.join(parent_dir,'photo_library',file.filename)
    file.save(photo_path)
    return jsonify({'status':'Image received','filename':file.filename}), 200

@app.route('/get_device_config', methods=['GET'])
def load_device_config():
    config = get_device_config(device_config_path)
    return config
    
@app.route('/get_photo_config', methods=['GET'])
def load_photo_config():
    config = get_photo_config(photo_config_path)
    return config

@app.route('/get_config', methods=['GET'])
def load_config():
    deviceConfig = json.loads(get_device_config(device_config_path))
    photoConfig = json.loads(get_photo_config(photo_config_path))
    config = {
        "Device Config":deviceConfig,
        "Photo Config":photoConfig
    }
    print(f"Combined config:{json.dumps(config)}")
    return json.dumps(config)

@app.route('/get_photo/<path:filename>', methods=['GET'])
def get_photo(filename):

    photo_path = os.path.join(parent_dir,'photo_library',filename)
    if os.path.exists(image_path):
        return send_file(photo_path,mimetype='image/jpeg')
    else:
        return "Image not found", 404
        
# Start integration
        
@app.route('/')
def index():
    return redirect(url_for('device_manager'))
    
@app.route('/device_manager')
def device_manager():
    return render_template('device_manager.html')
    
@app.route('/device_editor')
def device_editor():
    return render_template('device_editor.html')
    
@app.route('/photo_editor')
def photo_editor():
    return render_template('photo_editor.html')

# API endpoint to save device configuration
@app.route('/api/save_device_config', methods=['POST'])
def save_device_config():
    data = request.json
    print(f"Saving device config: {data}")
    
    config = update_device(data)
    
    print(config)
    
    return config

    return jsonify({"success": True})
    #else:
    return jsonify({"error": "Device not found"}), 404
    
@app.route('/api/save_photo_config', methods=['POST'])
def save_photo_config():
    data = request.json
    print(f"Saving photo config: {data}")
    
    config = update_photo(data)
    
    print(config)
    
    return config

    return jsonify({"success": True})
    #else:
    return jsonify({"error": "Device not found"}), 404

'''@app.route('/photo_library/<path:filename>', methods=['GET'])
def photo_library(filename):
    print("photo_library")
    photo_path = os.path.join('../photo_library',filename)
    
    photo = get_single_photo_config(filename)
    
    if photo is None:
        print(filename)
    
    scaling = get_single_photo_config(filename).get_scaling()
    
    #print(get_single_photo_config(filename).get_scaling())
    
    #format_photo_for_edit_window(photo_path)    
    return send_file(format_photo_for_edit_window(photo_path,scaling),mimetype='image/jpeg')'''
    
@app.route('/photo_library/<filename>/<scaling>', methods=['GET'])
def get_scaled_photo(filename,scaling):

    #print(f"Scaling value: {scaling}")
    #photo_path = os.path.join('../photo_library',filename)
    photo_path = os.path.join(parent_dir,'photo_library',filename)
    return send_file(format_photo_for_edit_window(photo_path,scaling),mimetype='image/jpeg')
    
@app.route('/photo_preview/<path:filename>', methods=['GET'])
def get_photo_preview(filename):

    photo_path = os.path.join(parent_dir,'photo_library',filename)
    return send_file(format_photo_for_preview(photo_path),mimetype='image/jpeg')

@app.route('/api/update_dns', methods=['GET'])
def update_dns():
    
    try:
        result = subprocess.run(['sudo', 'python3', upate_dns_script_path], check=True, text=True, capture_output=True)
        print("Script output:",result.stdout)
        print("Script error output (if any):",result.stderr)
        return jsonify({"message":"IP address updated successfully"}), 200
    except subprocess.CalledProcessError as e:
        print(f"Failed to run the script: {e}")
        return jsonify({"message":"IP address update failed"}), 404

@app.route('/api/find_discoverable_bluetooth_devices', methods=['GET'])
def find_discoverable_bluetooth_devices():
    
    print("/api/find_discoverable_bluetooth_devices")
    discovered_devices = DigitalPhotoFrameAPI.find_discoverable_bluetooth_devices()
    print("Result of find_discoverable_bluetooth_devices:")
    print(discovered_devices)
    return discovered_devices
    
@app.route('/api/invite_discovered_devices_to_network', methods=['POST'])
def invite_discovered_devices_to_network():
    
    print("/api/invite_discovered_devices_to_network")
    invited_devices = request.json
    print("Result of request.json:")
    print(invited_devices)
    connection_confirmation = DigitalPhotoFrameAPI.invite_discovered_devices_to_network(invited_devices)
    print("Result of invite_discovered_devices_to_network:")
    print(invited_devices)
    updated_collection = add_new_devices(invited_devices)
    print("Result of add_new_devices:")
    print(updated_collection)
    return updated_collection

@app.route('/api/enumerate_wifi_devices', methods=['GET'])
def enumerate_wifi_devices():
    
    print("/api/enumerate_wifi_devices")
    networked_devices = DigitalPhotoFrameAPI.enumerate_wifi_devices()
    print("Result of enumerate_wifi_devices:")
    print(networked_devices)
    updated_collection = get_connection_status(networked_devices)
    print("Result of get_connection_status:")
    print(updated_collection)
    return updated_collection
    
@app.route('/api/upload_photos', methods=['POST'])
def upload_photos():
    
    print("/api/upload_photos")
    if 'files[]' not in request.files:
        return redirect(request.url)
    
    files = request.files.getlist('files[]')
    photo_names = []
    
    for file in files:
        if file and file.filename.endswith('.jpg'):
            alphabet = string.ascii_letters+string.digits
            new_filename = ''.join(secrets.choice(alphabet) for _ in range(10))+'.jpg'
            file.save(os.path.join(photo_library_path,new_filename))
            photo_names.append(new_filename)
    
    print("Result of file iteration:")
    print(photo_names)
    
    if len(photo_names) != 0:
        photo_config = add_new_photos(photo_names)
        print("Result of add_new_photos:")
        print(photo_config)
    
    return redirect(url_for('photo_editor'))
    
@app.route('/api/update_connection_status', methods=['POST'])
def update_connection_status():
    data = request.json
    print(f"Updating connection status: {data}")
    
    config = update_device_connection_status(data)
    
    print(f"Config after update_device_connection_status:\n{config}")

    return jsonify({"success": True})
    
@app.route('/api/delete_devices', methods=['POST'])
def delete_devices():
    data = request.json
    print(f"delete_devices: {data}")
    
    config = remove_devices(data)
    
    print(f"Config after remove_devices:\n{config}")

    return config

@app.route('/api/delete_photos', methods=['POST'])
def delete_photos():
    data = request.json
    print(f"delete_photos: {data}")
    
    config = remove_photos(data)
    
    print(f"Config after remove_photos:\n{config}")

    return config

def start_web_server():
    
    app.run(host='0.0.0.0',port=5000, debug=False,use_reloader=False)


if __name__ == '__main__':
    #context = ('cert.pem', 'key.pem')
    #update_dns()
    app.run(host='0.0.0.0', port=5000, debug=True)
    #app.run(host='0.0.0.0', port=5000, ssl_context=context)
    
    
