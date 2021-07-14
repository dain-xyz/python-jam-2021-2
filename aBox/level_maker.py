from dataclasses import dataclass
from typing import Tuple, Type
import json
from pathlib import Path
from itertools import product
from collections import defaultdict, namedtuple
from functools import cached_property

from rich import print
from PIL import Image

from tiles import Tile, Player, Air, Wall, Box, Enemy, Fire

Point = namedtuple("Point", ["x", "y"])

def point_add(a, b):
    # todo: this stuff really needs to be a dataclass with proper __add__ method
    # but for the moment we want to be able to just type (3, 4) for debugging
    # rather than always Point(3, 4)

    return Point(a[0] + b[0], a[1] + b[1])

def point_sub(a, b):
    # likewise
    return Point(a[0] - b[0], a[1] - b[1])

def point_inv(a):
    # likewise
    return Point(-a[0], -a[1])


UP = Point(0, -1)
DOWN = Point(0, 1)
LEFT = Point(-1, 0)
RIGHT = Point(1, 0)
DIRECTIONS = {UP, DOWN, LEFT, RIGHT}


@dataclass
class TileStack:
    contents: list[Type[Tile]]
    
    def push(self, x):
        self.contents.append(x)
    
    def pop(self):
        return self.contents.pop()
    
    @property
    def top(self):
        return self.contents[-1]
    



class LevelState:
    def __init__(self, tilemap: dict[Point, Type[Tile]]):
        self._tiles = {}

        for point, raw_tile in tilemap.items():
            if raw_tile is Air:
                self._tiles[point] = TileStack([Air])

            elif raw_tile is Player:
                self._player_pos = point
                self._tiles[point] = TileStack([Air, Player])

            else:
                self._tiles[point] = TileStack([Air, raw_tile])
        
        self._grab_pos = None


    @classmethod
    def from_image(self, img) -> "LevelState":
        image = Image.open(img)
        pixel_map = image.load()
        coords = product(range(image.width), range(image.height))

        # temporary, this will eventually be pulled from a config file or something
        colormap = {
            (255, 255, 255): Air,
            (0, 0, 0): Wall,
            (0, 162, 232): Player,
            (255, 127, 39): Box,
            (237, 28, 36): Enemy,
            (136, 0, 21): Fire,
        }

        tilemap = {
            Point(x, y): colormap[pixel_map[x, y]]
            for x, y in coords
        }

        players = [x for x in tilemap.values() if x is Player]
        if (n_players := len(players)) != 1:
            raise ValueError(f"must have exactly one player tile in the map, got: {n_players}")
        
        return LevelState(tilemap)
    

    @cached_property
    def size(self) -> Point:
        x, y = max(self._tiles.keys())
        return Point(x + 1, y + 1)

    
    def is_solid(self, point: Point) -> bool:
        return self._tiles[point].top.solid

    
    def _move_unsafe(self, old: Point, new: Point) -> None:
        thing = self._tiles[old].pop()
        self._tiles[new].push(thing)


    def can_move(self, old: Point, new: Point) -> bool:
        return not self.is_solid(new)


    def move_topmost(self, old: Point, new: Point) -> None:
        if not self.can_move(old, new):
            raise ValueError(f"cannot move from {old} to {new}: destination is solid: {self._tiles[new]}")
        
        self._move_unsafe(old, new)
    
    def str_to_point(self, direction: str) -> Point:

        direction = direction.lower()
        if direction == "up":
            return Point(0, -1)
        elif direction == "down":
            return Point(0, 1)
        elif direction == "left":
            return Point(-1, 0)
        elif direction == "right":
            return Point(1, 0)
    

    @property
    def player_pos(self) -> Point:
        return self._player_pos
    

    @player_pos.setter
    def player_pos(self, new: Point) -> None:
        self.move_topmost(self.player_pos, new)
        self._player_pos = new


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
        return point_sub(self.grab_pos, self.player_pos) if self.is_grabbing else None
    

    def grab(self, direction_str: str) -> None:
        
        direction = self.str_to_point(direction_str[0])

        target = point_add(self.player_pos, direction)
        if self._tiles[target].top is not Box:
            return
        
        self._grab_pos = target
    

    def ungrab(self) -> None:
        self._grab_pos = None
    

    def move_player(self, direction_str: str):

        direction = self.str_to_point(direction_str[0])

        box_pos = self.grab_pos
        player_destination = point_add(self.player_pos, direction)
    
        if not self.is_grabbing:
            if self.can_move(self.player_pos, player_destination):
                self.player_pos = player_destination
            return
        
        box_destination = point_add(box_pos, direction)

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