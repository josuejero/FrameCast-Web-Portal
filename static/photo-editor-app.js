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
                photoList.innerHTML += `<label><input type="radio" name="photo" value="${id}"> ${photo.photo_name}</label>`;
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
            document.querySelector('.preview-image').src = data.path;
            document.querySelector('.rotate-ccw').dataset.photoId = data.photo_id;
            document.querySelector('.rotate-cw').dataset.photoId = data.photo_id;
            document.querySelector('.scale').dataset.photoId = data.photo_id;
            document.querySelector('.save').dataset.photoId = data.photo_id;
        })
        .catch(error => console.error('Error fetching photo config:', error));
}

function uploadPhoto() {
    console.log("Uploading new photo...");
    // Simulate photo upload
    let newPhoto = {
        photo_name: "New Photo",
        path: "path/to/new_photo.jpg"
    };
    fetch('/api/upload_photo', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(newPhoto)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('Photo uploaded successfully');
            getAllPhotos(); // Refresh photo list
        }
    })
    .catch(error => console.error('Error uploading photo:', error));
}

function savePhotoConfig(photo_id) {
    let rotation = document.querySelector('.rotate-ccw').dataset.rotation || 0;
    let scaling = document.querySelector('.scale-input').value;
    let window = {x: 0, y: 0}; // Simulate window position

    let photoConfig = {
        photo_id: photo_id,
        rotation: rotation,
        scaling: scaling,
        window: window
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

document.addEventListener('DOMContentLoaded', () => {
    console.log("Document loaded, fetching initial data...");
    getAllPhotos();
});

document.querySelector('.upload-button').addEventListener('click', uploadPhoto);
document.querySelector('.save').addEventListener('click', (event) => {
    savePhotoConfig(event.target.dataset.photoId);
});
