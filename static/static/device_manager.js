// Object to store discovered Bluetooth devices
let digitalPhotoFrameCollection = [];
let discoveredDevices = [];


// Event listener for when the document content is loaded
document.addEventListener('DOMContentLoaded', () => {
    
    const table = document.getElementById('data-table');
    table.addEventListener('click', (event) => {
        const row = event.target.closest('tr');
        if(!row || row.parentNode.nodeName === 'THEAD') return;
        row.classList.toggle('selected');
    });
    
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
        
    refreshDevices();
}

async function refreshDevices(){
    
    try{
        const response = await fetch('/api/enumerate_wifi_devices');
        const data = await response.json();
        digitalPhotoFrameCollection = data;
    } catch (error){
        console.error('Error fetching data:', error)
    }
        
    buildTable(digitalPhotoFrameCollection);
    
}

function buildTable(digitalPhotoFrameCollection) {
    
    const tableBody = document.getElementById('data-table').getElementsByTagName('tbody')[0];
    tableBody.innerHTML = '';
            
    digitalPhotoFrameCollection.forEach(digitalPhotoFrame => {
        const row = document.createElement('tr');
                
        const fields = ['Name','IP Address','Connected'];
                
        fields.forEach(field => {
                    
            const cell = document.createElement('td');
            cell.textContent = digitalPhotoFrame[field];
            row.appendChild(cell);
        });
                
        tableBody.appendChild(row);
    });
}

async function findNewDevices(){
    
    try{
        const response = await fetch('/api/find_discoverable_bluetooth_devices');
        const data = await response.json();
        discoveredDevices = data;
    } catch (error){
        console.error('Error fetching data:', error)
    }

    populateDiscoveredDeviceList(discoveredDevices);
}

function populateDiscoveredDeviceList(discoveredDevices){
    
    const deviceList = document.getElementById('discovered-devices');
    deviceList.innerHTML = '';
    
    discoveredDevices.forEach((device, index) => {
 
        const listItem = document.createElement('li');
        listItem.classList.add('list-item');
        listItem.textContent = device['Host Name'];
        listItem.addEventListener('click', () => {
            listItem.classList.toggle('selected');
        });
        
        deviceList.appendChild(listItem);
    }); 
}

function getSelectedDiscoveredDevices() {
    
    const deviceList = document.getElementById('discovered-devices');
    const devices = deviceList.getElementsByClassName('list-item');
    let devicesToInvite = [];
    Array.from(devices).forEach((device, index) => {
        if (device.classList.contains('selected')) {
            devicesToInvite.push(discoveredDevices[index]);
        }
    });

    return devicesToInvite;
}

async function inviteToNetwork() {

    devicesToInvite = getSelectedDiscoveredDevices();
    
    try{
        const response = await fetch('/api/invite_discovered_devices_to_network', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(devicesToInvite)
        });
        const data = await response.json();
        console.log("Save response:", data);
        digitalPhotoFrameCollection = data;
    } catch (error){
        console.error('Error saving device configuration:', error)
    }
        
    refreshDevices();
    const deviceList = document.getElementById('discovered-devices');
    deviceList.innerHTML = '';
}

async function deleteDevices() {
    
    devicesToDelete = getSelectedNetworkedDevices();
    if(devicesToDelete.length == 0) return;
    
    try{
        const response = await fetch('/api/delete_devices', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(devicesToDelete)
        });
        const data = await response.json();
        console.log("Save response:", data);
        digitalPhotoFrameCollection = data;
    } catch (error){
        console.error('Error saving device configuration:', error)
    }
    
    refreshDevices();
}

function getSelectedNetworkedDevices() {
    
    const table = document.getElementById('data-table');
    
    const devices = table.getElementsByTagName('tr');
    devicesToDelete = [];
    Array.from(devices).forEach((device, index) => {
        if (device.classList.contains('selected')) {
            console.log("Selected device:", digitalPhotoFrameCollection[index-1]);
            devicesToDelete.push(digitalPhotoFrameCollection[index-1]);
        }
    });
    console.log("devicesToDelete:", devicesToDelete);
    return devicesToDelete;
}

// end



/**
 * Function to find new Bluetooth devices that are discoverable
 */
/*unction findNewDevices() {
    fetch('/api/find_discoverable_bluetooth_devices')
        .then(response => response.json())
        .then(data => {
            discoveredDevices = data;
            let discoveredDevicesElement = document.getElementById('discovered-devices');
            if (discoveredDevicesElement) {
                discoveredDevicesElement.innerHTML = '';
                // Populate the discovered devices element with the names of found devices
                for (let mac in data) {
                    let device = data[mac];
                    discoveredDevicesElement.innerHTML += `<p>${device.device_name}</p>`;
                }
            } else {
                console.error('Element "discovered-devices" not found');
            }
        })
        .catch(error => console.error('Error finding new devices:', error));
}*/

/**
 * Function to invite discovered Bluetooth devices to join the network
 */
/*function inviteToNetwork() {
    fetch('/api/invite_to_network', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(Object.keys(discoveredDevices))
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log("Devices successfully invited to network");
                findWiFiDevices();
            } else {
                console.log("Failed to invite devices");
            }
        })
        .catch(error => console.error("Error inviting devices:", error));
}*/

/**
 * Function to find devices connected to the WiFi network
 */
/*function findWiFiDevices() {
    fetch('/api/enumerate_wifi_devices')
        .then(response => response.json())
        .then(data => {
            let networkedDevices = document.getElementById('networked-devices');
            if (networkedDevices) {
                networkedDevices.innerHTML = '';
                // Populate the networked devices element with the details of connected devices
                for (let sn in data) {
                    let device = data[sn];
                    networkedDevices.innerHTML += `
                        <div class="device-item">
                            <p>${device.device_name}</p>
                            <p>${device.device_type}</p>
                            <p>${device.status}</p>
                            <p>${device.ip_address}</p>
                        </div>`;
                }
            } else {
                console.error('Element "networked-devices" not found');
            }
        })
        .catch(error => console.error('Error finding WiFi devices:', error));
}*/



