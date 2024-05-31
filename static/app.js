let discoveredDevices = {};

document.addEventListener('DOMContentLoaded', () => {
    findWiFiDevices();
});

function findNewDevices() {
    fetch('/api/find_discoverable_bluetooth_devices')
    .then(response => response.json())
    .then(data => {
        discoveredDevices = data;
        let discoveredDevicesElement = document.getElementById('discovered-devices');
        if (discoveredDevicesElement) {
            discoveredDevicesElement.innerHTML = '';
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

function findWiFiDevices() {
    fetch('/api/enumerate_wifi_devices')
    .then(response => response.json())
    .then(data => {
        let networkedDevices = document.getElementById('networked-devices');
        if (networkedDevices) {
            networkedDevices.innerHTML = '';
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
