/**
 * Fetch all photos from the server and update the photo list in the UI
 */
function getAllPhotos() {
    console.log("Fetching all photos...");
    fetch('/api/get_all_photos')
        .then(response => response.json())
        .then(data => {
            console.log("Photos fetched:", data);
            let photoList = document.querySelector('.photo-list');
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

/**
 * Fetch the configuration for a specific photo and update the UI with the photo details
 * @param {string} photo_id - The ID of the photo to fetch
 */
function getPhotoConfig(photo_id) {
    console.log(`Fetching photo config for ${photo_id}...`);
    fetch(`/api/get_photo/${photo_id}`)
        .then(response => response.json())
        .then(data => {
            console.log("Photo config fetched:", data);
            const previewImage = document.querySelector('.preview-image');
            previewImage.src = data.path;
            previewImage.dataset.rotation = data.rotation;
            previewImage.dataset.scaling = data.scaling;
            document.querySelector('.scale-input').value = data.scaling;
            document.querySelector('.rotate-ccw').dataset.photoId = data.photo_id;
            document.querySelector('.rotate-cw').dataset.photoId = data.photo_id;
            document.querySelector('.scale').dataset.photoId = data.photo_id;
            document.querySelector('.save').dataset.photoId = data.photo_id;

            // Update the rotation and scaling data attributes
            updatePreviewImage(data.rotation, data.scaling);
        })
        .catch(error => console.error('Error fetching photo config:', error));
}

/**
 * Update the preview image with the specified rotation and scaling
 * @param {number} rotation - The rotation angle of the photo
 * @param {number} scaling - The scaling percentage of the photo
 */
function updatePreviewImage(rotation, scaling) {
    const previewImage = document.querySelector('.preview-image');
    previewImage.style.transform = `rotate(${rotation}deg) scale(${scaling / 100})`;
}

/**
 * Rotate the photo counterclockwise by 90 degrees
 */
function rotatePhotoCCW() {
    const photoId = this.dataset.photoId;
    fetch(`/api/get_photo/${photoId}`)
        .then(response => response.json())
        .then(data => {
            const newRotation = (data.rotation - 90 + 360) % 360; // Ensure rotation is always positive
            savePhotoConfig(photoId, newRotation, data.scaling);
        })
        .catch(error => console.error('Error rotating photo CCW:', error));
}

/**
 * Rotate the photo clockwise by 90 degrees
 */
function rotatePhotoCW() {
    const photoId = this.dataset.photoId;
    fetch(`/api/get_photo/${photoId}`)
        .then(response => response.json())
        .then(data => {
            const newRotation = (data.rotation + 90) % 360;
            savePhotoConfig(photoId, newRotation, data.scaling);
        })
        .catch(error => console.error('Error rotating photo CW:', error));
}

/**
 * Scale the photo to the specified percentage
 */
function scalePhoto() {
    const photoId = this.dataset.photoId;
    const newScaling = document.querySelector('.scale-input').value;
    fetch(`/api/get_photo/${photoId}`)
        .then(response => response.json())
        .then(data => {
            savePhotoConfig(photoId, data.rotation, newScaling);
        })
        .catch(error => console.error('Error scaling photo:', error));
}

/**
 * Save the photo configuration to the server
 * @param {string} photo_id - The ID of the photo to save
 * @param {number} rotation - The rotation angle of the photo
 * @param {number} scaling - The scaling percentage of the photo
 */
function savePhotoConfig(photo_id, rotation, scaling) {
    let window = { x: 0, y: 0 };
    let splitScreen = {
        x: document.querySelector('.split-screen-x').value,
        y: document.querySelector('.split-screen-y').value,
        width: document.querySelector('.split-screen-width').value,
        height: document.querySelector('.split-screen-height').value
    };

    let photoConfig = {
        photo_id: photo_id,
        rotation: rotation,
        scaling: scaling,
        window: window,
        split_screen: splitScreen
    };

    console.log("Saving photo config:", photoConfig);

    fetch('/api/save_photo_config', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(photoConfig)
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('Photo configuration saved successfully');
                getPhotoConfig(photo_id); // Refresh the photo config in the UI
            }
        })
        .catch(error => console.error('Error saving photo configuration:', error));
}

// Event listener for when the document content is loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log("Document loaded, fetching initial data...");
    getAllPhotos();
});

document.getElementById('upload-form').addEventListener('submit', uploadPhoto);
document.querySelector('.rotate-ccw').addEventListener('click', rotatePhotoCCW);
document.querySelector('.rotate-cw').addEventListener('click', rotatePhotoCW);
document.querySelector('.scale').addEventListener('click', scalePhoto);
document.querySelector('.save').addEventListener('click', (event) => {
    savePhotoConfig(event.target.dataset.photoId);
});
