// ./static/device-editor-app.js

document.addEventListener('DOMContentLoaded', () => {
    console.log("Document loaded, fetching initial data...");
    getAllPhotos();
    getAllDevices();
});

function getAllPhotos() {
    console.log("Fetching all photos...");
    fetch('/api/get_all_photos')
        .then(response => response.json())
        .then(data => {
            console.log("Photos fetched:", data);
            let photoList = document.getElementById('photo-list');
            photoList.innerHTML = '';
            for (let id in data) {
                let photo = data[id];
                const label = document.createElement('label');
                label.innerHTML = `<input type="radio" name="photo" value="${id}"> ${photo.photo_name}`;
                label.querySelector('input').addEventListener('change', () => {
                    getPhotoConfig(id);
                });
                photoList.appendChild(label);
            }
        })
        .catch(error => console.error('Error fetching photos:', error));
}

function getPhotoConfig(photo_id) {
    console.log(`Fetching photo config for ${photo_id}...`);
    fetch(`/api/get_photo/${photo_id}`)
        .then(response => response.json())
        .then(data => {
            console.log("Photo config fetched:", data);
            const previewImage = document.getElementById('photo-preview');
            previewImage.src = data.path;
            previewImage.dataset.rotation = data.rotation;
            previewImage.dataset.scaling = data.scaling;
            previewImage.dataset.x = data.split_screen.x;
            previewImage.dataset.y = data.split_screen.y;
            previewImage.dataset.width = data.split_screen.width;
            previewImage.dataset.height = data.split_screen.height;
        })
        .catch(error => console.error('Error fetching photo config:', error));
}

function getAllDevices() {
    console.log("Fetching all devices...");
    fetch('/api/get_all_devices')
        .then(response => response.json())
        .then(data => {
            console.log("Devices fetched:", data);
            let deviceList = document.getElementById('device-list');
            deviceList.innerHTML = '';
            for (let id in data) {
                let device = data[id];
                const label = document.createElement('label');
                label.innerHTML = `<input type="checkbox" name="device" value="${id}"> ${device.device_name}`;
                deviceList.appendChild(label);
            }
        })
        .catch(error => console.error('Error fetching devices:', error));
}


/**
 * Show photo preview
 */
function showPhotoPreview(photoPath) {
    const previewImage = document.getElementById('photo-preview');
    previewImage.src = photoPath;
}

/**
 * Save the device configuration to the server
 */
function saveDeviceConfig() {
    let deviceName = document.getElementById('device-name').value;
    let photoUpdateFrequency = document.getElementById('photo-update-frequency').value;
    let randomOrder = document.getElementById('random-order').checked;

    let deviceConfig = {
        device_name: deviceName,
        photo_update_frequency: photoUpdateFrequency,
        random_order: randomOrder
    };

    console.log("Saving device configuration:", deviceConfig);

    fetch('/api/save_device_config', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(deviceConfig)
    })
        .then(response => response.json())
        .then(data => {
            console.log("Save response:", data);
            if (data.success) {
                alert('Device configuration saved successfully');
            }
        })
        .catch(error => console.error('Error saving device configuration:', error));
}

/**
 * Add selected photos to selected devices
 */
function addToDevices() {
    let selectedPhotos = Array.from(document.querySelectorAll('input[name="photo"]:checked')).map(input => input.value);
    let selectedDevices = Array.from(document.querySelectorAll('input[name="device"]:checked')).map(input => input.value);

    if (selectedPhotos.length === 0 || selectedDevices.length === 0) {
        alert("Please select at least one photo and one device.");
        return;
    }

    console.log("Adding Photos to Devices", selectedPhotos, selectedDevices);

    fetch('/api/add_photos_to_devices', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            photo_ids: selectedPhotos,
            device_ids: selectedDevices
        })
    })
        .then(response => response.json())
        .then(data => {
            console.log("Add photos response:", data);
            if (data.success) {
                alert('Photos successfully added to devices');
            }
        })
        .catch(error => console.error('Error adding photos to devices:', error));
}

document.querySelector('.add-to-devices').addEventListener('click', addToDevices);
document.querySelector('.save-config').addEventListener('click', saveDeviceConfig);
