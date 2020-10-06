from classes import Player
from aiohttp import *
import aiohttp
import asyncio
import json


player = Player("name")
async def main():
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect('ws://mazovec.ru:8000/api') as ws:

            ####### Регистрация новой комнаты #######
            await player.createRoom(ws, "0000")
            await player.createPlayer(ws)
            #########################################

            dispatch = {
                'create': player.createRoom,
                'connect': player.connectRoom,
                'createPl': player.createPlayer,
                'updatePl': player.updatePlayer,
                'getUpdate': player.getUpdate
            }

            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    if msg.data == 'close':
                        await ws.close()
                        break
                    else:
                        event = json.loads(msg.data)
                        await dispatch[event['e']](ws=ws, data=event)

                elif msg.type == aiohttp.WSMsgType.ERROR:
                    pass


loop = asyncio.get_event_loop()
loop.run_until_complete(main())



