import * as THREE from 'three';

const scene = new THREE.Scene();
scene.background = new THREE.Color(0xffffff);
scene.fog = new THREE.Fog(0xffffff, 20, 70); // fog color, near value, far value

const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(window.devicePixelRatio);

camera.position.z = 0;
document.getElementById('splash').appendChild(renderer.domElement);

// Generate filenames
const numImg = 61;
const imageFilenames = [];
for (let i = 1; i <= numImg; i++) {
    const filename = `img/${String(i).padStart(3, '0')}.jpg`;
    imageFilenames.push(filename);
}

const loader = new THREE.TextureLoader();

// Params to define spread of images in front of the camera
const imageSpread = {
    x: 15,
    y: 10,
    z: -48,
    depth: 140,
};

const imageMeshes = [];
const defaultSize = 3;
const maxTilt = -15 * Math.PI / 180;

function isTooClose(newPosition, existingMeshes, minDistance) {
    for (const mesh of existingMeshes) {
        if (newPosition.distanceTo(mesh.position) < minDistance) {
            return true;
        }
    }
    return false;
}

const minDistance = 8; // Minimum distance between images, adjust as needed

imageFilenames.forEach((imagePath) => {
    loader.load(imagePath, (texture) => {
        const aspectRatio = texture.image ? texture.image.width / texture.image.height : 1;
        const geometry = new THREE.PlaneGeometry(aspectRatio * defaultSize, defaultSize);
        const material = new THREE.MeshBasicMaterial({ map: texture, side: THREE.DoubleSide, transparent: true, opacity: 1.0 });
        const mesh = new THREE.Mesh(geometry, material);

        let position;

        do {
            position = new THREE.Vector3(
                (Math.random() - 0.5) * imageSpread.x * 2,
                (Math.random() - 0.5) * imageSpread.y * 2,
                camera.position.z + imageSpread.z - Math.random() * imageSpread.depth
            );
        } while (isTooClose(position, imageMeshes, minDistance));

        mesh.position.copy(position);

        const tiltRatio = mesh.position.x / (imageSpread.x * 2);
        mesh.rotation.y = maxTilt * tiltRatio;

        scene.add(mesh);
        imageMeshes.push(mesh);
    }, undefined, () => {
        console.error('Error loading image:', imagePath);
    });
});

// Function to reposition an image
function repositionImage(mesh) {
    mesh.position.x = (Math.random() - 0.5) * imageSpread.x * 2;
    mesh.position.y = (Math.random() - 0.5) * imageSpread.y * 2;
    mesh.position.z = camera.position.z + imageSpread.z - imageSpread.depth;

    // Apply tilt based on x position
    const tiltRatio = mesh.position.x / (imageSpread.x * 2);
    mesh.rotation.y = maxTilt * tiltRatio;
}

function shuffle(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
}

// Animation loop
function animate() {
    requestAnimationFrame(animate);

    camera.position.z -= 0.04; // camera speed rate

    shuffle(imageMeshes);

    imageMeshes.forEach((mesh) => {
        const distance = Math.abs(mesh.position.z - camera.position.z);
        const fadeStart = 8;
        const fadeEnd = -2;

        if (distance <= fadeStart) {
            mesh.material.opacity = Math.max(0, (distance - fadeEnd) / (fadeStart - fadeEnd));
        }
        if (mesh.position.z > camera.position.z) {
            repositionImage(mesh);
            mesh.material.opacity = 1.0;
        }
    });

    renderer.render(scene, camera);
}

animate();

let lastTime = 0;
const maxAngle = 8 * Math.PI / 180;
let centerX = window.innerWidth / 2;
let centerY = window.innerHeight / 2;
let rotationX = 0, rotationY = 0;
const smoothingFactor = 0.02; // Adjust this value for more or less smoothing

function updateCamera(timestamp) {
    if (timestamp - lastTime > 10) {
        // Linear Interpolation for smooth transition
        camera.rotation.x += (rotationX - camera.rotation.x) * smoothingFactor;
        camera.rotation.y += (rotationY - camera.rotation.y) * smoothingFactor;

        lastTime = timestamp;
    }
    requestAnimationFrame(updateCamera);
}

document.addEventListener('mousemove', (event) => {
    const deltaX = (event.clientX - centerX) / centerX;
    const deltaY = (event.clientY - centerY) / centerY;

    rotationX = -maxAngle * Math.max(-1, Math.min(1, deltaY));
    rotationY = -maxAngle * Math.max(-1, Math.min(1, deltaX));
});

requestAnimationFrame(updateCamera);

window.addEventListener('resize', () => {
    centerX = window.innerWidth / 2;
    centerY = window.innerHeight / 2;
});

