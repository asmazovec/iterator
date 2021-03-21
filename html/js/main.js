import * as THREE from 'https://threejsfundamentals.org/threejs/resources/threejs/r119/build/three.module.js';
import { GUI } from 'https://threejsfundamentals.org/threejs/../3rdparty/dat.gui.module.js';
import { room, roomController } from './websocket.js'
import { scene } from './classes.js'


const canvas = document.querySelector('#c');

const fov = 60;
const aspect = 2;
const near = 1;
const far = 300;


let renderer = new THREE.WebGLRenderer({canvas});
renderer.shadowMapEnabled = true;


let camera = new THREE.PerspectiveCamera(fov, aspect, near, far);
camera.position.set(0, 50, 0);
camera.lookAt(0, 0, 0);
let clock = new THREE.Clock();
let angle = 0; // текущий угол камеры
let angularSpeed = THREE.Math.degToRad(5); // угловая скорость
let delta = 0;
let radius = 80;


let gui = new GUI();
gui.add(roomController, 'roomID');
gui.add(roomController, 'connect');
gui.add(roomController, 'disconnect');
gui.add(roomController, 'start');


let spotLight = new THREE.SpotLight(0xffffff );
spotLight.position.set( -40, 60, -10 );
spotLight.castShadow = true;
scene.add(spotLight );


let planeGeometry = new THREE.PlaneGeometry(100,100);
let planeMaterial = new THREE.MeshLambertMaterial({color: 0xffffff});
let plane = new THREE.Mesh(planeGeometry,planeMaterial);
plane.rotation.x = -0.5*Math.PI;
plane.position.x = 0;
plane.position.y = 0;
plane.position.z = 0;
plane.receiveShadow = true;
scene.add(plane);


function resizeRendererToDisplaySize(renderer) {
    const canvas = renderer.domElement;
    const width  = canvas.clientWidth;
    const height = canvas.clientHeight;
    const needResize = canvas.width !== width || canvas.height !== height;
    if (needResize) {
        renderer.setSize(width, height, false);
    }
    return needResize;
}

function renderScene() {
    camera.position.x = Math.cos(angle) * radius;
    camera.position.z = Math.sin(angle) * radius;
    angle += angularSpeed * delta;

    camera.lookAt(0, 0, 0);

    if(resizeRendererToDisplaySize(renderer)) {
        const canvas = renderer.domElement;
        camera.aspect = canvas.clientWidth / canvas.clientHeight;
        camera.updateProjectionMatrix();
    }
    for(let obj in room.objects) {
        room.objects[obj].move();
    }

	renderer.render(scene, camera);
    delta = clock.getDelta();
    requestAnimationFrame(renderScene);
}

renderScene();
