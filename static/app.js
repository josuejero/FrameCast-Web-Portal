function findNewDevices(){
  fetch('/api/find_discoverable_bluetooth_devices')
  .then(response => response.json())
  .then(data=>{
    let discoveredDevices = document.getElementById('discovered-devices')
    discoveredDevices.innerHTML = '';
    for(let mac in data){
      let device = data[mac]
      discoveredDevices.innerHTML += `<p>${device.device_name}</p>`
    }
  })
}

function inviteToNetwork(){
  let discoveredDevices = document.getElementById('discovered-devices').innerHTML

  if (discoveredDevices.trim() === ""){
    alert("No devices found to invite. Please click 'FIND NEW DEVICES' first.")
    return;
  }

  let selectedDevices = {}
  fetch('/api/invite_to_network', {
    method: 'POST',
    headers:{
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(selectedDevices)
  })
  .then(response => response.json())
  .then(data=>{
    if(data.success){
      findWiFiDevices()
    }
  })
}

function findWiFiDevices(){
  fetch('/api/enumerate_wifi_devices')
  .then(response => response.json())
  .then(data => {
    let networkedDevices = document.getElementById('networked-devices')
    networkedDevices.innerHTML = ''
    for (let sn in data){
      let device = data[sn]
      networkedDevices.innerHTML += `
        <div class="device-item">
            <p>${device.device_name}</p>
            <p>${device.device_type}</p>
            <p>${device.status}</p>
            <p>${device.ip_address}</p>
        </div>`
    }
  })
}