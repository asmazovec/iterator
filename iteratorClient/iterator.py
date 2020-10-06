from classes import player
import aiohttp
import classes



def connector(ws):
    player.createRoom("0000", ws)
    player.createPlayer(ws)

def updater(o):
    o.move()
