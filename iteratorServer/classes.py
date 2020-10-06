from room import *
import json


class Object(object):
    globalID: int = 0

    def __init__(self, 
            position: list = [0, 0], 
            rotation: complex = complex(1, 0)):
        self.id: int = Object.globalID;
        self.room: 'room.Room'
        self.position: list = position
        self.rotation: list = rotation
        #
        Object.globalID += 1
        #
        self.data: dict = {
            "id": self.id,
            "type": "object",
            "pos": {
                "x": self.position[0],
                "y": self.position[1]
            },
            "rot": {
                "x": int(self.rotation.real),
                "y": int(self.rotation.imag)
            }
        }

    def setPosition(self, 
            x: int,
            y: int):
        self.position[0] = x
        self.position[1] = y
        self.data["pos"]["x"] = self.position[0]
        self.data["pos"]["y"] = self.position[1]
        return self

    def setRotation(self, 
            x: int,
            y: int):
        self.rotation = complex(x, y)
        self.data["rot"]["x"] = int(self.rotation.real)
        self.data["rot"]["y"] = int(self.rotation.imag)
        return self

    def getData(self):
        a = {}
        a.update(self.data)
        return a


class Static(Object):
    def __init__(self,
            position: list = [0, 0],
            rotation: complex = complex(1, 0)):
        super().__init__(position, rotation)
        self.data["type"] = "static"


class Movable(Object):
    def __init__(self,
            position: list = [0, 0],
            rotation: complex = complex(1, 0)):
        super().__init__(position, rotation)   
        self.data["type"] = "movable"
        # Заголовок для временных данных
        self.data.update({"update": {}}) 

    def lookAtXY(self):
        """ Возвращает координату, на которую в данных момент смотрит объект """
        look = [self.position[0] + int(self.rotation.real),
                self.position[1] + int(self.rotation.imag)]
        return look


    def look(self):
        """ Возвращает объект, который стоит непосредственно перед объектом,
            если такой есть 
        """
        for obj in self.room.getObjects():
            if obj.position == self.lookAtXY():
                self.data["update"].update({"look": {}})
                self.data["update"]["look"].update({
                    "type": obj.data["type"], 
                    "pos": obj.data["pos"]
                })
                return obj
        return None

    def lookForward(self):
        """ Возвращает объект, на который смотрит объект, если такой есть """
        front = []
        for i in range(1, 20):
            front = [self.position[0] + int(self.rotation.real)*i,
                     self.position[1] + int(self.rotation.imag)*i]
            for obj in self.room.getObjects():
                if front == obj.position:
                    self.data["update"].update({"lookF": {}})
                    self.data["update"]["lookF"].update({
                        "type": obj.data["type"], 
                        "pos": obj.data["pos"]
                    })
                    return obj
        return None

    def move(self):
        if not self.look():
            lookAtXY = self.lookAtXY()
            self.setPosition(lookAtXY[0], lookAtXY[1])
        return self

    def turnLeft(self):
        self.rotation *= complex(0, 1)
        self.data["rot"]["x"] = int(self.rotation.real)
        self.data["rot"]["y"] = int(self.rotation.imag)
        return self

    def turnRight(self):
        self.rotation *= complex(0, -1)
        self.data["rot"]["x"] = int(self.rotation.real)
        self.data["rot"]["y"] = int(self.rotation.imag)
        return self
    
    def lookLeft(self):
        """ Возвращает объект слева от объекта, если такой есть """
        obj = self.turnLeft().look()
        self.turnRight()
        if obj:
            self.data.update({"lookL": {}})
            self.data["update"]["lookL"].update({ "type": obj.data["type"], "pos": obj.data["pos"]
            })
        return obj

    def lookRight(self):
        """ Возвращает объект справа от объекта, если такой есть """
        obj = self.turnRight().look()
        self.turnLeft()
        if obj:
            self.data.update({"lookR": {}})
            self.data["update"]["lookR"].update({
                "type": obj.data["type"], 
                "pos": obj.data["pos"]
            })
        return obj

    def getData(self):
        """ Возвращет словарь данных объекта, очищает поле временных данных """
        a = {}
        a.update(self.data)
        self.data["update"] = {}
        return a


class Player(Movable):
    def __init__(self, 
            name: str,
            health: int = 100,
            position: list = [0, 0],
            rotation: complex = complex(1, 0)):
        super().__init__(position, rotation)
        self.data["type"] = "player"
        self.name = name
        self.health = health
        self.data.update({"name": self.name, "health": self.health})


