import aiohttp


class Player(object):
    def __init__(self, 
            name: str):
        self.name = name
        self.data = {}
        self.msg = {'do': 'skip'}

    def update(self):
        pass
    

    ############################
    def skip(self):
        self.msg['do'] = 'skip' 

    def move(self):
        self.msg['do'] = 'move'
    
    def turnLeft(self):
        self.msg['do'] = 'turnLeft'

    def turnRight(self):
        self.msg['do'] = 'turnRight'
    ############################


    ############################
    def getX(self):
        return self.data['pos']['x']

    def getY(self):
        return self.data['pos']['y']

    def getDistX(self, x):
        return abs(self.getX - x) - 1

    def getDistY(self, y):
        return abs(self.getY - y) - 1
    ############################


    ############################
    def look(self):
        if 'look' in self.data['update']:
            return self.data['update']['look']['type']
        else:
            return None
    
    def lookF(self):
        if 'lookF' in self.data['update']:
            return self.data['update']['lookF']['type']
        else:
            return None

    def lookL(self):
        if 'lookL' in self.data['update']:
            return self.data['update']['lookL']['type']
        else:
            return None

    def lookR(self):
        if 'lookR' in self.data['update']:
            return self.data['update']['lookR']['type']
        else:
            return None

    def distXLookF(self):
        if 'lookF' in self.data['update']:
            return abs(self.data['update']['lookF']['pos']['x'] - self.getX) - 1
        else:
            return None

    def distYLookF(self):
        if 'lookF' in self.data['update']:
            return abs(self.data['update']['lookF']['pos']['y'] - self.getY) - 1
        else:
            return None
    ############################




    ############################
    async def createRoom(self,
            ws, 
            passwd: str = '0000', 
            minPl=2, 
            maxPl=3, 
            data = {}):
        if 'm' in data:
            print(data['e'] + ' ' + data['m'])
        else:
            await ws.send_json({
                'e': 'create', 
                'passwd': passwd, 
                'minPl': minPl,
                'maxPl': maxPl
            })

    async def connectRoom(self,
            ws,
            roomID: int,
            passwd: str,
            data = {}):
        if 'm' in data:
            print(data['e'] + ' ' + data['m'])
        else:
            await ws.send_json({
                'e': 'connect',
                'roomID': roomID,
                'passwd': passwd
            })

    async def createPlayer(self, 
            ws,
            data = {}):
        if 'm' in data:
            print(data['e'] + ' ' + data['m'])
        else:
            await ws.send_json({
                'e': 'createPl',
                'name': self.name
            })

    async def updatePlayer(self, 
            ws, 
            data = {}):
        if 'm' in data:
            print(data['e'] + ' ' + data['m'])
        else:
            await ws.send_json({'e': 'getUpdate'})

    async def getUpdate(self, 
            ws, 
            data = {}):
        if 'm' in data:
            print(data['e'] + ' ' + data['m'])
        else:
            data.pop('e')
            self.data = data
            dispatch = {
                'skip': {'do': 'skip'},
                'move': {'do': 'move'},
                'turnLeft': {'do': 'turnLeft'},
                'turnRight': {'do': 'turnRight'}
            }
            self.update()
            a = {'e': 'updatePl'}
            a.update(dispatch[self.msg['do']])
            self.msg['do'] = 'skip'
            await ws.send_json(a)
