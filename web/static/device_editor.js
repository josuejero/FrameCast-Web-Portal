
let digitalPhotoFrameCollection = [];
let digitalPhotoCollection = [];
let selectedDeviceIndex = 0;
let selectedPhotoIndex = 0;
let selectedAssignedPhotoIndex = -1;

// Event listener for when the document content is loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log("Document loaded, fetching initial data...");
    loadPhotos();
    loadDevices();
});


// Start Dan's code

async function loadDevices(){
    
    try{
        const response = await fetch('/get_device_config');
        const data = await response.json();
        digitalPhotoFrameCollection = data;
    } catch (error){
        console.error('Error fetching data:', error)
    }
    
    /*fetch('/get_device_config')
        .then(response => response.json())
        .then(data => {
            digitalPhotoFrameCollection = data;
                    console.log(data);
            populateDeviceList(digitalPhotoFrameCollection);
        })
        .catch(error => console.error('Error fetching data:', error));*/
        
    populateDeviceList(digitalPhotoFrameCollection);
    if(selectedDeviceIndex < digitalPhotoFrameCollection.length){
        populateDeviceFields(digitalPhotoFrameCollection[selectedDeviceIndex]); 
    }

}

function populateDeviceList(digitalPhotoFrameCollection){
    
    const deviceList = document.getElementById('device-list');
    deviceList.innerHTML = '';
    
    let lastSelectedDevice = null;
    
    digitalPhotoFrameCollection.forEach((device, index) => {
 
        const listItem = document.createElement('li');
        listItem.classList.add('list-item');
        listItem.textContent = device['Name'];
        listItem.addEventListener('click', () => {
            listItem.classList.toggle('selected');
            
            if(listItem.classList.contains('selected')){
                if(lastSelectedDevice && lastSelectedDevice !== listItem){
                    lastSelectedDevice.classList.remove('last-selected');
                } 
                
                listItem.classList.add('last-selected');
                lastSelectedDevice = listItem;
                
            } else {
                if(lastSelectedDevice === listItem){
                    listItem.classList.remove('last-selected');
                    lastSelectedDevice = null;
                }
            }
            
            selectedDeviceIndex = index;
            populateDeviceFields(device);
        });
        
        deviceList.appendChild(listItem);
    });
    
    
}

function populateDeviceFields(device) {
    
    document.getElementById('device-name').value = device['Name'];
    document.getElementById('photo-update-frequency').value = device['Update Frequency'];
    document.getElementById('random-order').checked = device['Randomize'];
    
    const assignedPhotoList = document.getElementById('assigned-photo-list');
    const assignedPhotos = assignedPhotoList.getElementsByClassName('list-item');
    assignedPhotoList.innerHTML = '';
    
    let lastSelectedAssignedPhoto = null;

    device['Photo List'].forEach((photo,index) => {
        
        const listItem = document.createElement('li');
        listItem.classList.add('list-item');
        listItem.textContent = photo;
        listItem.addEventListener('click', () => {
            listItem.classList.toggle('selected');
            if(listItem.classList.contains('selected')){
                if(lastSelectedAssignedPhoto && lastSelectedAssignedPhoto !== listItem){
                    lastSelectedAssignedPhoto.classList.remove('last-selected');
                } 
                
                listItem.classList.add('last-selected');
                lastSelectedAssignedPhoto = listItem;
                
            } else {
                if(lastSelectedAssignedPhoto === listItem){
                    listItem.classList.remove('last-selected');
                    lastSelectedAssignedPhoto = null;
                }
            }
            selectedAssignedPhotoIndex = index;
            showAssignedPhotoPreview(photo);
        });
        assignedPhotoList.appendChild(listItem);
    });

}

function loadPhotos(){
    
    fetch('/get_photo_config')
        .then(response => response.json())
        .then(data => {
            digitalPhotoCollection = data;
            
            populatePhotoList(digitalPhotoCollection);
        })
        .catch(error => console.error('Error fetching data:', error));
}

function populatePhotoList(digitalPhotoCollection){
    
    const photoList = document.getElementById('photo-list');
    photoList.innerHTML = '';
    
    let lastSelectedPhoto = null;
    
    digitalPhotoCollection.forEach((photo, index) => {

        const listItem = document.createElement('li');
        listItem.classList.add('list-item');
        listItem.textContent = photo['Name'];
        listItem.addEventListener('click', () => {
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
            showPhotoPreview(photo);
            
            //selectedIndex = index;
            //populateDeviceFields(device);
        });
        
        photoList.appendChild(listItem);
    });
}

