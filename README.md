# FrameCast Web Portal

## Overview

The Web Portal is part of the FrameCast ecosystem, designed to run on the Principal's Raspberry Pi 4. It provides functionalities similar to the Android mobile app, allowing users to manage and configure their digital photo frames via a web browser. This includes uploading photos, assigning them to devices, and editing device configurations.

## Features

- **Device Manager**: Discover and manage Bluetooth and WiFi connected devices.
- **Device Editor**: Configure device settings, assign photos, and manage photo display settings.
- **Photo Editor**: Edit photos by rotating, scaling, and setting the display window.

## Prerequisites

- Raspberry Pi 4
- Python 3.7 or higher
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- SQLite
- Node.js and npm (for frontend tests)
- Puppeteer and Jest (for frontend tests)

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/josuejero/FrameCast-Web-Portal.git
    cd FrameCast-Web-Portal
    ```

2. **Set up the virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install the dependencies**:
    ```bash
    pip3 install Flask Flask-SQLAlchemy Flask-Migrate netifaces
    ```

4. **Set up the database**:
    ```bash
    flask db upgrade
    ```

5. **Run the application**:
    ```bash
    flask run --host=0.0.0.0
    ```

## Directory Structure

    ├── app.py
    ├── concat_files.sh
    ├── instance
    │ └── photos.db
    ├── jest.config.js
    ├── jest.setup.js
    ├── LICENSE
    ├── migrations
    │ ├── alembic.ini
    │ ├── env.py
    │ ├── pycache
    │ │ └── env.cpython-39.pyc
    │ ├── README
    │ ├── script.py.mako
    │ └── versions
    │ ├── c7e6147d997f_add_photo_update_frequency_and_random_.py
    │ └── pycache
    │ ├── 59e4b90e1b69_initial_migration_with_ip_address_column.cpython-39.pyc
    │ └── c7e6147d997f_add_photo_update_frequency_and_random_.cpython-39.pyc
    ├── package.json
    ├── package-lock.json
    ├── photo_frame.db
    ├── photos.db
    ├── pycache
    │ ├── app.cpython-37.pyc
    │ ├── app.cpython-39.pyc
    │ ├── test_app.cpython-39-pytest-8.2.1.pyc
    │ ├── test_config.cpython-39-pytest-8.2.1.pyc
    │ ├── test_db.cpython-39-pytest-8.2.1.pyc
    │ └── test_device_model.cpython-39-pytest-8.2.1.pyc
    ├── README.md
    ├── static
    │ ├── app.js
    │ ├── device-editor-app.js
    │ ├── photo-editor-app.js
    │ ├── style.css
    │ ├── style_device_editor.css
    │ └── style_photo_editor.css
    ├── templates
    │ ├── device_editor.html
    │ ├── index.html
    │ └── photo_editor.html
    ├── test_app.py
    ├── test_config.py
    ├── test_db.py
    ├── test_device_model.py
    └── tests
    └── photo-editor-app.test.js

## API Endpoints

### Device Manager

- **GET /api/find_discoverable_bluetooth_devices**: Finds discoverable Bluetooth devices.
- **POST /api/invite_to_network**: Invites discovered devices to the network.
- **GET /api/enumerate_wifi_devices**: Enumerates WiFi devices.

### Device Editor

- **GET /api/get_all_devices**: Retrieves all devices in the ecosystem.
- **POST /api/save_device_config**: Saves the configuration of a device.
- **POST /api/add_photos_to_devices**: Adds photos to devices.
- **POST /api/move_photo/<photo_id>**: Moves the photo within the device's list.
- **DELETE /api/remove_photo/<photo_id>**: Removes the photo from the device.

### Photo Editor

- **GET /api/get_all_photos**: Retrieves all photos on the Principal.
- **POST /api/upload_photo**: Uploads a new photo to the Principal.
- **GET /api/get_photo/<int:photo_id>**: Retrieves details of a specific photo.
- **POST /api/save_photo_config**: Saves the configuration of a photo.

## Usage

### Device Manager

1. **Find New Devices**: Click the "Find New Devices" button to discover Bluetooth devices.
2. **Invite to Network**: Click the "Invite to Network" button to add the selected devices to the network.

### Device Editor

1. **Configure Devices**: Select a device to edit its settings.
2. **Assign Photos**: Select photos and assign them to devices.

### Photo Editor

1. **Edit Photos**: Select a photo to edit its display settings.
2. **Upload New Photos**: Click the "Upload New Photos" button to add photos to the Principal.

## Contributing

Contributions are welcome! Please fork the repository and submit pull requests.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements

- Flask
- SQLite
- JavaScript
