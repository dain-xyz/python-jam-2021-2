from dataclasses import dataclass
from typing import Tuple, Type, Iterator, Sequence
import json
from pathlib import Path
from itertools import product
from collections import defaultdict, namedtuple
from functools import cached_property
from enum import Enum, auto

from rich import print
from PIL import Image

from tiles import Tile, Player, Floor, Wall, Box, Enemy, Fire


@dataclass(frozen=True, order=True)
class Point:
    x: int
    y: int

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: "Point") -> "Point":
        return Point(self.x - other.x, self.y - other.y)
    
    def __neg__(self) -> "Point":
        return Point(-self.x, -self.y)

    def __iter__(self) -> Iterator[int]:
        return iter((self.x, self.y))


P = Point

class Action(Enum):
    move_up = auto()
    move_down = auto()
    move_left = auto()
    move_right = auto()
    grab_up = auto()
    grab_down = auto()
    grab_left = auto()
    grab_right = auto()
    ungrab = auto()
    wait = auto()


UP = P(0, -1)
DOWN = P(0, 1)
LEFT = P(-1, 0)
RIGHT = P(1, 0)
DIRECTIONS = {UP, DOWN, LEFT, RIGHT}


moves = {
    Action.move_up: UP,
    Action.move_down: DOWN,
    Action.move_left: LEFT,
    Action.move_right: RIGHT
}

moves_inverse = {
    UP: Action.move_up,
    DOWN: Action.move_down,
    LEFT: Action.move_left,
    RIGHT: Action.move_right
}


grabs = {
    Action.grab_up: UP,
    Action.grab_down: DOWN,
    Action.grab_left: LEFT,
    Action.grab_right: RIGHT
}

grabs_inverse = {
    UP: Action.grab_up,
    DOWN: Action.grab_down,
    LEFT: Action.grab_left,
    RIGHT: Action.grab_right
}



class TileStack:
    def __init__(self, level, position, contents=None):
        # a TileStack knows what level it belongs to
        self.level = level
        self.position = position
        self.contents = []

        if contents:
            for tile in contents:
                self.push(tile)

    
    def push(self, tile):
        # tiles must know what stack they belong to, and by extension
        # they can query their position, level, and so on.
        tile.stack = self
        self.contents.append(tile)
    

    def pop(self):
        tile = self.contents.pop()
        tile.stack = None
        return tile
    

    def remove(self, tile):
        self.contents.remove(tile)
        tile.stack = None
    

    @property
    def top(self):
        return self.contents[-1]
    

    def __iter__(self):
        return iter(self.contents)