function showPhotoPreview(photo){
    
    
    const photoObject = document.getElementById("photo-preview");
     
    const photoName = photo["Name"];

    const newSrc = `../../photo_preview/${photoName}`;
    
    photoObject.src = newSrc;
    photoObject.style.display = 'block';
  
}

function showAssignedPhotoPreview(photo){
    
    
    const photoObject = document.getElementById("assigned-photo-preview");
     
    const photoName = photo;

    const newSrc = `../../photo_preview/${photoName}`;
    
    photoObject.src = newSrc;
    photoObject.style.display = 'block';
  
}



async function addPhotosToDevices(){
    
    let selectedPhotos = getSelectedPhotos();
    let selectedDevices = getSelectedDevices();
    
    for (let i = 0; i < selectedDevices.length; i++){
        
       let deviceIndex = selectedDevices[i];
       
       let device = digitalPhotoFrameCollection[deviceIndex]
       let existingPhotos = device['Photo List'];
       //console.log(existingPhotos);
       let uniquePhotos = selectedPhotos.filter(item => !existingPhotos.includes(item));
       //console.log(uniquePhotos);
       let combinedPhotos = existingPhotos.concat(uniquePhotos);
       //console.log(combinedPhotos);
       
       let deviceConfig = {
            "Device Index":deviceIndex,
            "Device Name": device['Name'],
            "Update Frequency": device['Update Frequency'],
            "Randomize": device['Randomize'],
            "Photo List": combinedPhotos
        };

        console.log("Saving device configuration:", deviceConfig);

        try{
            const response = await fetch('/api/save_device_config', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(deviceConfig)
            });
            const data = await response.json();
            console.log("Save response:", data);
            digitalPhotoFrameCollection = data;
        } catch (error){
            console.error('Error saving device configuration:', error)
        }
        
    }
    

    populateDeviceList(digitalPhotoFrameCollection)
    if(selectedDeviceIndex < digitalPhotoFrameCollection.length){
        populateDeviceFields(digitalPhotoFrameCollection[selectedDeviceIndex]); 
    }
}

