// Function to fetch and display all photos
function getAllPhotos() {
  console.log("Fetching all photos..."); // Log fetch start
  fetch('/api/get_all_photos')
    .then(response => response.json())
    .then(data => {
      console.log("Photos fetched:", data); // Log received data
      let photoList = document.getElementById('photo-list');
      photoList.innerHTML = '';
      for (let id in data) {
        let photo = data[id];
        photoList.innerHTML += `<label><input type="checkbox" name="photo" value="${id}"> ${photo.photo_name}</label>`;
      }
    })
    .catch(error => console.error('Error fetching photos:', error)); // Log errors
}

// Function to fetch and display all devices
function getAllDevices() {
  console.log("Fetching all devices..."); // Log fetch start
  fetch('/api/get_all_devices')
    .then(response => response.json())
    .then(data => {
      console.log("Devices fetched:", data); // Log received data
      let deviceList = document.getElementById('device-list');
      deviceList.innerHTML = '';
      for (let id in data) {
        let device = data[id];
        deviceList.innerHTML += `<label><input type="checkbox" name="device" value="${id}"> ${device.device_name}</label>`;
      }
    })
    .catch(error => console.error('Error fetching devices:', error)); // Log errors
}

// Function to save device configuration
function saveDeviceConfig() {
  let deviceName = document.getElementById('device-name').value;
  let photoUpdateFrequency = document.getElementById('photo-update-frequency').value;
  let randomOrder = document.getElementById('random-order').checked;

  let deviceConfig = {
    device_name: deviceName,
    photo_update_frequency: photoUpdateFrequency,
    random_order: randomOrder
  };

  console.log("Saving device configuration:", deviceConfig); // Log device configuration

  fetch('/api/save_device_config', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(deviceConfig)
  })
    .then(response => response.json())
    .then(data => {
      console.log("Save response:", data); // Log response from server
      if (data.success) {
        alert('Device configuration saved successfully');
      }
    })
    .catch(error => console.error('Error saving device configuration:', error)); // Log errors
}

// Event listener to load data when the page loads
document.addEventListener('DOMContentLoaded', () => {
  console.log("Document loaded, fetching initial data..."); // Log document load
  getAllPhotos();
  getAllDevices();
});

// Additional functionalities
document.querySelector('.add-to-devices').addEventListener('click', () => {
  let selectedPhotos = Array.from(document.querySelectorAll('input[name="photo"]:checked')).map(input => input.value);
  let selectedDevices = Array.from(document.querySelectorAll('input[name="device"]:checked')).map(input => input.value);

  if (selectedPhotos.length === 0 || selectedDevices.length === 0) {
    alert("Please select at least one photo and one device.");
    return;
  }

  console.log("Adding Photos to Devices", selectedPhotos, selectedDevices); // Log selected photos and devices
  // Here you can add the logic to pair the selected photos with the selected devices
});

document.querySelector('.save-config').addEventListener('click', saveDeviceConfig);
