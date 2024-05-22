from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/device-editor')
def device_editor():
    return render_template('device_editor.html')

@app.route('/photo-editor')
def photo_editor():
    return render_template('photo_editor.html')

@app.route('/api/find_discoverable_bluetooth_devices', methods=['GET'])
def find_discoverable_bluetooth_devices():
    discovered_devices = {
        "00:11:22:33:44:55": {"device_name": "Device1", "device_type": "Agent", "status": "Online", "ip_address": "192.168.1.2"},
        "00:11:22:33:44:56": {"device_name": "Device2", "device_type": "Agent", "status": "Offline", "ip_address": "192.168.1.3"}
    }
    return jsonify(discovered_devices)

@app.route('/api/invite_to_network', methods=['POST'])
def invite_to_network():
    data = request.json
    print(f"Inviting devices: {data}") # Log received data
    return jsonify({"success": True})

@app.route('/api/enumerate_wifi_devices', methods=['GET'])
def enumerate_wifi_devices():
    networked_devices = {
        "123456": {"device_name": "Device1", "device_type": "Principal", "status": "Online", "ip_address": "192.168.1.2"},
        "123457": {"device_name": "Device2", "device_type": "Agent", "status": "Offline", "ip_address": "192.168.1.3"}
    }
    return jsonify(networked_devices)

@app.route('/api/get_all_photos', methods=['GET'])
def get_all_photos():
    photos = {
        "photo1": {"photo_name": "Photo1", "path": "path/to/photo1.jpg"},
        "photo2": {"photo_name": "Photo2", "path": "path/to/photo2.jpg"}
    }
    return jsonify(photos)

@app.route('/api/get_all_devices', methods=['GET'])
def get_all_devices():
    devices = {
        "device1": {"device_name": "Device1", "device_type": "Agent", "status": "Online"},
        "device2": {"device_name": "Device2", "device_type": "Principal", "status": "Offline"}
    }
    return jsonify(devices)

@app.route('/api/get_photo/<photo_id>', methods=['GET'])
def get_photo(photo_id):
    photo = {
        "photo_id": photo_id,
        "photo_name": f"Photo{photo_id[-1]}",
        "rotation": 0,
        "scaling": 100,
        "window": (0, 0)
    }
    return jsonify(photo)

def upload_photo():
    data = request.json
    print(f"Uploading photo: {data}")
    return jsonify({"success": True})

@app.route('/api/save_device_config', methods=['POST'])
def save_device_config():
    data = request.json
    print(f"Saving device config: {data}")
    return jsonify({"success": True})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
