function getAllPhotos(){
  fetch('/api/get_all_photos')
  .then(response => response.json())
  .then(data => {
    let photoList = document.getElementById('photo-list')
    photoList.innerHTML = ''
    for(let id in data){
      let photo = data[id]
      photoList.innerHTML += `<label><input type="checkbox" name="photo"> ${photo.photo_name}</label>`;
    }
  })
}

function getAllDevices(){
  fetch('/api/get_all_devices')
  .then(response => response.json())
  .then(data => {
    let deviceList = document.getElementById('device-list')
    deviceList.innerHTML = ''
    for (let id in data){
      let device = data[id]
      deviceList.innerHTML += `<label><input type="checkbox" name="device"> ${device.device_name}</label>`;
    }
  })
}

function saveDeviceConfig(){
  let deviceName = document.getElementById('device-name').value
  let photoUpdateFrequency = document.getElementById('photo-update-frequency').value
  let randomOrder = document.getElementById('random-order').checked

  let deviceConfig = {
    device_name: deviceName,
    photo_update_frequency: photoUpdateFrequency,
    random_order: randomOrder
  }

  fetch('/api/save_device_config', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(deviceConfig)
  })
  .then(response => response.json())
  .then(data => {
    if (data.success){
      alert('Device configuration saved successfully')
    }
  })
}

document.addEventListener('DOMContentLoaded', () => {
  getAllPhotos();
  getAllDevices();
})