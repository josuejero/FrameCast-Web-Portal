let selectedPhotoIndex = 0;

/**
 * Fetch all photos from the server and update the photo list in the UI
 */
 
 
async function loadPhotos(){
    
    try{
        const response = await fetch('/get_photo_config');
        const data = await response.json();
        digitalPhotoCollection = data;
    } catch (error){
        console.error('Error fetching data:', error)
    }
       
    populatePhotoList(digitalPhotoCollection);
    if(selectedPhotoIndex < digitalPhotoCollection.length){
        populatePhotoEditor(digitalPhotoCollection[selectedPhotoIndex]); 
    }
}

function populatePhotoList(digitalPhotoCollection){
    
    const photoList = document.getElementById('photo-list');
    const photos = photoList.getElementsByClassName('list-item');
    
    photoList.innerHTML = '';
    
    let lastSelectedPhoto = null;
    
    digitalPhotoCollection.forEach((photo, index) => {

        const listItem = document.createElement('li');
        listItem.classList.add('list-item');
        listItem.textContent = photo['Name'];
        listItem.addEventListener('click', () => {
            //Array.from(photos).forEach(i => i.classList.remove('selected'));
            listItem.classList.toggle('selected');
            if(listItem.classList.contains('selected')){
                if(lastSelectedPhoto && lastSelectedPhoto !== listItem){
                    lastSelectedPhoto.classList.remove('last-selected');
                } 
                
                listItem.classList.add('last-selected');
                lastSelectedPhoto = listItem;
                
            } else {
                if(lastSelectedPhoto === listItem){
                    listItem.classList.remove('last-selected');
                    lastSelectedPhoto = null;
                }
            }
            
            
            selectedPhotoIndex = index;
            populatePhotoEditor(photo);
        });
        
        photoList.appendChild(listItem);
    });
}

function populatePhotoEditor(photo) {
    
    //document.getElementById('device-name').value = device['Name'];
    
    //console.log(photo);
    
    const photoObject = document.getElementById("previewImage");
    const scaling = document.getElementById("photoScaleValue");
    
    scaling.value = photo["Scaling"];
    
    const photoName = photo["Name"];

    const newSrc = `../../photo_library/${photoName}/${scaling.value}`;
    
    photoObject.src = newSrc;
    photoObject.style.display = 'block';
    
    
    const box = document.getElementById("windowBox");
    
    console.log(photo["Window"]);
    console.log(photo["Window"]["x"]);
    
    x=photo["Window"]["x"]/2;
    y=photo["Window"]["y"]/2;
    
    console.log(`x: ${x}, y: ${y}`);
    
    box.style.left = `${x}px`;
    box.style.top = `${y}px`;
}

async function deletePhotos(){
    
    let photosToDelete = getSelectedPhotos();
    
    if(photosToDelete.length == 0) return;
    
    try{
        const response = await fetch('/api/delete_photos', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(photosToDelete)
        });
        const data = await response.json();
        console.log("Save response:", data);
        digitalPhotoCollection = data;
        console.log("DP Collection after API call:", digitalPhotoCollection);
    } catch (error){
        console.error('Error saving device configuration:', error)
    }
       
    populatePhotoList(digitalPhotoCollection);
    if(selectedPhotoIndex < digitalPhotoCollection.length){
        populatePhotoEditor(digitalPhotoCollection[selectedPhotoIndex]); 
    }
}

function getSelectedPhotos() {
    
    const photoList = document.getElementById('photo-list');
    const photos = photoList.getElementsByClassName('list-item');
    const selectedPhotos = [];
    Array.from(photos).forEach(photo => {
        if (photo.classList.contains('selected')) {
            selectedPhotos.push(photo.textContent);
        }
    });
    
    return selectedPhotos;
 
}
 
 
/**
 * Simulate uploading a new photo to the server
 */
