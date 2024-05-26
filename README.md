# FrameCast Web Portal

## Overview

The FrameCast project involves creating a browser-based web portal for managing digital photo frames. The web portal runs on a Raspberry Pi 4 and allows users to configure devices, upload photos, and edit photo display settings.

## Features

- **Device Manager**: Discover and manage digital photo frames over Bluetooth and WiFi.
- **Device Editor**: Configure device settings and assign photos to devices.
- **Photo Editor**: Edit photo display settings such as rotation, scaling, and windowing.

## Technologies Used

- **Python**
- **Flask**
- **Flask-SQLAlchemy**
- **Flask-Migrate**
- **SQLite**
- **HTML**
- **CSS**
- **JavaScript**

## Getting Started

### Prerequisites

- Python 3.x
- Flask
- Flask-SQLAlchemy
- Flask-Migrate

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/josuejero/FrameCast-Web-Portal.git
    cd framecast-web-portal
    ```

2. Set up a virtual environment and activate it:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install dependencies:
    ```bash
    pip install Flask Flask-SQLAlchemy Flask-Migrate
    ```

4. Initialize and migrate the database:
    ```bash
    flask db init
    flask db migrate -m "Initial migration with ip_address column"
    flask db upgrade
    ```

5. Run the Flask application:
    ```bash
    sudo python3 app.py
    ```

6. Open your browser and navigate to:
    ```
    http://<your-raspberry-pi-ip>:5000
    ```

## Project Structure

    ```bash
    digital-photo-frame-ecosystem/
    │
    ├── app.py # Flask application
    ├── templates/
    │ ├── index.html # Device Manager page
    │ ├── device_editor.html # Device Editor page
    │ ├── photo_editor.html # Photo Editor page
    │
    ├── static/
    │ ├── style.css # General styles
    │ ├── style_device_editor.css # Device Editor styles
    │ ├── style_photo_editor.css # Photo Editor styles
    │ ├── device-editor-app.js # JavaScript for Device Editor
    │ ├── photo-editor-app.js # JavaScript for Photo Editor
    │
    ├── migrations/ # Database migration scripts
    │
    └── README.md
    ```

## API Endpoints

### Device Manager

- **GET /api/find_discoverable_bluetooth_devices**: Finds discoverable Bluetooth devices.
- **POST /api/invite_to_network**: Invites discovered devices to the network.
- **GET /api/enumerate_wifi_devices**: Enumerates WiFi devices.

### Device Editor

- **GET /api/get_all_devices**: Retrieves all devices in the ecosystem.
- **POST /api/save_device_config**: Saves the configuration of a device.

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

