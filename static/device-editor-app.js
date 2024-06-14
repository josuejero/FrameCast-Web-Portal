document.addEventListener('DOMContentLoaded', () => {
    console.log("Document loaded, fetching initial data...");
    getAllPhotos();
    getAllDevices();
    populateDeviceDropdown();
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
                label.innerHTML = `<input type="checkbox" name="photo" value="${id}"> ${photo.photo_name}`;
                label.querySelector('input').addEventListener('change', () => {
                    updatePhotoPreviews();
                });
                photoList.appendChild(label);
            }
        })
        .catch(error => console.error('Error fetching photos:', error));
}

function updatePhotoPreviews() {
    let selectedPhotoIds = Array.from(document.querySelectorAll('input[name="photo"]:checked')).map(input => input.value);
    let photoPreviews = document.getElementById('photo-previews');
    photoPreviews.innerHTML = '';

    selectedPhotoIds.forEach(photoId => {
        fetch(`/api/get_photo/${photoId}`)
            .then(response => response.json())
            .then(data => {
                const img = document.createElement('img');
                img.src = data.path;
                img.classList.add('preview-image');
                photoPreviews.appendChild(img);
            })
            .catch(error => console.error('Error fetching photo:', error));
    });
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

function populateDeviceDropdown() {
    fetch('/api/get_all_devices')
        .then(response => response.json())
        .then(data => {
            let deviceDropdown = document.getElementById('device-name');
            deviceDropdown.innerHTML = '';
            for (let id in data) {
                let device = data[id];
                const option = document.createElement('option');
                option.value = id;
                option.textContent = device.device_name;
                deviceDropdown.appendChild(option);
            }
        })
        .catch(error => console.error('Error fetching devices for dropdown:', error));
}

document.querySelector('.add-to-devices').addEventListener('click', () => {
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
});

document.querySelector('.save-config').addEventListener('click', () => {
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
});

document.getElementById('device-name').addEventListener('change', () => {
    let deviceId = document.getElementById('device-name').value;
    if (deviceId) {
        getDeviceDetails(deviceId);
    } else {
        clearPreviewImage();
    }
});

function getDeviceDetails(deviceId) {
    fetch(`/api/get_device/${deviceId}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
                return;
            }
            document.getElementById('photo-update-frequency').value = data.photo_update_frequency;
            document.getElementById('random-order').checked = data.random_order;
            
            let assignedPhotoList = document.getElementById('assigned-photo-list');
            assignedPhotoList.innerHTML = '';
            if (data.photos.length === 0) {
                clearPreviewImage(); // Clear the preview image
            } else {
                data.photos.forEach(photo => {
                    const label = document.createElement('label');
                    label.innerHTML = `<input type="radio" name="assigned-photo" value="${photo.photo_id}"> ${photo.photo_name}`;
                    label.querySelector('input').addEventListener('change', () => {
                        document.getElementById('assigned-photo-preview').src = photo.path;
                    });
                    assignedPhotoList.appendChild(label);
                });
                // Set the preview image to the first photo by default
                document.getElementById('assigned-photo-preview').src = data.photos[0].path;
            }
        })
        .catch(error => console.error('Error fetching device details:', error));
}

function clearPreviewImage() {
    document.getElementById('assigned-photo-preview').src = '';
}
