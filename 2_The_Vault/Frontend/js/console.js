const API_URL = 'http://127.0.0.1:5000/incidents';

// --- Function to fetch data from the backend ---
async function fetchIncidents() {
    try {
        const response = await fetch(API_URL);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const incidents = await response.json();
        updateDashboard(incidents);
    } catch (error) {
        console.error("Could not fetch incidents:", error);
    }
}

// --- Function to control the "Targeting System" panel ---
function updateTargetingSystem(incident) {
    const targetIpEl = document.getElementById('target-ip');
    const statusTextEl = document.getElementById('trace-status-text');
    const progressBarEl = document.getElementById('trace-progress-bar');

    targetIpEl.textContent = incident.ip_address;
    
    statusTextEl.textContent = 'INITIATING TRACE...';
    progressBarEl.style.width = '10%';

    setTimeout(() => {
        statusTextEl.textContent = 'ROUTING THROUGH PROXIES...';
        progressBarEl.style.width = '40%';
    }, 1500);

    setTimeout(() => {
        statusTextEl.textContent = 'GEOLOCATING ORIGIN...';
        progressBarEl.style.width = '75%';
    }, 3000);
    
    setTimeout(() => {
        statusTextEl.textContent = `TARGET ACQUIRED: ${incident.country.toUpperCase()}`;
        progressBarEl.style.width = '100%';
    }, 4500);
}

// --- Main function to update the entire dashboard UI ---
function updateDashboard(incidents) {
    // 1. Update top metric boxes
    const totalIncidentsEl = document.getElementById('total-incidents');
    const openIncidentsEl = document.getElementById('open-incidents');
    const highestRiskEl = document.getElementById('highest-risk');

    totalIncidentsEl.textContent = incidents.length;
    openIncidentsEl.textContent = incidents.filter(inc => inc.status === 'open').length;
    
    const maxRisk = incidents.length > 0 ? Math.max(...incidents.map(inc => inc.risk_score)) : '--';
    highestRiskEl.textContent = maxRisk;
    
    if (maxRisk >= 20) {
        highestRiskEl.parentElement.classList.add('critical');
    } else {
        highestRiskEl.parentElement.classList.remove('critical');
    }

    // 2. Find the latest high-risk incident and update the targeting panel
    const latestHighRiskIncident = incidents.find(inc => inc.risk_score >= 20);
    if (latestHighRiskIncident) {
        const currentTargetIp = document.getElementById('target-ip').textContent;
        if (currentTargetIp !== latestHighRiskIncident.ip_address) {
            updateTargetingSystem(latestHighRiskIncident);
        }
    }

    // 3. Update the main incident log table
    const tableBody = document.getElementById('incident-table-body');
    const existingIds = new Set([...tableBody.querySelectorAll('tr')].map(tr => tr.id));
    const fragment = document.createDocumentFragment();

    incidents.sort((a, b) => new Date(b.reported_at) - new Date(a.reported_at));

    incidents.forEach(inc => {
        const row = document.createElement('tr');
        row.id = `incident-${inc.id}`;
        
        const timestamp = new Date(inc.reported_at).toLocaleString();

        let riskClass = 'risk-low';
        if (inc.risk_score >= 20) { riskClass = 'risk-high'; }
        else if (inc.risk_score >= 10) { riskClass = 'risk-medium'; }

        // --- CORRECTED THIS ENTIRE BLOCK to use 'inc' ---
        row.innerHTML = `
            <td>${timestamp}</td>
            <td>${inc.title}</td>
            <td>${inc.incident_type}</td>
            <td>${inc.system_name}</td>
            <td>${inc.ip_address}</td>
            <td class="${riskClass}">${inc.risk_score}</td>
            <td>${inc.status}</td>
        `;

        if (!existingIds.has(row.id)) {
            row.classList.add('new-incident');
        }
        
        fragment.appendChild(row);
    });

    tableBody.innerHTML = '';
    tableBody.appendChild(fragment);
}

// --- Start the process when the page loads ---
document.addEventListener('DOMContentLoaded', () => {
    fetchIncidents();
    setInterval(fetchIncidents, 5000);
});

// Add this to fetch health
async function fetchHealth() {
    try {
        const response = await fetch('/health');
        const data = await response.json();
        
        // Find or create a Health Box on the dashboard
        let healthBox = document.getElementById('server-health-display');
        if (!healthBox) {
            // If it doesn't exist, let's hijack the "Total Incidents" box for now or log it
            console.log("Current Server Health:", data.health);
            // Optional: Update the title of the page to show health
            document.title = `:: SYSTEM HEALTH: ${data.health}% ::`;
        }
        
        if (data.health === 0) {
            document.body.style.background = "red"; // VISUAL CRASH EFFECT
            alert("⚠️ SYSTEM FAILURE: SERVER HAS BEEN BREACHED AND CRASHED!");
        }
    } catch (error) {
        console.error("Health check failed", error);
    }
}

// Update the interval to check health too
setInterval(fetchHealth, 2000);