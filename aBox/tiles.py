# class Tile:
#     solid = False
#     movable = False


# class Player(Tile):
#     symbol = "O"
#     movable = True

# class Air(Tile):
#     symbol = " "

# class Wall(Tile):
#     symbol = "\u2588"
#     solid = True

# class Box(Tile):
#     symbol = "\u25a0"
#     solid = True
#     movable = True

# class Enemy(Tile):
#     symbol = "X"
#     solid = True

# class Fire(Tile):
#     symbol = "F"

class Tile:
    solid = False
    lethal = False

    def __init__(self, stack=None):
        self.stack = stack
        self.move_target = None # make this a tuple of old/new?

    @property
    def position(self):
        return self.stack.position
    
    @property
    def level(self):
        return self.stack.level


class Player(Tile):
    pass


class Floor(Tile):
    pass


class Wall(Tile):
    solid = True


class Box(Tile):
    solid = True


class Enemy(Tile):
    lethal = True


class Fire(Tile):
    lethal = True