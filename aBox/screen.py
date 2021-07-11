from blessed import Terminal

from level_maker import make_dictionary_map
import json

#loads the objects list from json file
file = open('objects.json')
objects = json.load(file)
file.close

Point = tuple[int, int]
term = Terminal()

initial = {}
for i in objects:
    initial[i['ob']] = []


def map_print(map) -> None:
    """
    Gets the converted image passed along and
    prints it to the terminal using blessed
    """
    with term.hidden_cursor():
        print(term.home + term.clear)

        for y in range(map["img_dim"][1]):
            for x in range(map["img_dim"][0]):
                for current_object in objects:
                    if (x, y) in map[current_object['ob']]:
                        print(term.move_xy(x, y) + term.white(current_object['char']))
                        continue

        print(term.move_xy(map["player"][0], map["player"][1]) + term.white("O"))

    print(term.move_y(map["img_dim"][1]))
    return


def level_print(level) -> None:
    with term.hidden_cursor():
        print(term.home + term.clear)

        for (x, y), tile in level._point_to_tile.items():
            foo = term.move_xy(x, y) + term.white(tile.symbol)
            print(foo)
        
        print(term.move_y(level.size.y))


if __name__ == "__main__":
    map_print(make_dictionary_map("levels\\level" + input("type image number: ") + ".png"))