async function uploadPhotos(files) {
    
    //const fileInput = document.getElementById('fileinput');
    const formData = new FormData();
    
    for (const file of files){
        formData.append('files[]', file);
    }
    
    const response = await fetch('/api/upload_photos',{
        method: 'POST',
        body: formData
    });
    
    if(response.ok){
        window.location.href='photo_editor';
        loadPhotos();
    } else {
        console.error('File upload failed');
    }
    
    
}


async function savePhotoConfig(){
    
    const box = document.getElementById("windowBox");
    const scaling = document.getElementById("photoScaleValue");
    
    scaling.value = Math.min(100,scaling.value);
    scaling.value = Math.max(10,scaling.value);
    
    let x = box.offsetLeft*2;
    let y = box.offsetTop*2;
    
    let photoConfig = {
        "Photo Index":selectedPhotoIndex,
        "Window": { x,y },
        "Scaling":scaling.value
    };

    console.log("Saving device configuration:", photoConfig);

    try{
        const response = await fetch('/api/save_photo_config', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(photoConfig)
        });
        const data = await response.json();
        console.log("Save response:", data);
        digitalPhotoCollection = data;
    } catch (error){
        console.error('Error saving device configuration:', error)
    }

    populatePhotoList(digitalPhotoCollection)
    if(selectedPhotoIndex < digitalPhotoCollection.length){
        populatePhotoEditor(digitalPhotoCollection[selectedPhotoIndex]); 
    }
    
}

function scalePhoto(){
        
    let photo = digitalPhotoCollection[selectedPhotoIndex]; 
    
    const photoObject = document.getElementById("previewImage");
    const scaling = document.getElementById("photoScaleValue");
    
    const photoName = photo["Name"];

    const newSrc = `../../photo_library/${photoName}/${scaling.value}`;
    
    console.log(newSrc);
    
    photoObject.src = newSrc;   
}



// Event listener for when the document content is loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log("Document loaded, fetching initial data...");
    
    loadPhotos();
    
    const box = document.getElementById("windowBox");
    const panel = document.querySelector(".photo-container");
    const image = document.getElementById("previewImage");
    
    let offsetX, offsetY, initialX, initialY;
    
    box.addEventListener("mousedown", function(e) {
        
        offsetX = e.clientX - box.getBoundingClientRect().left;
        offsetY = e.clientY - box.getBoundingClientRect().top;
        //initialX = e.clientX;
        //initialY = e.clientY;
        box.style.cursor = "grabbing";
        
        document.addEventListener("mousemove", onMouseMove);
        document.addEventListener("mouseup", onMouseUp);

    });
    
    function onMouseMove(e) {
        
        const panelRect = panel.getBoundingClientRect();
        const imageRect = previewImage.getBoundingClientRect();
        
        let x = e.clientX - offsetX - panelRect.left + panel.scrollLeft;
        let y = e.clientY - offsetY - panelRect.top + panel.scrollTop;
        
        x = Math.max(0, Math.min(x,image.width - box.offsetWidth));
        y = Math.max(0, Math.min(y,image.height - box.offsetHeight));
        
        //const x = e.clientX - offsetX;
        //const y = e.clientY - offsetY;
        
        box.style.left = `${x}px`;
        box.style.top = `${y}px`;
        
        console.log(`x: ${x}, y: ${y}`);
  
    }
    
    function onMouseUp() {
        
        document.removeEventListener("mousemove", onMouseMove);
        document.removeEventListener("mouseup", onMouseUp);
        box.style.cursor = "grab";
  
    }
    
    
    //getAllPhotos();
});

// Event listener for the upload button
document.getElementById('scalePhoto').addEventListener('click', scalePhoto);

//document.querySelector('.upload-button').addEventListener('click', uploadPhoto);

// Event listener for the save button
/*document.querySelector('.save').addEventListener('click', (event) => {
    savePhotoConfig(event.target.dataset.photoId);
});*/
document.querySelector('.save').addEventListener('click', savePhotoConfig);
document.getElementById('fileInput').addEventListener('change', function(){
    if(this.files.length > 0){
        uploadPhotos(this.files);
    }
});


