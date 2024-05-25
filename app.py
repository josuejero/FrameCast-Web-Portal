from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

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

    for mac, device in discovered_devices.items():
        if mac in data:
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
    return jsonify({"success": True})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not Device.query.first():
            device1 = Device(device_name="Device1", device_type="Principal", status="Online", ip_address="192.168.1.1")
            device2 = Device(device_name="Device2", device_type="Agent", status="Offline", ip_address="192.168.1.2")
            db.session.add(device1)
            db.session.add(device2)
            db.session.commit()
    app.run(debug=True, host='0.0.0.0')
