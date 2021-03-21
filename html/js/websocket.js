import * as THREE from 'https://threejsfundamentals.org/threejs/resources/threejs/r119/build/three.module.js';
import { Room, GObject } from './classes.js';

let ws;
let connectID;
let connectDelay = 2000;
let connectTimes = 15;

let timerID;
let gameDelay = 1000;

function wsStart(host='ws://localhost/ws') {
    ws = new WebSocket(host);

    if(connectTimes == 0) {
        alert("Проблемы с подключением к серверу")
        window.location.href = "/error/onServerError.html";
    }

    ws.onopen = function(event) {
        connectTimes = 15;
        clearInterval(connectID);
        if(room.connected) {
            alert("Соединение установлено");
            clearInterval(timerID);
            timerID = setInterval(function() {
                ws.send(JSON.stringify(room.getUpdate()));
            }, gameDelay);
        } else {
            ws.send(JSON.stringify(room.connectRoom()));
        }
    }

    ws.onclose = function(event) {
        if(event.wasClean) {
            alert("Соединение закрыто чисто");
            ws = false;
        } else {
            ws = null;
            clearInterval(timerID);
            connectTimes -= 1;
            connectID = setTimeout(wsStart, connectDelay, host);
        }
    }

    ws.onmessage = function(event) {
        let resp = JSON.parse(event.data)

        if(resp.e == 'connect' && resp.m == 'ok') {
            room.connected = true;
        }
        if('m' in resp) {
            if(resp.m == 'error' && 'iter' in resp) {
                room.iter = resp.iter;
            }
        } else {
            console.log(event.data);
            room.updateObject(resp.id, resp.type, resp.pos.x, resp.pos.y, resp.rot);
        }
    }

    ws.onerror = function(event) {
    }
}
//wsStart('ws://mazovec.ru:8000/ws');


let room = new Room(0);

let roomController = {
    roomID: 0,
    connect: function() {
        if(!room.connected) {
            room.disconnectRoom();
            room.id = this.roomID;
            if(!ws) { wsStart('ws://46.161.155.209/ws'); }
        }
    },
    disconnect: function() {
        if(room.connected) {
            room.disconnectRoom();
            clearInterval(timerID);
            clearTimeout(connectID);
            if(ws) { ws.close(); }
        }
    },
    start: function() {
        if(room.connected) {
            clearInterval(timerID);
            timerID = setInterval(function() {
                if(ws) { ws.send(JSON.stringify(room.getUpdate())); }
            }, gameDelay);
        }
    }
}

export { room, roomController };
