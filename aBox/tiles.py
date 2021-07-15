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
    
    @property
    def tile_below(self):
        if len(self.stack.contents) == 1:
            return None

        index = self.stack.contents.index(self)
        return self.stack.contents[index - 1]
    
    @property
    def tile_above(self):
        if self.stack.top == self:
            return None
        
        index = self.stack.contents.index(self)
        return self.stack.contents[index + 1]


class Player(Tile):
    symbol = "O"

    @property
    def is_dead(self):
        return self.stack.contents[-2].lethal


class Floor(Tile):
    symbol = " "


class Wall(Tile):
    symbol = "🮐"
    solid = True


class Box(Tile):
    symbol = "\u25a0"
    solid = True


class Enemy(Tile):
    symbol = "X"
    lethal = True


class Fire(Tile):
    symbol = "F"
    lethal = True