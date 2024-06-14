from flask import Flask, render_template, jsonify, request, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
import os
import socket
import netifaces as ni
import logging

logging.basicConfig(level=logging.DEBUG)

# Initialize the Flask app
app = Flask(__name__, static_folder='static', static_url_path='/static')

# Configuration for file uploads
UPLOAD_FOLDER = os.path.join(app.root_path, 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///photos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define the Photo model
class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    photo_name = db.Column(db.String(100), nullable=False)
    path = db.Column(db.String(200), nullable=False)
    rotation = db.Column(db.Integer, default=0)
    scaling = db.Column(db.Integer, default=100)
    window_x = db.Column(db.Integer, default=0)
    window_y = db.Column(db.Integer, default=0)
    split_screen_x = db.Column(db.Integer, default=0)
    split_screen_y = db.Column(db.Integer, default=0)
    split_screen_width = db.Column(db.Integer, default=100)
    split_screen_height = db.Column(db.Integer, default=100)

# Define the Device model
class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_name = db.Column(db.String(100), nullable=False)
    device_type = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    ip_address = db.Column(db.String(50), nullable=False)
    photo_update_frequency = db.Column(db.Integer, default=0)
    random_order = db.Column(db.Boolean, default=False)

# Define the PhotoDevice model
class PhotoDevice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    photo_id = db.Column(db.Integer, db.ForeignKey('photo.id'), nullable=False)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)

# Function to get IP address
def get_ip_address():
    hostname = socket.gethostname()
    fqdn = socket.getfqdn()

    try:
        interfaces = ni.interfaces()
        for interface in interfaces:
            if ni.AF_INET in ni.ifaddresses(interface):
                ip_address = ni.ifaddresses(interface)[ni.AF_INET][0]['addr']
                if ip_address != '127.0.0.1':
                    break
    except Exception as e:
        print(f"Error getting IP address: {e}")
        ip_address = None

    return ip_address, fqdn

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route to render the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route to render the device editor page
@app.route('/device-editor')
def device_editor():
    return render_template('device_editor.html')

# Route to render the photo editor page
@app.route('/photo-editor')
def photo_editor():
    return render_template('photo_editor.html')

@app.route('/api/get_device/<device_id>', methods=['GET'])
def get_device(device_id):
    device = Device.query.get(device_id)
    if device:
        attached_photos = PhotoDevice.query.filter_by(device_id=device_id).all()
        photos = [Photo.query.get(photo_device.photo_id) for photo_device in attached_photos]
        photos_data = [
            {
                "photo_id": photo.id,
                "photo_name": photo.photo_name,
                "path": url_for('uploaded_file', filename=os.path.basename(photo.path))
            } for photo in photos
        ]
        device_data = {
            "device_id": device.id,
            "device_name": device.device_name,
            "photo_update_frequency": device.photo_update_frequency,
            "random_order": device.random_order,
            "photos": photos_data
        }
        return jsonify(device_data)
    else:
        return jsonify({"error": "Device not found"}), 404


# API endpoint to find discoverable Bluetooth devices
@app.route('/api/find_discoverable_bluetooth_devices', methods=['GET'])
def find_discoverable_bluetooth_devices():
    global discovered_devices
    discovered_devices = {
        "00:11:22:33:44:55": {"device_name": "Device1", "device_type": "Agent", "status": "Online", "ip_address": "192.168.1.2"},
        "00:11:22:33:44:56": {"device_name": "Device2", "device_type": "Agent", "status": "Offline", "ip_address": "192.168.1.3"}
    }
    return jsonify(discovered_devices)

# API endpoint to invite devices to the network
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

# API endpoint to enumerate WiFi devices
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

# API endpoint to get all photos
# ./app.py

