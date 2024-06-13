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
            if (!data.path) {
                console.error("Image path is empty.");
                previewImage.src = "";
            } else {
                previewImage.src = data.path;
                console.log("Image path set to:", data.path);
            }
            previewImage.dataset.rotation = data.rotation;
            previewImage.dataset.scaling = data.scaling;
            previewImage.dataset.x = data.split_screen.x;
            previewImage.dataset.y = data.split_screen.y;
            previewImage.dataset.width = data.split_screen.width;
            previewImage.dataset.height = data.split_screen.height;

            document.querySelector('.scale-input').value = data.scaling;
            document.querySelector('.split-screen-x').value = data.split_screen.x;
            document.querySelector('.split-screen-y').value = data.split_screen.y;
            document.querySelector('.split-screen-width').value = data.split_screen.width;
            document.querySelector('.split-screen-height').value = data.split_screen.height;

            document.querySelector('.rotate-ccw').dataset.photoId = data.photo_id;
            document.querySelector('.rotate-cw').dataset.photoId = data.photo_id;
            document.querySelector('.scale').dataset.photoId = data.photo_id;
            document.querySelector('.save').dataset.photoId = data.photo_id;

            updatePreviewImage(data.rotation, data.scaling, data.split_screen.x, data.split_screen.y, data.split_screen.width, data.split_screen.height);
        })
        .catch(error => console.error('Error fetching photo config:', error));
}

/**
 * Update the preview image with the specified rotation, scaling, and position
 * @param {number} rotation - The rotation angle of the photo
 * @param {number} scaling - The scaling percentage of the photo
 * @param {number} x - The x position of the photo
 * @param {number} y - The y position of the photo
 * @param {number} width - The width percentage of the photo
 * @param {number} height - The height percentage of the photo
 */
function updatePreviewImage(rotation, scaling, x, y, width, height) {
    console.log(`Updating preview image with rotation: ${rotation}, scaling: ${scaling}, x: ${x}, y: ${y}, width: ${width}, height: ${height}`);
    const previewImage = document.querySelector('.preview-image');
    previewImage.style.transform = `translate(-50%, -50%) rotate(${rotation}deg) scale(${scaling / 100})`;
    previewImage.style.position = 'absolute';
    previewImage.style.left = `${x}%`;
    previewImage.style.top = `${y}%`;
    previewImage.style.width = `${width}%`;
    previewImage.style.height = `${height}%`;
    console.log(`Preview image styles: transform=${previewImage.style.transform}, position=${previewImage.style.position}, left=${previewImage.style.left}, top=${previewImage.style.top}, width=${previewImage.style.width}, height=${previewImage.style.height}`);
    console.log(`Preview image src: ${previewImage.src}`);
}




/**
 * Rotate the photo counterclockwise by 90 degrees
 */
function rotatePhotoCCW() {
    console.log("Rotating photo counterclockwise...");
    const photoId = this.dataset.photoId;
    const previewImage = document.querySelector('.preview-image');
    const currentRotation = parseInt(previewImage.dataset.rotation);
    const newRotation = (currentRotation - 90 + 360) % 360; // Ensure rotation is always positive
    console.log(`Current rotation: ${currentRotation}, new rotation: ${newRotation}`);
    previewImage.dataset.rotation = newRotation;
    updatePreviewImage(newRotation, parseInt(previewImage.dataset.scaling), parseInt(previewImage.dataset.x), parseInt(previewImage.dataset.y), parseInt(previewImage.dataset.width), parseInt(previewImage.dataset.height));
    savePhotoConfig(photoId, newRotation, parseInt(previewImage.dataset.scaling), parseInt(previewImage.dataset.x), parseInt(previewImage.dataset.y), parseInt(previewImage.dataset.width), parseInt(previewImage.dataset.height));
}

/**
 * Rotate the photo clockwise by 90 degrees
 */
