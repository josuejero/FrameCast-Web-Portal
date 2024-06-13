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
            document.querySelector('.preview-image').src = data.path;
            document.querySelector('.rotate-ccw').dataset.photoId = data.photo_id;
            document.querySelector('.rotate-cw').dataset.photoId = data.photo_id;
            document.querySelector('.scale').dataset.photoId = data.photo_id;
            document.querySelector('.save').dataset.photoId = data.photo_id;
        })
        .catch(error => console.error('Error fetching photo config:', error));
}
/**
 * Simulate uploading a new photo to the server
 */
function uploadPhoto(event) {
    event.preventDefault();
    let formData = new FormData(document.getElementById('upload-form'));
    console.log("Uploading new photo...");
    fetch('/api/upload_photo', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('Photo uploaded successfully');
            getAllPhotos();
        }
    })
    .catch(error => console.error('Error uploading photo:', error));
}

/**
 * Save the photo configuration to the server
 * @param {string} photo_id - The ID of the photo to save
 */
function savePhotoConfig(photo_id) {
    let rotation = document.querySelector('.rotate-ccw').dataset.rotation || 0;
    let scaling = document.querySelector('.scale-input').value;
    let window = {x: 0, y: 0};
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
document.querySelector('.save').addEventListener('click', (event) => {
    savePhotoConfig(event.target.dataset.photoId);
});