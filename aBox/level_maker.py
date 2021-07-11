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
    # it would be nice to define this as __add__ on a dataclass but
    # for the moment we want to be able to just type (3, 4) for debugging
    # rather than always Point(3, 4)

    return Point(a[0] + b[0], a[1] + b[1])


UP = Point(0, -1)
DOWN = Point(0, 1)
LEFT = Point(-1, 0)
RIGHT = Point(1, 0)
DIRECTIONS = {UP, DOWN, LEFT, RIGHT}


class LevelState:
    def __init__(self, tilemap: dict[Point, Type[Tile]]):
        # mapping from x-y coordinates to tile type
        self._point_to_tile = tilemap

        # mapping from tile type to set of x-y coordinates
        index = defaultdict(set)
        for point, tile in self._point_to_tile.items():
            index[tile].add(point)

        self._tile_to_points = dict(index)
        
        # there should only ever be one player
        if len((player_tiles := self._tile_to_points[Player])) != 1:
            raise ValueError(f"must have exactly one player tile in the map, got: {player_tiles}")
        
        self._tile_to_points[Player] = player_tiles.pop()

        # we begin by grabbing nothing
        self._grabbing = None


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
        
        return LevelState(tilemap)


    @cached_property
    def size(self) -> Point:
        x, y = max(self._point_to_tile.keys())
        return Point(x + 1, y + 1)
    

    @property
    def player_pos(self) -> Point:
        return self._tile_to_points[Player]


    @property
    def grabbed_box_pos(self) -> Point:
        # defensive programming in case I screwed up somewhere
        
        if not self._grabbing:
            raise RuntimeError("tried to get grabbed box pos but not currently grabbing box")
        
        expected_box_pos = point_add(self.player_pos, self._grabbing)
        if expected_box_pos not in self._tile_to_points[Box]:
            raise RuntimeError(f"expected a box at {expected_box_pos} but no Box there")
        
        return expected_box_pos


    
    def is_solid(self, point: Point) -> bool:
        return self._point_to_tile[point].solid

    # the safe vs unsafe functions are for debugging; probably could merge them into one
    # and just log the errors
    
    def unsafe_grab(self, direction: Point) -> bool:
        target = point_add(self.player_pos, direction)
        if not target in self._tile_to_points[Box]:
            raise KeyError(f"{target} is not a Box")
        
        self._grabbing = direction
    

    def grab(self, direction: Point) -> bool:
        try:
            self.unsafe_grab(direction)
        except KeyError:
            pass
    

    def unsafe_ungrab(self) -> None:
        if self._grabbing is None:
            raise ValueError("cannot ungrab: not grabbing anything right now")

        # if we somehow lost track of the box then this will throw RuntimeError
        self.grabbed_box_pos

        self._grabbing = None
    

    def ungrab(self) -> None:
        try:
            self.unsafe_ungrab()
        except ValueError:
            pass
    

    def movement_is_possible(self, start: Point, direction: Point) -> bool:
        new_pos = point_add(start, direction)
        return new_pos in self._point_to_tile and not self._point_to_tile[new_pos].solid

    
    def unsafe_move_box(self, box_pos: Point, direction: Point) -> None:
        if box_pos not in self._tile_to_points[Box]:
            raise KeyError(f"{box_pos} is not a Box")
        
        if not self.movement_is_possible(box_pos, direction):
            raise ValueError(f"cannot move box from {box_pos} by {direction}")
        
        old_pos = box_pos
        new_pos = point_add(old_pos, direction)

        # this could probably be refactored eventually but it works for now

        self._point_to_tile[old_pos] = Air
        self._tile_to_points[Air].add(old_pos)
        self._tile_to_points[Box].remove(old_pos)

        self._point_to_tile[new_pos] = Box
        self._tile_to_points[Box].add(new_pos)
        self._tile_to_points[Air].remove(new_pos)
    

    def move_box(self, box_pos: Point, direction: Point) -> None:
        try:
            self.unsafe_move_box(box_pos, direction)
        except ValueError:
            pass


    def unsafe_move_player(self, direction: Point) -> None:
        # player is not moving a box
        if not self._grabbing:
            if not self.movement_is_possible(self.player_pos, direction):
                raise ValueError(f"cannot move player from {self.player_pos} by {direction}")
            
            old_pos = self.player_pos
            new_pos = point_add(old_pos, direction)

            self._point_to_tile[old_pos] = Air
            self._tile_to_points[Air].add(old_pos)

            self._point_to_tile[new_pos] = Player
            self._tile_to_points[Player] = new_pos
            self._tile_to_points[Air].remove(new_pos)

            return
        
        # player wants to push the box
        elif direction == self._grabbing:
            self.unsafe_move_box(self.grabbed_box_pos, direction)
            




    def move_player(self, direction: Point) -> None:
        try:
            self.unsafe_move_player(direction)
        except ValueError:
            pass



    def __str__(self) -> str:
        # this is for debugging purposes, not necessarily for the actual program
        
        array = [
            [None for x in range(self.size.x)]
            for y in range(self.size.y)
        ]

        for (x, y), tile in self._point_to_tile.items():
            array[y][x] = tile.symbol
        
        lines = ["".join(line) for line in array]
        return "\n".join(lines)


if __name__ == "__main__":
    level_number = input("type image number: ")
    filename = f"level{level_number}.png"
    img_source = Path("levels") / filename

    state = LevelState.from_image(img_source)
    print(state)
