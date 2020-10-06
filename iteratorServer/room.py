from classes import Static, Player, Movable
from aiohttp import web
from random import *


class Room(object):
    globalID: int = 0
    
    def __init__(self, 
            passwd: str,
            minPlayers: int = 2, 
            maxPlayers: int = 2):
        if minPlayers < 2:
            minPlayers = 2
        if maxPlayers < minPlayers:
            maxPlayers = minPlayers
        self.id: int  = Room.globalID
        self.passwd: str  = passwd
        self.players: dict = {}
        self.movable: dict = {}
        self.statics: dict = {}
        # Ограничения на количество игроков в комнате
        self.maxPlayers: int = maxPlayers
        self.minPlayers: int = minPlayers
        # Подключённые в данный момент сессии
        self.wsBrows: list = []   
        self.wsPlayers: list = []
        # Итерация комнаты и глобальный ID
        self.iter: int  = 0
        Room.globalID += 1

    def getObjects(self):
        a = list(self.movable.values()) + \
            list(self.players.values()) + \
            list(self.statics.values())
        return a
    
    def createPlayer(self,
            name: str):
        if len(self.players) < self.maxPlayers:
            player = Player(name, position=[randint(-3, 3), randint(-3, 3)])
            player.room = self
            self.players[player.id] = player
            return player
        return None

    def createStatic(self, 
            position: list, 
            rotation: complex = complex(1, 0)):
        static = Static(position, rotation)
        static.room = self
        self.statics[static.id] = static

    def createMovable(self,
            position: list,
            rotation: complex = complex(1, 0)):
        movable = Movable(position, rotation)
        movable.room = self
        self.movable[movable.id] = movable

    async def sendToPlayers(self, data: dict):
        for pl in self.wsPlayers:
            if pl.closed:
                self.wsPlayers.remove(pl)
                print(f'Отключился игрок {pl}')
            else:
                await pl.send_json(data)
            
    async def sendToBrowsers(self, data: dict):
        for b in self.wsBrows:
            if b.closed:
                self.wsBrows.remove(b)
                print(f'Отключился клиент {b}')
            else:
                await b.send_json(data)

    async def update(self, 
            iteration: int):
        if iteration > self.iter:
            print(f'Одобрен запрос на обновление. Итерация {iteration}')
            self.iter = iteration
            for obj in list(self.movable.values()) + \
                       list(self.statics.values()):
                mvblData = mvbl.getData()
                await self.sendToBrowsers({
                    'e': 'getUpdate',
                    'id': mvblData['id'],
                    'type': mvblData['type'],
                    'pos': mvblData['pos'],
                    'rot': mvblData['rot']
                })
            await self.sendToPlayers({'e': 'updatePl'})
            return {'e': 'getUpdate', 'm': 'ok'}
        return {'e': 'getUpdate', 'm': 'error', 'iter': self.iter }


class RoomsContainer(object):
    def __init__(self, 
            maxRooms: int = 10):
        self.rooms = {}
        self.maxRooms = maxRooms

    def createRoom(self, 
            passwd: str,
            minPlayers: int = 2,
            maxPlayers: int = 2):
        if len(self.rooms) < self.maxRooms:
            room = Room(passwd, minPlayers, maxPlayers)
            self.rooms[room.id] = room
            return room
        return None

    def connectRoomView(self,
            roomID: int):
        if roomID in self.rooms:
            return self.rooms[roomID]
        return None

    def connectRoomPlayer(self,
            roomID: int,
            passwd: str):
        if roomID in self.rooms:
            if self.rooms[roomID].passwd == passwd:
                return self.room[roomID]
        return None

roomsContainer = RoomsContainer()