async function removePhotosFromDevice(){
    
    let selectedAssignedPhotos = getSelectedAssignedPhotos();
    console.log(selectedAssignedPhotos);
    let device = digitalPhotoFrameCollection[selectedDeviceIndex];
    let assignedPhotos = device['Photo List'];
    console.log(assignedPhotos);
    let truncatedPhotos = assignedPhotos.filter(item => !selectedAssignedPhotos.includes(item));
    console.log(truncatedPhotos);
    
    let deviceConfig = {
        "Device Index":selectedDeviceIndex,
        "Device Name": device['Name'],
        "Update Frequency": device['Update Frequency'],
        "Randomize": device['Randomize'],
        "Photo List": truncatedPhotos
    };

    console.log("Saving device configuration:", deviceConfig);

    try{
        const response = await fetch('/api/save_device_config', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(deviceConfig)
        });
        const data = await response.json();
        console.log("Save response:", data);
        digitalPhotoFrameCollection = data;
    } catch (error){
        console.error('Error saving device configuration:', error)
    }
    
    populateDeviceList(digitalPhotoFrameCollection)
    if(selectedDeviceIndex < digitalPhotoFrameCollection.length){
        populateDeviceFields(digitalPhotoFrameCollection[selectedDeviceIndex]); 
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

function getSelectedAssignedPhotos() {
    
    const assignedPhotoList = document.getElementById('assigned-photo-list');
    const photos = assignedPhotoList.getElementsByClassName('list-item');
    const selectedPhotos = [];
    Array.from(photos).forEach(photo => {
        if (photo.classList.contains('selected')) {
            selectedPhotos.push(photo.textContent);
        }
    });
    
    return selectedPhotos;
}

function getSelectedDevices() {
    
    const deviceList = document.getElementById('device-list');
    const devices = deviceList.getElementsByClassName('list-item');
    const selectedIndices = [];
    Array.from(devices).forEach((device, index) => {
        if (device.classList.contains('selected')) {
            selectedIndices.push(index);
        }
    });
    
    return selectedIndices;
 
}

// End Dan's code


/**
 * Save the device configuration to the server
 */
async function saveDevice() {
    
    let deviceName = document.getElementById('device-name').value;
    let photoUpdateFrequency = document.getElementById('photo-update-frequency').value;
    let randomOrder = document.getElementById('random-order').checked;
    
    const assignedPhotoList = document.getElementById('assigned-photo-list');
    const photosInList = assignedPhotoList.getElementsByClassName('list-item');
    const assignedPhotos = []
    Array.from(photosInList).forEach(photo => {
        assignedPhotos.push(photo.textContent);
    });
    
    console.log(assignedPhotos);
    
    

    let deviceConfig = {
        "Device Index":selectedDeviceIndex,
        "Device Name": deviceName,
        "Update Frequency": photoUpdateFrequency,
        "Randomize": randomOrder,
        "Photo List": assignedPhotos
    };

    console.log("Saving device configuration:", deviceConfig);

    try{
        const response = await fetch('/api/save_device_config', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(deviceConfig)
        });
        const data = await response.json();
        console.log("Save response:", data);
        digitalPhotoFrameCollection = data;
        /*if (data.success) {
            alert('Device configuration saved successfully');
            digitalPhotoFrameCollection = data;
        }*/
    } catch (error){
        console.error('Error saving device configuration:', error)
    }

    populateDeviceList(digitalPhotoFrameCollection)
    if(selectedDeviceIndex < digitalPhotoFrameCollection.length){
        populateDeviceFields(digitalPhotoFrameCollection[selectedDeviceIndex]); 
    }

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



/**
 * Move a selected photo up or down in the list
 * @param {string} direction - The direction to move the photo ('up' or 'down')
 */
async function movePhoto(direction) {
         
    
    const assignedPhotoList = document.getElementById('assigned-photo-list');
    const photos = assignedPhotoList.getElementsByClassName('list-item');
    let selectedPhotoIndex = -1;
    Array.from(photos).forEach((photo, index) => {
        if (photo.classList.contains('last-selected')) {
            selectedPhotoIndex = index;
        }
    });
    
    console.log(selectedPhotoIndex);
    
    let device = digitalPhotoFrameCollection[selectedDeviceIndex];
    let assignedPhotos = device['Photo List'];
    console.log(assignedPhotos);
    
    if(
        selectedPhotoIndex === -1 || 
        (selectedPhotoIndex === 0 && direction === 'up') ||
        (selectedPhotoIndex === assignedPhotos.length-1 && direction === 'down')){
        return;
    }

    let newIndex = direction === 'up' ? selectedPhotoIndex -1 : selectedPhotoIndex +1;
    let selectedPhoto = assignedPhotos[selectedPhotoIndex];
    console.log(selectedPhotoIndex);
    console.log(assignedPhotos[selectedPhotoIndex]);
    
    assignedPhotos.splice(selectedPhotoIndex, 1);
    assignedPhotos.splice(newIndex, 0, selectedPhoto);
    console.log(assignedPhotos);
    
    assignedPhotoList.innerHTML = '';
    
    let lastSelectedAssignedPhoto = null;

    assignedPhotos.forEach((photo,index) => {
        
        const listItem = document.createElement('li');
        listItem.classList.add('list-item');
        listItem.textContent = photo;
        listItem.addEventListener('click', () => {
            listItem.classList.toggle('selected');
            if(listItem.classList.contains('selected')){
                if(lastSelectedAssignedPhoto && lastSelectedAssignedPhoto !== listItem){
                    lastSelectedAssignedPhoto.classList.remove('last-selected');
                } 
                
                listItem.classList.add('last-selected');
                lastSelectedAssignedPhoto = listItem;
                
            } else {
                if(lastSelectedAssignedPhoto === listItem){
                    listItem.classList.remove('last-selected');
                    lastSelectedAssignedPhoto = null;
                }
            }
            selectedAssignedPhotoIndex = index;
            showAssignedPhotoPreview(photo);
        });
        assignedPhotoList.appendChild(listItem);
        if(index===newIndex){
            listItem.classList.add('selected');
            listItem.classList.add('last-selected');
        }
    });
    
}
 

// Event listeners for buttons
document.querySelector('.add-to-devices').addEventListener('click', addPhotosToDevices);
document.querySelector('.save-config').addEventListener('click', saveDevice);
document.querySelector('.move-up').addEventListener('click', () => movePhoto('up'));
document.querySelector('.move-down').addEventListener('click', () => movePhoto('down'));
document.querySelector('.remove').addEventListener('click', removePhotosFromDevice);
