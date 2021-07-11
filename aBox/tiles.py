class Tile:
    solid = False


class Player(Tile):
    symbol = "O"

class Air(Tile):
    symbol = " "

class Wall(Tile):
    symbol = "\u2588"
    solid = True

class Box(Tile):
    symbol = "\u25a0"
    solid = True

class Enemy(Tile):
    symbol = "X"
    solid = True

class Fire(Tile):
    symbol = "F"