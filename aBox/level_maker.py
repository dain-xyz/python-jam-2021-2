from PIL import Image #import skimage
import typing
from dataclasses import dataclass
from rich import print
from perams import objects
from typing import Tuple

def make_list_map(img):
    levelimg = Image.open(img)
    #creates a list of list of dictionaries of the map image
    map = []
    for y in range(0, levelimg.height):
        map.insert(y, [])
        for x in range(0, levelimg.width):
            cordinate = (x, y)
            pixel = r, g, b = levelimg.getpixel(cordinate)
            for curent_object in objects:
                if(pixel[0] == curent_object['r'] and pixel[1] == curent_object['g'] and pixel[2] == curent_object['b']):
                    map[y].insert(0, {"ob":curent_object['ob']})

    return map

def make_string_map(img):
    levelimg = Image.open(img)
    #creates a string of the map image
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

def make_tuple_map(img):
    levelimg = Image.open(img) 
    #crates tupels of the cordinets of the objects
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
                    if objects[i]['ob'] in ( "air","enemy"):
                        continue
                    if objects[i]['ob'] in ( "player"):
                        initial.player = (x, y)
                        continue
                    exec(f"initial.{objects[i]['ob']}.add({cordinate})")
    return initial

def make_dictionary_map(img) -> dict:
    levelimg = Image.open(img) 
    #crates tupels of the cordinets of the objects
    initial = {'img_dim':levelimg.size}
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
                    if objects[i]['ob'] in ( "air","enemy"):
                        continue
                    if objects[i]['ob'] in ( "player"):
                        initial['player'] = (x, y)
                        continue
                    initial[objects[i]['ob']].append(cordinate)
    return initial
