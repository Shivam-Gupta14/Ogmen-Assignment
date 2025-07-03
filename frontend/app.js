async function loadDevices() {
    try {
        const response = await fetch('http://api:8000/devices/');
        const devices = await response.json();
        const select = document.getElementById('deviceSelect');
        devices.forEach(device => {
            const option = document.createElement('option');
            option.value = device.device_id;
            option.textContent = device.device_name;
            select.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading devices:', error);
    }
}

async function loadDeviceData() {
    const deviceId = document.getElementById('deviceSelect').value;
    if (!deviceId) return;

    try {
        const latestResponse = await fetch(`http://api:8000/metrics/${deviceId}/data/?limit=10`);
        const latestData = await latestResponse.json();
        const latestBody = document.getElementById('latestDataBody');
        latestBody.innerHTML = '';
        latestData.forEach(data => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${data.metric_name}</td>
                <td>${data.value} ${data.metric_name.includes('battery') ? '%' : data.metric_name.includes('temperature') ? '°C' : data.metric_name.includes('feed_dispensed') ? 'g' : data.metric_name.includes('duration') ? 'min' : ''}</td>
                <td>${new Date(data.recorded_at).toLocaleString()}</td>
            `;
            latestBody.appendChild(row);
        });

        const summaryResponse = await fetch(`http://api:8000/metrics/${deviceId}/summary/`);
        const summaryData = await summaryResponse.json();
        const summaryBody = document.getElementById('summaryDataBody');
        summaryBody.innerHTML = '';
        Object.entries(summaryData).forEach(([metric, values]) => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${metric}</td>
                <td>${values.avg ? values.avg.toFixed(2) : '-'}</td>
                <td>${values.min ? values.min.toFixed(2) : '-'}</td>
                <td>${values.max ? values.max.toFixed(2) : '-'}</td>
                <td>${values.latest}</td>
            `;
            summaryBody.appendChild(row);
        });

        const commandResponse = await fetch(`http://api:8000/commands/${deviceId}/?limit=5`);
        const commandLogs = await commandResponse.json();
        const commandBody = document.getElementById('commandLogsBody');
        commandBody.innerHTML = '';
        commandLogs.forEach(log => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${log.command}</td>
                <td>${log.status}</td>
                <td>${new Date(log.created_at).toLocaleString()}</td>
            `;
            commandBody.appendChild(row);
        });

        const ws = new WebSocket(`ws://api:8000/ws/telemetry/${deviceId}`);
        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            const latestBody = document.getElementById('latestDataBody');
            data.forEach(item => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${item.metric_name}</td>
                    <td>${item.value} ${item.metric_name.includes('battery') ? '%' : item.metric_name.includes('temperature') ? '°C' : item.metric_name.includes('feed_dispensed') ? 'g' : item.metric_name.includes('duration') ? 'min' : ''}</td>
                    <td>${new Date(item.recorded_at).toLocaleString()}</td>
                `;
                latestBody.insertBefore(row, latestBody.firstChild);
            });
        };
    } catch (error) {
        console.error('Error loading device data:', error);
    }
}

async function sendCommand(command) {
    const deviceId = document.getElementById('deviceSelect').value;
    if (!deviceId) {
        alert('Please select a device');
        return;
    }
    try {
        await fetch(`http://api:8000/commands/${deviceId}/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ command })
        });
        loadDeviceData();
    } catch (error) {
        console.error('Error sending command:', error);
        alert('Failed to send command');
    }
}

window.onload = loadDevices;
