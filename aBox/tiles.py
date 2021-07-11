class Tile:
    solid = False
    movable = False


class Player(Tile):
    symbol = "O"
    movable = True

class Air(Tile):
    symbol = " "

class Wall(Tile):
    symbol = "\u2588"
    solid = True

class Box(Tile):
    symbol = "\u25a0"
    solid = True
    movable = True

class Enemy(Tile):
    symbol = "X"
    solid = True

class Fire(Tile):
    symbol = "F"