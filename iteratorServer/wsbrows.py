from room import roomsContainer
from aiohttp import web
import asyncio
import aiohttp
import room
import classes
import json


class WSBrows(web.View):
    def __init__(self, request):
        self.roomsContainer = roomsContainer
        self.room: 'classes.Room' = None
        self._request = request

    async def connectRoom(self, 
            ws,
            data: dict):
        await asyncio.sleep(0)
        room = self.roomsContainer.connectRoomView(data['roomID'])
        self.room = None
        if room:
            self.room = room
            self.room.wsBrows.append(ws)
            return {'e': 'connect', 'm': 'ok'}
        return {'e': 'connect', 'm': 'error'}

    async def getUpdate(self, 
            ws,
            data: dict):
        await asyncio.sleep(0)
        if self.room:
            return await self.room.update(data['iter'])
        return {'e': 'getUpdate', 'm': 'error'}

    async def get(self):
        ws = web.WebSocketResponse()
        await ws.prepare(self.request)
        dispatcher = {
            'connect': self.connectRoom,
            'getUpdate': self.getUpdate
        }
        #
        async for msg in ws:
            if msg.type == web.WSMsgType.text:
                if msg.data == 'close':
                    await ws.close()
                else:
                    event = json.loads(msg.data)
                    if ws.closed:
                        print(f'ws browser connection closed')
                        self.room.wsBrows.remove(ws)
                        await ws.close()
                    else:
                        await ws.send_json(await dispatcher[event['e']](ws=ws, data=event))
            elif msg.type == web.WSMsgType.error:
                print(f'error {ws.exception()}')
        #
        self.room.wsBrows.remove(ws)
        print(f'ws browser connection closed')
        return ws
