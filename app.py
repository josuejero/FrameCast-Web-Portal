from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import socket
import subprocess
import netifaces as ni

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///photos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    photo_name = db.Column(db.String(100), nullable=False)
    path = db.Column(db.String(200), nullable=False)
    rotation = db.Column(db.Integer, default=0)
    scaling = db.Column(db.Integer, default=100)
    window_x = db.Column(db.Integer, default=0)
    window_y = db.Column(db.Integer, default=0)

class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_name = db.Column(db.String(100), nullable=False)
    device_type = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    ip_address = db.Column(db.String(50), nullable=False)
    photo_update_frequency = db.Column(db.Integer, default=0)
    random_order = db.Column(db.Boolean, default=False)

class PhotoDevice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    photo_id = db.Column(db.Integer, db.ForeignKey('photo.id'), nullable=False)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)
    
@app.route('/api/simulated_photo_config', methods=['GET'])
def get_simulated_photo_config():
    simulated_response = {
        "photo_id": 1,
        "photo_name": "Simulated Photo",
        "rotation": 0,
        "scaling": 100,
        "window": (0, 0)
    }
    return jsonify(simulated_response)

@app.route('/api/simulated_photos', methods=['GET'])
def get_simulated_photos():
    simulated_photos = {
        1: {"photo_name": "Photo1", "path": "path/to/photo1.jpg"},
        2: {"photo_name": "Photo2", "path": "path/to/photo2.jpg"}
    }
    return jsonify(simulated_photos)

# Function to get IP address
def get_ip_address():
    hostname = socket.gethostname()
    fqdn = socket.getfqdn()

    # Get the local IP address using netifaces
    try:
        interfaces = ni.interfaces()
        for interface in interfaces:
            if ni.AF_INET in ni.ifaddresses(interface):
                ip_address = ni.ifaddresses(interface)[ni.AF_INET][0]['addr']
                # Exclude loopback address
                if ip_address != '127.0.0.1':
                    break
    except Exception as e:
        print(f"Error getting IP address: {e}")
        ip_address = None

    return ip_address, fqdn

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
    global discovered_devices
    discovered_devices = {
        "00:11:22:33:44:55": {"device_name": "Device1", "device_type": "Agent", "status": "Online", "ip_address": "192.168.1.2"},
        "00:11:22:33:44:56": {"device_name": "Device2", "device_type": "Agent", "status": "Offline", "ip_address": "192.168.1.3"}
    }
    return jsonify(discovered_devices)

@app.route('/api/invite_to_network', methods=['POST'])
def invite_to_network():
    global discovered_devices
    data = request.json
    print(f"Inviting devices: {data}")

    for mac in data:
        device = discovered_devices.get(mac)
        if device:
            print(f"Adding device: {device}")
            new_device = Device(
                device_name=device['device_name'],
                device_type=device['device_type'],
                status=device['status'],
                ip_address=device['ip_address']
            )
            db.session.add(new_device)
    
    db.session.commit()
    return jsonify({"success": True})

@app.route('/api/enumerate_wifi_devices', methods=['GET'])
def enumerate_wifi_devices():
    devices = Device.query.all()
    devices_dict = {
        device.id: {
            "device_name": device.device_name,
            "device_type": device.device_type,
            "status": device.status,
            "ip_address": device.ip_address
        }
        for device in devices
    }
    return jsonify(devices_dict)

@app.route('/api/get_all_photos', methods=['GET'])
def get_all_photos():
    photos = Photo.query.all()
    photos_dict = {photo.id: {"photo_name": photo.photo_name, "path": photo.path} for photo in photos}
    return jsonify(photos_dict)

@app.route('/api/get_all_devices', methods=['GET'])
def get_all_devices():
    devices = Device.query.all()
    devices_dict = {device.id: {"device_name": device.device_name, "device_type": device.device_type, "status": device.status} for device in devices}
    return jsonify(devices_dict)

@app.route('/api/get_photo/<photo_id>', methods=['GET'])
def get_photo(photo_id):
    photo = Photo.query.get(photo_id)
    if photo:
        photo_data = {
            "photo_id": photo.id,
            "photo_name": photo.photo_name,
            "rotation": photo.rotation,
            "scaling": photo.scaling,
            "window": (photo.window_x, photo.window_y)
        }
        return jsonify(photo_data)
    else:
        return jsonify({"error": "Photo not found"}), 404

@app.route('/api/upload_photo', methods=['POST'])
def upload_photo():
    data = request.json
    print(f"Uploading photo: {data}")
    new_photo = Photo(photo_name=data['photo_name'], path=data['path'])
    db.session.add(new_photo)
    db.session.commit()
    return jsonify({"success": True})

@app.route('/api/save_device_config', methods=['POST'])
def save_device_config():
    data = request.json
    print(f"Saving device config: {data}")
    device = Device.query.filter_by(device_name=data['device_name']).first()
    if device:
        device.photo_update_frequency = data['photo_update_frequency']
        device.random_order = data['random_order']
        db.session.commit()
        return jsonify({"success": True})
    else:
        return jsonify({"error": "Device not found"}), 404

@app.route('/api/add_photos_to_devices', methods=['POST'])
def add_photos_to_devices():
    data = request.json
    print(f"Adding photos to devices: {data}")
    photo_ids = data.get('photo_ids', [])
    device_ids = data.get('device_ids', [])
    for photo_id in photo_ids:
        for device_id in device_ids:
            new_photo_device = PhotoDevice(photo_id=photo_id, device_id=device_id)
            db.session.add(new_photo_device)
    db.session.commit()
    return jsonify({"success": True})

@app.route('/api/move_photo/<photo_id>', methods=['POST'])
def move_photo(photo_id):
    direction = request.json.get('direction')
    print(f"Moving photo {photo_id} {direction}")
    return jsonify({"success": True})

@app.route('/api/remove_photo/<photo_id>', methods=['DELETE'])
def remove_photo(photo_id):
    print(f"Removing photo {photo_id}")
    return jsonify({"success": True})

@app.route('/api/get_ip_address', methods=['GET'])
def get_ip():
    ip_address, fqdn = get_ip_address()
    return jsonify({'ip_address': ip_address, 'fqdn': fqdn})

def map_url_to_ip(ip_address):
    url = f"http://{ip_address}:5000"
    # You can update the system's hosts file or use a DNS server to map the URL to this IP
    # For example, updating /etc/hosts (Linux/Mac):
    try:
        with open('/etc/hosts', 'a') as f:
            f.write(f"{ip_address}\tframecast.local\n")
        print(f"Mapped {url} to framecast.local")
    except Exception as e:
        print(f"Error mapping URL to IP: {e}")
        
@app.route('/api/map_url', methods=['GET'])
def map_url():
    ip_address, _ = get_ip_address()
    map_url_to_ip(ip_address)
    return jsonify({'success': True})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0')
