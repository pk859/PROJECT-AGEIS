// --- CONFIGURATION ---
const API_URL = "/health"; 
const healthBar = document.getElementById('health-bar');
const healthVal = document.getElementById('health-val');
const statusText = document.getElementById('status-text');
const logFeed = document.getElementById('log-feed');

// Video Elements
const vidProgress = document.getElementById('vid-progress');
const vidFinal = document.getElementById('vid-final');
const vidBreach = document.getElementById('vid-breach'); // Data Breach Video
let isHackSequenceStarted = false;

// --- 1. CLOCK ---
setInterval(() => {
    document.getElementById('clock').innerText = new Date().toLocaleTimeString('en-US', { hour12: false });
}, 1000);

// --- 2. MODAL SWITCHER ---
window.showModal = function(id) {
    document.getElementById('map-view').style.display = 'none';
    document.querySelectorAll('.modal-window').forEach(el => el.style.display = 'none');
    
    const target = document.getElementById(id);
    if(target) {
        target.style.display = id === 'map-view' ? 'block' : 'flex';
    }
    document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
};
document.getElementById('map-view').style.display = 'block';

// --- 3. LOGS & ANALYTICS ---
function addLog(msg, type="INFO") {
    const div = document.createElement('div');
    div.className = 'log-entry';
    const color = type === "ALERT" ? "color:red" : (type === "WARN" ? "color:orange" : "");
    div.innerHTML = `<span style="${color}">[${type}]</span> ${msg}`;
    logFeed.prepend(div);
    if(logFeed.children.length > 20) logFeed.lastChild.remove();
}

const logMessages = [
    "Packet Filtered: 192.168.0.X", "Handshake Verified", "Port 443 Traffic Normal", 
    "Geo-IP Scan: Frankfurt", "Geo-IP Scan: Tokyo", "Database Query OK", 
    "Session Authenticated"
];

setInterval(() => {
    if(!document.body.classList.contains('hacked')) {
        if(Math.random() > 0.5) {
            addLog(logMessages[Math.floor(Math.random() * logMessages.length)], "INFO");
        }
        // Random Stats
        const httpStat = document.getElementById('http-stat');
        if(httpStat) httpStat.innerText = Math.floor(40000 + Math.random() * 5000) + "/s";
        
        const sqlStat = document.getElementById('sql-stat');
        if(sqlStat) sqlStat.innerText = Math.floor(1000 + Math.random() * 300) + "/s";

        document.querySelectorAll('.bar').forEach(bar => {
            bar.style.height = Math.floor(Math.random() * 100) + "%";
        });
    }
}, 800);

// --- 4. BACKEND HEALTH CHECK & VIDEO LOGIC ---
async function checkSystemHealth() {
    try {
        const response = await fetch(API_URL);
        const data = await response.json();
        
        healthVal.innerText = data.health + "%";
        healthBar.style.width = data.health + "%";

        // =================================================
        // SCENARIO A: SERVER CRASH (Health <= 0)
        // =================================================
        if (data.health <= 0) {
            if (!isHackSequenceStarted) {
                isHackSequenceStarted = true;
                document.body.classList.add('hacked');
                statusText.innerText = "CRITICAL BREACH";
                statusText.style.color = "red";
                
                const overlay = document.getElementById('hacked-overlay');
                overlay.style.background = "rgba(0, 0, 0, 0.85)"; // Transparent for popup
                
                // 1. FORCE STOP Breach Video (Just in case)
                if(vidBreach) {
                    vidBreach.style.display = 'none';
                    vidBreach.pause();
                }

                // 2. Play Loading Sequence
                vidProgress.style.display = 'block';
                vidProgress.currentTime = 0;
                vidProgress.play();
                
                // 3. Chain to Final Video ONLY here
                vidProgress.onended = function() {
                    // Double check we are still in "Crash Mode"
                    if(document.body.classList.contains('hacked') && statusText.innerText === "CRITICAL BREACH") {
                        overlay.style.background = "black";
                        vidProgress.style.display = 'none';
                        vidFinal.style.display = 'block';
                        vidFinal.play();
                    }
                };
            }
        } 
        // =================================================
        // SCENARIO B: DATA BREACH (Health == 50)
        // =================================================
        else if (data.health == 50) {
            if (!isHackSequenceStarted) {
                isHackSequenceStarted = true;
                document.body.classList.add('hacked');
                statusText.innerText = "DATA EXFILTRATION";
                statusText.style.color = "orange";

                const overlay = document.getElementById('hacked-overlay');
                overlay.style.background = "black"; // Black immediately

                // 1. FORCE STOP Crash Videos (The Fix)
                // This prevents 'vidProgress.onended' from firing and showing the skull
                vidProgress.pause();
                vidFinal.pause();
                vidProgress.style.display = 'none';
                vidFinal.style.display = 'none';

                // 2. Play Breach Video
                if(vidBreach) {
                    vidBreach.style.display = 'block';
                    vidBreach.currentTime = 0;
                    vidBreach.play();
                }
            }
        }
        // =================================================
        // SCENARIO C: SYSTEM NORMAL
        // =================================================
        else {
            if (isHackSequenceStarted) {
                isHackSequenceStarted = false;
                document.body.classList.remove('hacked');
                statusText.innerText = "SECURE";
                statusText.style.color = "#00f2ff";
                
                // STOP ALL VIDEOS
                vidProgress.pause();
                vidFinal.pause();
                if(vidBreach) vidBreach.pause();
                
                // RESET VISIBILITY
                vidProgress.style.display = 'block'; 
                vidFinal.style.display = 'none';
                if(vidBreach) vidBreach.style.display = 'none';

                const overlay = document.getElementById('hacked-overlay');
                overlay.style.background = "rgba(0, 0, 0, 0.85)";
            }
        }
    } catch (e) {}
}

// --- RASP ALERT SYSTEM ---
let raspAlertActive = false;

async function checkRaspStatus() {
    try {
        // We check the latest incident to see if RASP fired
        const response = await fetch('/incidents');
        const data = await response.json();
        
        if (data.length > 0) {
            const latest = data[0];
            // If the latest log is our RASP Alert and it's fresh (created recently)
            if (latest.title.includes("RASP ALERT") && !raspAlertActive) {
                showAccessDenied();
            }
        }
    } catch (e) {}
}

function showAccessDenied() {
    raspAlertActive = true;
    
    // Create or Find the Overlay
    let overlay = document.getElementById('rasp-overlay');
    if(!overlay) {
        overlay = document.createElement('div');
        overlay.id = 'rasp-overlay';
        overlay.style = `
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(255, 0, 0, 0.4); z-index: 9999;
            display: flex; justify-content: center; align-items: center;
            font-family: 'Rajdhani', sans-serif; pointer-events: none;
        `;
        overlay.innerHTML = `
            <div style="background: black; border: 2px solid red; padding: 40px; text-align: center; color: red;">
                <h1 style="font-size: 3em; margin: 0;">🚫 ACCESS DENIED</h1>
                <p style="font-size: 1.5em; color: white;">RASP PROTOCOL ENGAGED</p>
                <p>Threat Neutralized. Locking Interface...</p>
            </div>
        `;
        document.body.appendChild(overlay);
    }
    
    overlay.style.display = 'flex';

    // Remove it after 15 Seconds
    setTimeout(() => {
        overlay.style.display = 'none';
        raspAlertActive = false;
    }, 15000); // 15000 ms = 15 seconds
}

// Add to your existing Interval
setInterval(checkRaspStatus, 2000);

setInterval(checkSystemHealth, 1000);