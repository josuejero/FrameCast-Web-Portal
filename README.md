# FrameCast Web Portal

## Project Overview

The FrameCast Web Portal project is designed to manage digital photo frames through a web-based interface. This project includes various functionalities for handling devices and photos, including configuration, communication with devices via Bluetooth and WiFi, and photo management.

## Key Features

- **Device Management**: Add, edit, and manage devices connected to the FrameCast network.
- **Photo Management**: Upload, edit, and organize photos for display on digital photo frames.
- **Web Interface**: User-friendly web interface for managing devices and photos.
- **API Integration**: RESTful API endpoints for device and photo operations.
- **Bluetooth and WiFi**: Discover and manage devices using Bluetooth and WiFi connectivity.

## Installation

To set up the FrameCast Web Portal, follow these steps:

1. **Clone the repository**:
    ```sh
    git clone https://github.com/josuejero/FrameCast-Web-Portal.git
    cd FrameCast-Web-Portal
    ```

2. **Create a virtual environment and activate it**:
    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Set up the database**:
    ```sh
    flask db upgrade
    ```

4. **Run the application**:
    ```sh
    flask run
    ```

## Usage

Once the application is running, you can access the web interface at `http://127.0.0.1:5000/`. The web interface provides options to manage devices and photos.

### Running Tests

- **To run the tests, use the following command**:
    ```sh
    pytest
    ```

## API Endpoints

The project includes several API endpoints to interact with devices and photos. Some of the key endpoints are:

- `GET /api/get_device/<device_id>`: Retrieve details of a specific device.
- `POST /api/upload_photo`: Upload a new photo.
- `GET /api/get_all_photos`: Retrieve all photos.
- `POST /api/save_device_config`: Save device configuration.
- `POST /api/save_photo_config`: Save photo configuration.

Refer to the project documentation for a complete list of API endpoints and their usage.

## Contribution

We welcome contributions to enhance the FrameCast Web Portal. If you would like to contribute, please fork the repository, create a new branch, and submit a pull request. Ensure that your code follows the project's coding standards and includes appropriate tests.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Acknowledgments

We would like to thank all the FIU Spring-24/Summer-24 Senior Design Team 9 that made this project possible.

