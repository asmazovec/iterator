import * as THREE from 'https://threejsfundamentals.org/threejs/resources/threejs/r119/build/three.module.js';


let shift = 10;
let scene = new THREE.Scene();

class GObject {
    constructor(id, type, x, y, rot, geometry, material) {
        this.id = id;
        this.type = type;
        this.x = x;
        this.y = y;
        this.rot = rot;

        this.mesh = new THREE.Mesh(geometry, material);
        this.mesh.position.x = shift * this.x;
        this.mesh.position.z = shift * this.y;
        this.mesh.position.y = 5;
        this.mesh.castShadow = true;

        scene.add(this.mesh);
    }

    setPos(x, y) {
        this.x = x;
        this.y = y;
        return this;
    }

    setRot(rot) {
        this.rot.x = rot.x;
        this.rot.y = rot.y;
        return this;
    }

    move() {
        let dx = (shift * this.x - this.mesh.position.x);
        let dy = (shift * this.y - this.mesh.position.z);
        if(Math.abs(dx) >= 0.01) {
            this.mesh.position.x += Math.tanh(0.4 * dx);
        }
        if(Math.abs(dy) >= 0.01) {
            this.mesh.position.z += Math.tanh(0.4 * dy);
        }
    }

    remove() {
        scene.remove(this.mesh);
    }
}

class Room {
    constructor(roomID) {
        this.id = roomID
        this.objects = {};
        this.connected = false;
        this.iter = 0;
    }

    connectRoom() {
        return {
            e: 'connect',
            roomID: this.id,
        };
    }

    disconnectRoom() {
        for(let obj in this.objects) {
            this.objects[obj].remove();
            delete this.objects[obj];
        }
        this.id = 0;
        this.objects = {};
        this.connected = false;
        this.iter = 0;
    }

    getUpdate() {
        this.iter += 1;
        return {
            e: 'getUpdate',
            iter: this.iter,
        };
    }

    updateObject(objID, type, x, y, rot) {
        if(objID.toString() in this.objects) {
            this.objects[objID.toString()].setPos(x, y).setRot(rot);
        } else {
            let geometry;
            let material;
            if(type == 'player') {
                geometry = new THREE.SphereGeometry(4, 8, 6);
                material = new THREE.MeshLambertMaterial({color: 0x22BB22});
            } else if(type == 'movable') {
                geometry = new THREE.CylinderGeometry(3, 4, 9, 8, 1);
                material = new THREE.MeshLambertMaterial({color: 0xBB2222});
            } else if(type == 'static') {
                geometry = new THREE.BoxGeometry( 10, 6, 10 );
                material = new THREE.MeshLambertMaterial({color: 0xBBBBFF});
            } else {
                geometry = new THREE.SphereGeometry(4, 8, 6);
                material = new THREE.MeshLambertMaterial({color: 0xBBBBFF});
            }
            this.objects[objID.toString()] = new GObject(objID, type, x, y, rot, geometry, material);
        }
    }
}

export { Room, GObject, scene };
