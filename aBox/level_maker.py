from dataclasses import dataclass
from typing import Tuple, Type, Iterator
import json
from pathlib import Path
from itertools import product
from collections import defaultdict, namedtuple
from functools import cached_property

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


UP = P(0, -1)
DOWN = P(0, 1)
LEFT = P(-1, 0)
RIGHT = P(1, 0)
DIRECTIONS = {UP, DOWN, LEFT, RIGHT}


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

        for position, tile in tilemap.items():
            self.stacks[position] = TileStack(self, position)
            self.push_tile(position, tile)
    

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
        for x, y in coords:
            position = Point(x, y)
            tile_type = colormap[pixel_map[x, y]]
            if tile_type is Floor:
                tilemap[position] = [Floor()]
            else:
                tilemap[position] = [Floor(), tile_type()]

        players = [x for x in tilemap.values() if isinstance(x, Player)]
        if (n_players := len(players)) != 1:
            raise ValueError(f"must have exactly one player tile in the map, got: {n_players}")
        
        return LevelState(tilemap)
    

    def player(self):
        player_set = self.tiles[Player]
        if not player_set:
            raise RuntimeError("tried to access player but no player in the level")

        if len(player_set) > 1:
            raise RuntimeError("more than one player in level")
        
        return next(iter(player_set))
    

    @cached_property
    def size(self) -> Point:
        x, y = max(self.stacks.keys())
        return Point(x + 1, y + 1)

    
    def is_solid(self, point: Point) -> bool:
        return self.stacks[point].top.solid

    
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


    @property
    def grab_pos(self) -> Point:
        if self._grab_pos is None:
            return None
        
        tile = self._tiles[self._grab_pos]
        if tile.top is not Box:
            raise RuntimeError(f"thought tile {tile} at {self._grab_pos} had box at top, but it doesn't")
        
        return self._grab_pos
    

    @property
    def is_grabbing(self):
        return bool(self.grab_pos)
    

    @property
    def grab_direction(self):
        return self.grab_pos - self.player_pos if self.is_grabbing else None
    

    def grab(self, direction: Point) -> None:
        target = self.player_pos + direction
        if self._tiles[target].top is not Box:
            return
        
        self._grab_pos = target
    

    def ungrab(self) -> None:
        self._grab_pos = None
    

    def move_player(self, direction):
        box_pos = self.grab_pos
        player_destination = self.player_pos + direction
    
        if not self.is_grabbing:
            if self.can_move(self.player_pos, player_destination):
                self.player_pos = player_destination
            return
        
        box_destination = box_pos + direction

        # pushing
        if player_destination == box_pos:
            if self.can_move(box_pos, box_destination):
                self.move_topmost(box_pos, box_destination)
                self.player_pos = player_destination
                self._grab_pos = box_destination
            return
        
        # pulling
        if box_destination == self.player_pos:
            if self.can_move(self.player_pos, player_destination):
                self.player_pos = player_destination
                self.move_topmost(box_pos, box_destination)
                self._grab_pos = box_destination
            return
        
        # sideways
        player_can_move = self.can_move(self.player_pos, player_destination)
        box_can_move = self.can_move(box_pos, box_destination)
        
        if player_can_move and box_can_move:
            self.player_pos = player_destination
            self.move_topmost(box_pos, box_destination)
            self._grab_pos = box_destination


    def __str__(self) -> str:
        # this is for debugging purposes, not necessarily for the actual program
        
        array = [
            [None for x in range(self.size.x)]
            for y in range(self.size.y)
        ]

        for (x, y), tile in self._tiles.items():
            array[y][x] = tile.top.symbol
        
        lines = ["".join(line) for line in array]
        return "\n".join(lines)

