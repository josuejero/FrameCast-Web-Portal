// Object to store discovered Bluetooth devices
let discoveredDevices = {};

// Event listener for when the document content is loaded
document.addEventListener('DOMContentLoaded', () => {
    findWiFiDevices();
});

/**
 * Function to find new Bluetooth devices that are discoverable
 */
function findNewDevices() {
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
}

/**
 * Function to invite discovered Bluetooth devices to join the network
 */
function inviteToNetwork() {
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
}

/**
 * Function to find devices connected to the WiFi network
 */
function findWiFiDevices() {
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
}
