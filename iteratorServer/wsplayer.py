from room import roomsContainer
from aiohttp import web
import asyncio
import aiohttp
import room
import classes
import json


class WSPlayer(web.View):
    def __init__(self, request):
        self.roomsContainer = roomsContainer
        self.room: 'classes.Room' = None
        self.player: 'classes.Player' = None
        self._request = request
        ws = None

    async def createRoom(self, 
            ws,
            data: dict):
        await asyncio.sleep(0)
        room = self.roomsContainer.createRoom(data['passwd'], data['minPl'], data['maxPl'])
        self.room = None
        self.player = None
        if room:
            self.room = room
            self.room.wsPlayers.append(ws)
            return {'e': 'create', 'm': 'roomID ' + str(self.room.id)}
        return {'e': 'create', 'm': 'error'}

    async def connectRoom(self, 
            ws,
            data: dict):
        await asyncio.sleep(0)
        room = self.roomsContainer.connectRoomPlayer(data['roomID'], data['passwd'])
        self.room = None
        self.player = None
        if room:
            self.room = room
            self.room.wsPlayers.append(ws)
            return {'e': 'connect', 'm': 'ok'}
        return {'e': 'connect', 'm': 'error'}

    async def createPlayer(self, 
            ws,
            data: dict):
        await asyncio.sleep(0)
        if self.room:
            player = self.room.createPlayer(data['name'])
            self.player = None
            if player:
                self.player = player
                return {'e': 'createPl', 'm': 'ok'}
        return {'e': 'createPl', 'm': 'error'}

    async def getUpdate(self, 
            ws,
            data: dict):
        await asyncio.sleep(0)
        if self.player:
            self.player.look()
            self.player.lookForward()
            self.player.lookLeft()
            self.player.lookRight()
            a = {'e': 'getUpdate'}
            a.update(self.player.getData())
            return a
        return {'e': 'getUpdate', 'm': 'error'}

    async def updatePlayer(self, 
            ws,
            data: dict):
        if self.player:
            dispatcher = {
                'skip': self.player.look,
                'move': self.player.move,
                'turnLeft': self.player.turnLeft,
                'turnRight': self.player.turnRight
            }
            dispatcher[data['do']]()
            plData = self.player.getData()
            await self.room.sendToBrowsers({
                'e': 'getUpdate',
                'id': plData['id'],
                'type': plData['type'],
                'pos': plData['pos'],
                'rot': plData['rot']
            })
            return {'e': 'updatePl', 'm': 'ok'}
        return {'e': 'updatePl', 'm': 'error'}

    async def get(self):
        ws = web.WebSocketResponse()
        await ws.prepare(self.request)
        dispatcher = {
            'create': self.createRoom,
            'connect': self.connectRoom,
            'createPl': self.createPlayer,
            'getUpdate': self.getUpdate,
            'updatePl': self.updatePlayer
        }
        #
        async for msg in ws:
            if msg.type == web.WSMsgType.text:
                if msg.data == 'close':
                    await ws.close()
                else:
                    event = json.loads(msg.data)
                    if ws.closed:
                        print(f'ws player connection closed')
                        self.room.wsPlayers.remove(ws)
                        await ws.close()
                    else:
                        await ws.send_json(await dispatcher[event['e']](ws=ws, data=event))
            elif msg.type == web.WSMsgType.error:
                print(f'error {ws.exception()}')
        #
        self.room.wsPlayers.remove(ws)
        print(f'ws player connection closed')
        return ws