function rotatePhotoCW() {
    console.log("Rotating photo clockwise...");
    const photoId = this.dataset.photoId;
    const previewImage = document.querySelector('.preview-image');
    const currentRotation = parseInt(previewImage.dataset.rotation);
    const newRotation = (currentRotation + 90) % 360;
    console.log(`Current rotation: ${currentRotation}, new rotation: ${newRotation}`);
    previewImage.dataset.rotation = newRotation;
    updatePreviewImage(newRotation, parseInt(previewImage.dataset.scaling), parseInt(previewImage.dataset.x), parseInt(previewImage.dataset.y), parseInt(previewImage.dataset.width), parseInt(previewImage.dataset.height));
    savePhotoConfig(photoId, newRotation, parseInt(previewImage.dataset.scaling), parseInt(previewImage.dataset.x), parseInt(previewImage.dataset.y), parseInt(previewImage.dataset.width), parseInt(previewImage.dataset.height));
}

/**
 * Scale the photo to the specified percentage
 */
function scalePhoto() {
    console.log("Scaling photo...");
    const photoId = this.dataset.photoId;
    const newScaling = document.querySelector('.scale-input').value;
    const previewImage = document.querySelector('.preview-image');
    console.log(`New scaling: ${newScaling}`);
    previewImage.dataset.scaling = newScaling;
    updatePreviewImage(parseInt(previewImage.dataset.rotation), newScaling, parseInt(previewImage.dataset.x), parseInt(previewImage.dataset.y), parseInt(previewImage.dataset.width), parseInt(previewImage.dataset.height));
    savePhotoConfig(photoId, parseInt(previewImage.dataset.rotation), newScaling, parseInt(previewImage.dataset.x), parseInt(previewImage.dataset.y), parseInt(previewImage.dataset.width), parseInt(previewImage.dataset.height));
}

/**
 * Save the photo configuration to the server
 * @param {string} photo_id - The ID of the photo to save
 * @param {number} rotation - The rotation angle of the photo
 * @param {number} scaling - The scaling percentage of the photo
 * @param {number} x - The x position of the photo
 * @param {number} y - The y position of the photo
 * @param {number} width - The width percentage of the photo
 * @param {number} height - The height percentage of the photo
 */
function savePhotoConfig(photo_id, rotation, scaling, x, y, width, height) {
    let window = { x: 0, y: 0 };
    let splitScreen = { x: x, y: y, width: width, height: height };

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
            }
        })
        .catch(error => console.error('Error saving photo configuration:', error));
}

/**
 * Upload photo function to handle the form submission
 */
function uploadPhoto(event) {
    event.preventDefault();
    const formData = new FormData(document.getElementById('upload-form'));
    fetch('/api/upload_photo', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('Photo uploaded successfully');
            getAllPhotos(); // Refresh the photo list
        } else {
            console.error('Error uploading photo:', data.error);
        }
    })
    .catch(error => console.error('Error uploading photo:', error));
}

// Event listener for when the document content is loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log("Document loaded, fetching initial data...");
    getAllPhotos();

    // Add event listeners for rotate and scale buttons
    document.querySelector('.rotate-ccw').addEventListener('click', rotatePhotoCCW);
    document.querySelector('.rotate-cw').addEventListener('click', rotatePhotoCW);
    document.querySelector('.scale').addEventListener('click', scalePhoto);
    document.querySelector('.save').addEventListener('click', (event) => {
        const photoId = event.target.dataset.photoId;
        const rotation = parseInt(document.querySelector('.preview-image').dataset.rotation);
        const scaling = parseInt(document.querySelector('.preview-image').dataset.scaling);
        const x = parseInt(document.querySelector('.split-screen-x').value);
        const y = parseInt(document.querySelector('.split-screen-y').value);
        const width = parseInt(document.querySelector('.split-screen-width').value);
        const height = parseInt(document.querySelector('.split-screen-height').value);
        savePhotoConfig(photoId, rotation, scaling, x, y, width, height);
    });

    // Add event listeners for split-screen controls
    document.querySelectorAll('.split-screen-x, .split-screen-y, .split-screen-width, .split-screen-height').forEach(input => {
        input.addEventListener('input', () => {
            const rotation = parseInt(document.querySelector('.preview-image').dataset.rotation);
            const scaling = parseInt(document.querySelector('.preview-image').dataset.scaling);
            const x = parseInt(document.querySelector('.split-screen-x').value);
            const y = parseInt(document.querySelector('.split-screen-y').value);
            const width = parseInt(document.querySelector('.split-screen-width').value);
            const height = parseInt(document.querySelector('.split-screen-height').value);
            updatePreviewImage(rotation, scaling, x, y, width, height);
        });
    });
});

document.getElementById('upload-form').addEventListener('submit', uploadPhoto);
