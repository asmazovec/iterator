from aiohttp import web
from gameObject import *
from api import *
from aiojobs.aiohttp import setup, spawn, atomic
import aiohttp
import asyncio
import json


async def ws_render(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    
    async for msg in ws:     
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            else:
                message = json.loads(msg.data)
                await render_api(ws, message)
                
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print(f'ws connection closed with exception {ws.exception()}')

    print('browser connection closed')

    return ws


async def ws_api(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    
    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            else:
                message = json.loads(msg.data)
                await game_api(ws, message)

        elif msg.type == aiohttp.WSMsgType.ERROR:
            print(f'ws connection closed with exception {ws.exception}')

    print('API connection closed')

    return ws









