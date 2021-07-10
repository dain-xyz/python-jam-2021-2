from dataclasses import dataclass
from typing import Tuple

from PIL import Image

from perams import objects


def make_list_map(img: str) -> list:
    """Functions need docstring to pass the github tests"""
    levelimg = Image.open(img)
    # creates a list of list of dictionaries of the map image
    map = []
    for y in range(0, levelimg.height):
        map.insert(y, [])
        for x in range(0, levelimg.width):
            cordinate = (x, y)
            pixel = r, g, b = levelimg.getpixel(cordinate)
            for curent_object in objects:
                if(pixel[0] == curent_object['r']
                   and pixel[1] == curent_object['g']
                   and pixel[2] == curent_object['b']):
                    map[y].insert(0, {"ob": curent_object['ob']})

    return map


def make_string_map(img: str) -> str:
    """Functions need docstring to pass the github tests"""
    levelimg = Image.open(img)
    # Creates a string of the map image
    mapstring = ""
    for y in range(0, levelimg.height):
        for x in range(0, levelimg.width):
            cordinate = (x, y)
            pixel = r, g, b = levelimg.getpixel(cordinate)
            for i in range(len(objects)):
                if(pixel[0] == objects[i]['r'] and pixel[1] == objects[i]['g'] and pixel[2] == objects[i]['b']):
                    mapstring += objects[i]['char']
        mapstring += "\n"

    return mapstring


def make_tuple_map(img: str) -> tuple:
    """Functions need docstring to pass the github tests"""
    levelimg = Image.open(img)
    # Creates tuples of the coordinates of the objects
    Point = tuple[int, int]

    @dataclass
    class LevelState:
        img_dim: Tuple[int, int]
        player: Point
        wall: set[Point]
        box: set[Point]

    initial = LevelState(
        img_dim=(levelimg.size),
        player=(),
        wall=set(),
        box=set()
    )
    for y in range(0, levelimg.height):
        for x in range(0, levelimg.width):
            cordinate = (x, y)
            pixel = r, g, b = levelimg.getpixel(cordinate)
            for i in range(len(objects)):
                if(pixel[0] == objects[i]['r'] and pixel[1] == objects[i]['g'] and pixel[2] == objects[i]['b']):
                    if objects[i]['ob'] in ("air", "enemy"):
                        continue
                    if objects[i]['ob'] in ("player"):
                        initial.player = (x, y)
                        continue
                    exec(f"initial.{objects[i]['ob']}.add({cordinate})")  # noqa: S102
    return initial