class LevelState:
    def __init__(self, tilemap: dict[Point, Sequence[Tile]]):
        self.stacks = {}
        self.tiles = defaultdict(set)

        for position, tiles in tilemap.items():
            self.stacks[position] = TileStack(self, position)
            for tile in tiles:
                self.push_tile(position, tile)
        
        self.grab_target = None
    

    def push_tile(self, position, tile):
        self.stacks[position].push(tile)
        self.tiles[type(tile)].add(tile)
    

    def remove_tile(self, tile):
        tile.stack.remove(tile)
        self.tiles[type(tile)].remove(tile)
    

    @classmethod
    def from_image(self, img) -> "LevelState":
        image = Image.open(img)
        pixel_map = image.load()
        coords = product(range(image.width), range(image.height))

        # temporary, this will eventually be pulled from a config file or something
        colormap = {
            (255, 255, 255): Floor,
            (0, 0, 0): Wall,
            (0, 162, 232): Player,
            (255, 127, 39): Box,
            (237, 28, 36): Enemy,
            (136, 0, 21): Fire,
        }

        tilemap = {}
        n_players = 0
        for x, y in coords:
            position = Point(x, y)
            tile_type = colormap[pixel_map[x, y]]
            if tile_type is Floor:
                tilemap[position] = [Floor()]
            elif tile_type is Player:
                tilemap[position] = [Floor(), Player()]
                n_players += 1
            else:
                tilemap[position] = [Floor(), tile_type()]

        if n_players != 1:
            raise ValueError(f"must have exactly one player tile in the map, got: {n_players}")
        
        # print(tilemap)
        return LevelState(tilemap)
    

    @property
    def player(self):
        player_set = self.tiles[Player]
        if not player_set:
            raise RuntimeError("tried to access player but no player in the level")

        if len(player_set) > 1:
            raise RuntimeError("more than one player in level")
        
        return next(iter(player_set))

    @property
    def grab_pos(self):
        return self.grab_target.position if self.grab_target else None
    
    @property
    def is_grabbing(self):
        return bool(self.grab_target)

    @property
    def grab_direction(self):
        if self.is_grabbing:
            return self.grab_target.position - self.player.position
    

    @cached_property
    def size(self) -> Point:
        x, y = max(self.stacks.keys())
        return Point(x + 1, y + 1)

    
    def is_solid(self, point: Point) -> bool:
        return self.stacks[point].top.solid
    

    def move_unsafe(self, tile, destination):
        # WARNING: this does not check if the destination is solid!
        self.remove_tile(tile)
        self.push_tile(destination, tile)


    def update(self, action: Action) -> None:
        if not isinstance(action, Action):
            raise TypeError(f"{action} is not a valid Action")

        if action == Action.wait:
            return

        elif action == Action.ungrab:
            self.grab_target = None

        elif action in grabs:
            grab_direction = grabs[action]
            grab_target_pos = self.player.position + grab_direction
            grab_target_occupant = self.stacks[grab_target_pos].top

            if isinstance(grab_target_occupant, Box):
                self.grab_target = grab_target_occupant

        elif action in moves:
            move_direction = moves[action]
            player_target_pos = self.player.position + move_direction
            player_target_occupant = self.stacks[player_target_pos].top

            if not self.is_grabbing:
                if not player_target_occupant.solid:
                    self.move_unsafe(self.player, player_target_pos)
                return # may not be able to return when this gets more complicated
            
            box_target_pos = self.grab_pos + move_direction
            box_target_occupant = self.stacks[box_target_pos].top

            # pushing
            if move_direction == self.grab_direction:
                if not box_target_occupant.solid:
                    self.move_unsafe(self.grab_target, box_target_pos)
                    self.move_unsafe(self.player, player_target_pos)
            
            # pulling
            elif move_direction == -self.grab_direction:
                if not player_target_occupant.solid:
                    self.move_unsafe(self.player, player_target_pos)
                    self.move_unsafe(self.grab_target, box_target_pos)
            
            # sideways
            else:
                if not (player_target_occupant.solid or box_target_occupant.solid):
                    self.move_unsafe(self.player, player_target_pos)
                    self.move_unsafe(self.grab_target, box_target_pos)


            

            


        
    
    def ungrab(self):
        self.update(Action.ungrab)
    

    def move_player(self, direction):
        self.update(moves_inverse[direction])
    

    def grab(self, direction):
        self.update(grabs_inverse[direction])
    

    def __str__(self) -> str:
        # this is for debugging purposes, not necessarily for the actual program
        
        array = [
            [None for x in range(self.size.x)]
            for y in range(self.size.y)
        ]

        for (x, y), stack in self.stacks.items():
            array[y][x] = stack.top.symbol
        
        lines = ["".join(line) for line in array]
        return "\n".join(lines)
        




    
    # def _move_unsafe(self, old: Point, new: Point) -> None:
    #     thing = self._tiles[old].pop()
    #     self._tiles[new].push(thing)


    # def can_move(self, old: Point, new: Point) -> bool:
    #     return not self.is_solid(new)


    # def move_topmost(self, old: Point, new: Point) -> None:
    #     if not self.can_move(old, new):
    #         raise ValueError(f"cannot move from {old} to {new}: destination is solid: {self._tiles[new]}")
        
    #     self._move_unsafe(old, new)
    

    # @property
    # def player_pos(self) -> Point:
    #     return self._player_pos
    

    # @player_pos.setter
    # def player_pos(self, new: Point) -> None:
    #     self.move_topmost(self.player_pos, new)
    #     self._player_pos = new


    # @property
    # def grab_pos(self) -> Point:
    #     if self._grab_pos is None:
    #         return None
        
    #     tile = self._tiles[self._grab_pos]
    #     if tile.top is not Box:
    #         raise RuntimeError(f"thought tile {tile} at {self._grab_pos} had box at top, but it doesn't")
        
    #     return self._grab_pos
    

    # @property
    # def is_grabbing(self):
    #     return bool(self.grab_pos)
    

    # @property
    # def grab_direction(self):
    #     return self.grab_pos - self.player_pos if self.is_grabbing else None
    

    # def grab(self, direction: Point) -> None:
    #     target = self.player_pos + direction
    #     if self._tiles[target].top is not Box:
    #         return
        
    #     self._grab_pos = target
    

    # def ungrab(self) -> None:
    #     self._grab_pos = None
    

    # def move_player(self, direction):
    #     box_pos = self.grab_pos
    #     player_destination = self.player_pos + direction
    
    #     if not self.is_grabbing:
    #         if self.can_move(self.player_pos, player_destination):
    #             self.player_pos = player_destination
    #         return
        
    #     box_destination = box_pos + direction

    #     # pushing
    #     if player_destination == box_pos:
    #         if self.can_move(box_pos, box_destination):
    #             self.move_topmost(box_pos, box_destination)
    #             self.player_pos = player_destination
    #             self._grab_pos = box_destination
    #         return
        
    #     # pulling
    #     if box_destination == self.player_pos:
    #         if self.can_move(self.player_pos, player_destination):
    #             self.player_pos = player_destination
    #             self.move_topmost(box_pos, box_destination)
    #             self._grab_pos = box_destination
    #         return
        
    #     # sideways
    #     player_can_move = self.can_move(self.player_pos, player_destination)
    #     box_can_move = self.can_move(box_pos, box_destination)
        
    #     if player_can_move and box_can_move:
    #         self.player_pos = player_destination
    #         self.move_topmost(box_pos, box_destination)
    #         self._grab_pos = box_destination




