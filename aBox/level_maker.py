from dataclasses import dataclass
from typing import Tuple

from PIL import Image

from perams import objects
from rich import print

Point = tuple[int, int]
@dataclass
class LevelState:
    img_dim: Tuple[int, int]
    player: Point
    wall: set[Point]
    box: set[Point]


def make_list_map(img) -> list:
    """
    Converts map image to lists.
    """
    levelimg = Image.open(img)
    map = []
    for y in range(0, levelimg.height):
        map.insert(y, [])
        for x in range(0, levelimg.width):
            cordinate = (x, y)
            pixel = r, g, b = levelimg.getpixel(cordinate)
            for curr_object in objects:
                if(pixel[0] == curr_object['r'] and pixel[1] == curr_object['g'] and pixel[2] == curr_object['b']):
                    map[y].insert(0, {"ob": curr_object['ob']})

    return map


def make_string_map(img) -> str:
    """
    Converts the map image into a string.
    """
    levelimg = Image.open(img)
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


def make_tuple_map(img) -> LevelState:
    """
    Converts the map image into tuples of the coordinates of the objects.
    """
    levelimg = Image.open(img)

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
                    exec(f"initial.{objects[i]['ob']}.add({cordinate})")
    return initial


def make_dictionary_map(img) -> dict:
    """
    Converts the map image to a dictionary of all the object positions.
    """
    levelimg = Image.open(img)
    initial = {'img_dim': levelimg.size}
    for i in objects:
        initial[i['ob']] = []

    for y in range(0, levelimg.height):
        for x in range(0, levelimg.width):
            cordinate = (x, y)
            r = levelimg.getpixel(cordinate)[0]
            g = levelimg.getpixel(cordinate)[1]
            b = levelimg.getpixel(cordinate)[2]
            for i in range(len(objects)):
                if(r == objects[i]['r'] and g == objects[i]['g'] and b == objects[i]['b']):
                    if objects[i]['ob'] in ("air", "enemy"):
                        continue
                    if objects[i]['ob'] in ("player"):
                        initial['player'] = (x, y)
                        continue
                    initial[objects[i]['ob']].append(cordinate)
    return initial


if __name__ == "__main__":
    img_source = input("type image number: ")
    print("list:\n" + str(make_list_map("levels\\level" + img_source + ".png")))
    print("string:\n" + str(str(make_string_map("levels\\level" + img_source + ".png"))))
    print("tuple:\n" + str(make_tuple_map("levels\\level" + img_source + ".png")))
    print("dictionary:\n" + str(make_dictionary_map("levels\\level" + img_source + ".png")))