@app.route('/api/get_all_photos', methods=['GET'])
def get_all_photos():
    photos = Photo.query.all()
    photos_dict = {photo.id: {"photo_name": photo.photo_name, "path": url_for('uploaded_file', filename=os.path.basename(photo.path))} for photo in photos}
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
            "path": url_for('uploaded_file', filename=os.path.basename(photo.path)),
            "rotation": photo.rotation,
            "scaling": photo.scaling,
            "window": {"x": photo.window_x, "y": photo.window_y},
            "split_screen": {
                "x": photo.split_screen_x,
                "y": photo.split_screen_y,
                "width": photo.split_screen_width,
                "height": photo.split_screen_height
            }
        }
        logging.debug(f"Photo data: {photo_data}")
        return jsonify(photo_data)
    else:
        return jsonify({"error": "Photo not found"}), 404

@app.route('/api/upload_photo', methods=['POST'])
def upload_photo():
    logging.debug('Upload photo endpoint called')
    if 'file' not in request.files:
        logging.error("No file part in the request")
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        logging.error("No selected file")
        return jsonify({"error": "No selected file"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        logging.debug(f'File saved to {filepath}')
        new_photo = Photo(photo_name=filename, path=filepath)
        db.session.add(new_photo)
        db.session.commit()
        logging.debug(f'New photo added to database with id {new_photo.id}')
        return jsonify({"success": True, "photo_id": new_photo.id}), 201
    logging.error("File type not allowed")
    return jsonify({"error": "File type not allowed"}), 400

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# API endpoint to save device configuration
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

@app.route('/api/save_photo_config', methods=['POST'])
def save_photo_config():
    data = request.json
    photo = Photo.query.get(data['photo_id'])
    if photo:
        photo.rotation = data['rotation']
        photo.scaling = data['scaling']
        photo.window_x = data['window']['x']
        photo.window_y = data['window']['y']
        photo.split_screen_x = data['split_screen']['x']
        photo.split_screen_y = data['split_screen']['y']
        photo.split_screen_width = data['split_screen']['width']
        photo.split_screen_height = data['split_screen']['height']
        db.session.commit()
        return jsonify({"success": True})
    return jsonify({"error": "Photo not found"}), 404

# API endpoint to add photos to devices
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

# API endpoint to move a photo
@app.route('/api/move_photo/<photo_id>', methods=['POST'])
def move_photo(photo_id):
    direction = request.json.get('direction')
    print(f"Moving photo {photo_id} {direction}")
    return jsonify({"success": True})

# API endpoint to remove a photo
@app.route('/api/remove_photo/<photo_id>', methods=['DELETE'])
def remove_photo(photo_id):
    print(f"Removing photo {photo_id}")
    return jsonify({"success": True})

# API endpoint to get the IP address
@app.route('/api/get_ip_address', methods=['GET'])
def get_ip():
    ip_address, fqdn = get_ip_address()
    return jsonify({'ip_address': ip_address, 'fqdn': fqdn})

# Function to map URL to IP
def map_url_to_ip(ip_address):
    url = f"http://{ip_address}:5000"
    try:
        with open('/etc/hosts', 'a') as f:
            f.write(f"{ip_address}\tframecast.local\n")
        print(f"Mapped {url} to framecast.local")
    except Exception as e:
        print(f"Error mapping URL to IP: {e}")

# Route to reset the state (useful for tests)
@app.route('/reset', methods=['GET'])
def reset_state():
    # Clear all photos
    db.session.query(Photo).delete()
    # Add initial photos
    initial_photos = [
        Photo(photo_name='Photo1', path='path/to/photo1.jpg'),
        Photo(photo_name='Photo2', path='path/to/photo2.jpg')
    ]
    db.session.bulk_save_objects(initial_photos)
    db.session.commit()
    return jsonify({"success": True})

# API endpoint to map URL
@app.route('/api/map_url', methods=['GET'])
def map_url():
    ip_address, _ = get_ip_address()
    map_url_to_ip(ip_address)
    return jsonify({'success': True})

# Main function to run the application
if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0')
