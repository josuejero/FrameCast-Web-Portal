// Event listener for when the document content is loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log("Document loaded, fetching initial data...");
    getAllPhotos();
    getAllDevices();
});

/**
 * Fetch all photos from the server and update the photo list in the UI
 */
function getAllPhotos() {
    console.log("Fetching all photos...");
    fetch('/api/get_all_photos')
        .then(response => response.json())
        .then(data => {
            console.log("Photos fetched:", data);
            let photoList = document.getElementById('photo-list');
            photoList.innerHTML = '';
            // Populate the photo list element with fetched photos
            for (let id in data) {
                let photo = data[id];
                photoList.innerHTML += `<label><input type="checkbox" name="photo" value="${id}"> ${photo.photo_name}</label>`;
            }
        })
        .catch(error => console.error('Error fetching photos:', error));
}

/**
 * Fetch all devices from the server and update the device list in the UI
 */
function getAllDevices() {
    console.log("Fetching all devices...");
    fetch('/api/get_all_devices')
        .then(response => response.json())
        .then(data => {
            console.log("Devices fetched:", data);
            let deviceList = document.getElementById('device-list');
            deviceList.innerHTML = '';
            // Populate the device list element with fetched devices
            for (let id in data) {
                let device = data[id];
                deviceList.innerHTML += `<label><input type="checkbox" name="device" value="${id}"> ${device.device_name}</label>`;
            }
        })
        .catch(error => console.error('Error fetching devices:', error));
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

// Event listeners for buttons
document.querySelector('.add-to-devices').addEventListener('click', addToDevices);
document.querySelector('.save-config').addEventListener('click', saveDeviceConfig);

/**
 * Move a selected photo up or down in the list
 * @param {string} direction - The direction to move the photo ('up' or 'down')
 */
function movePhoto(direction) {
    let selectedPhotoId = document.querySelector('.assigned-photo-list input[name="assigned-photo"]:checked')?.value;
    if (!selectedPhotoId) {
        alert("Please select a photo to move.");
        return;
    }

    console.log(`Moving photo ${selectedPhotoId} ${direction}`);

    fetch(`/api/move_photo/${selectedPhotoId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ direction })
    })
        .then(response => response.json())
        .then(data => {
            console.log("Move photo response:", data);
            if (data.success) {
                getAllPhotos();
            }
        })
        .catch(error => console.error(`Error moving photo ${direction}:`, error));
}

// Event listeners for move up and move down buttons
document.querySelector('.move-up').addEventListener('click', () => movePhoto('up'));
document.querySelector('.move-down').addEventListener('click', () => movePhoto('down'));

/**
 * Remove a selected photo from the list
 */
function removePhoto() {
    let selectedPhotoId = document.querySelector('.assigned-photo-list input[name="assigned-photo"]:checked')?.value;
    if (!selectedPhotoId) {
        alert("Please select a photo to remove.");
        return;
    }

    console.log(`Removing photo ${selectedPhotoId}`);

    fetch(`/api/remove_photo/${selectedPhotoId}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then(response => response.json())
        .then(data => {
            console.log("Remove photo response:", data);
            if (data.success) {
                getAllPhotos();
            }
        })
        .catch(error => console.error(`Error removing photo:`, error));
}

// Event listener for the remove button
document.querySelector('.remove').addEventListener('click', removePhoto);
