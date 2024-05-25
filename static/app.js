document.addEventListener('DOMContentLoaded', () => {
    getAllPhotos();
    getAllDevices();
});

function findNewDevices() {
    fetch('/api/find_discoverable_bluetooth_devices')
    .then(response => response.json())
    .then(data => {
        let discoveredDevices = document.getElementById('discovered-devices');
        if (discoveredDevices) {
            discoveredDevices.innerHTML = '';
            for (let mac in data) {
                let device = data[mac];
                discoveredDevices.innerHTML += `<p>${device.device_name}</p>`;
            }
        } else {
            console.error('Element "discovered-devices" not found');
        }
    })
    .catch(error => console.error('Error finding new devices:', error));
}

function inviteToNetwork() {
    let discoveredDevices = document.getElementById('discovered-devices').innerHTML;
    if (discoveredDevices.trim() === "") {
        alert("No devices found to invite. Please click 'FIND NEW DEVICES' first.");
        return;
}

let selectedDevices = {}; // Collect selected devices if necessary

fetch('/api/invite_to_network', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(selectedDevices)
})
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            findWiFiDevices();
        }
    })
    .catch(error => console.error('Error inviting devices:', error));
}

function findWiFiDevices() {
fetch('/api/enumerate_wifi_devices')
    .then(response => response.json())
    .then(data => {
        let networkedDevices = document.getElementById('networked-devices');
        if (networkedDevices) {
            networkedDevices.innerHTML = '';
            for (let sn in data) {
                let device = data[sn];
                networkedDevices.innerHTML += `
                    <div class="device-item">
                        <p>${device.device_name}</p>
                        <p>${device.device_type}</p>
                        <p>${device.status}</p>
                        <p>${device.ip_address}</p>
                    </div>`;
            }
        } else {
            console.error('Element "networked-devices" not found');
        }
    })
    .catch(error => console.error('Error finding WiFi devices:', error));
}

function getAllPhotos() {
fetch('/api/get_all_photos')
    .then(response => response.json())
    .then(data => {
        let photoList = document.getElementById('photo-list');
        if (photoList) {
            photoList.innerHTML = '';
            for (let id in data) {
                let photo = data[id];
                photoList.innerHTML += `<label><input type="checkbox" name="photo" value="${id}"> ${photo.photo_name}</label>`;
            }
        } else {
            console.error('Element "photo-list" not found');
        }
    })
    .catch(error => console.error('Error fetching photos:', error));
}

function getAllDevices() {
    fetch('/api/get_all_devices')
        .then(response => response.json())
        .then(data => {
            let deviceList = document.getElementById('device-list');
            if (deviceList) {
                deviceList.innerHTML = '';
                for (let id in data) {
                    let device = data[id];
                    deviceList.innerHTML += `<label><input type="checkbox" name="device" value="${id}"> ${device.device_name}</label>`;
                }
            } else {
                console.error('Element "device-list" not found');
            }
        })
        .catch(error => console.error('Error fetching devices:', error));
}

function saveDeviceConfig() {
    let deviceName = document.getElementById('device-name').value;
    let photoUpdateFrequency = document.getElementById('photo-update-frequency').value;
    let randomOrder = document.getElementById('random-order').checked;

    let deviceConfig = {
        device_name: deviceName,
        photo_update_frequency: photoUpdateFrequency,
        random_order: randomOrder
    };

    fetch('/api/save_device_config', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(deviceConfig)
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Device configuration saved successfully');
        }
    })
    .catch(error => console.error('Error saving device configuration:', error));
}

function uploadNewPhoto() {
    // Implementation for uploading new photo
    console.log('Uploading new photo');
    // Add your logic here for uploading new photos
}
