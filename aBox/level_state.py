from dataclasses import dataclass
from typing import Tuple, Type, Iterator, Sequence
import json
from pathlib import Path
from itertools import product
from collections import defaultdict, namedtuple
from functools import cached_property
from enum import Enum, auto
import pprint

from rich import print
from PIL import Image

from tiles import Tile, Player, Floor, Wall, Box, Enemy, Fire, Win
from utils import Point, P, Action, UP, DOWN, LEFT, RIGHT


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
        self.contents = [] # this would probably be better as a linked list

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
    
    @property
    def won(self):
        return all(isinstance(box.tile_below, Win) for box in self.tiles[Box])
    

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
        print(direction)
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
    

    def serialize_to_code(self) -> str:
        # generates code to remake the level with the same tile positions
        # but loses state like grab target, so it is not strictly a repr
        tiles_as_strings = {
            pos: [f"{x.__class__.__name__}()" for x in stack.contents]
            for pos, stack in self.stacks.items()
        }
        return pprint.pformat(tiles_as_strings, indent=4).replace("'", "")
        