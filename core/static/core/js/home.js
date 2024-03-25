console.log("hello world");

// Create a scene
const scene = new THREE.Scene();

// Camera
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.z = 5;

/// Renderer
const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight / 2);

// Embed in HTML DOM
const sceneBox = document.getElementById('scene-box');
sceneBox.appendChild(renderer.domElement);

// Ground Plane
const planeGeometry = new THREE.PlaneGeometry(10, 10);
planeGeometry.rotateX(30);
const planeMaterial = new THREE.MeshBasicMaterial({color : 0x0000ff});
const plane = new THREE.Mesh(planeGeometry, planeMaterial);
scene.add(plane);

// Fog of View
const fogColor = "#000";
const fogNear = 2;
const fogFar = 8;
scene.fog = new THREE.Fog(fogColor, fogNear, fogFar);

// Animation Loop
const animate = () => {
    renderer.render(scene, camera);
    requestAnimationFrame(animate);
}

animate()