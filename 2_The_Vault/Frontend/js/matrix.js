// --- Three.js Matrix Digital Rain ---

// 1. Scene, Camera, Renderer Setup
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({
    canvas: document.querySelector('#bg'),
});

renderer.setPixelRatio(window.devicePixelRatio);
renderer.setSize(window.innerWidth, window.innerHeight);
camera.position.setZ(30);

// 2. Create the Particles (Rain)
const particleCount = 10000;
const particles = new THREE.BufferGeometry();
const positions = new Float32Array(particleCount * 3); // x, y, z for each particle

for (let i = 0; i < particleCount * 3; i++) {
    positions[i] = (Math.random() - 0.5) * 100; // Random positions in a cube
}

particles.setAttribute('position', new THREE.BufferAttribute(positions, 3));

const particleMaterial = new THREE.PointsMaterial({
    color: 0x00ff41, // Hacker green
    size: 0.1,
    transparent: true,
    opacity: 0.7,
});

const rain = new THREE.Points(particles, particleMaterial);
scene.add(rain);

// 3. Animation Loop
function animate() {
    requestAnimationFrame(animate);

    // Animate the rain falling
    rain.geometry.attributes.position.array.forEach((y, i) => {
        if (i % 3 === 1) { // We only modify the y-coordinate
            rain.geometry.attributes.position.array[i] -= 0.1;

            // If particle is off-screen, move it back to the top
            if (rain.geometry.attributes.position.array[i] < -50) {
                rain.geometry.attributes.position.array[i] = 50;
            }
        }
    });
    rain.geometry.attributes.position.needsUpdate = true;

    renderer.render(scene, camera);
}

// 4. Handle Window Resize
window.addEventListener('resize', onWindowResize, false);
function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

// Start the animation
animate();