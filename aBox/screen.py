from blessed import Terminal

from level_maker import make_tuple_map

Point = tuple[int, int]
term = Terminal()


def map_print(map: str) -> None:
    """
    Gets the converted image from level_maker.py and
    prints it to the terminal using blessed.
    """
    Map = [[" " for i in range(map.img_dim[1])] for i in range(map.img_dim[0])]
    for i in map.wall:
        Map[i[0]][i[1]] = "█"
    for i in map.box:
        Map[i[0]][i[1]] = "■"
    Map[map.player[0]][map.player[1]] = "O"

    with term.hidden_cursor():
        print(term.home + term.clear)

        for y in range(map.img_dim[1]):
            for x in range(map.img_dim[0]):
                if (x, y) in map.wall:
                    print(term.move_xy(x, y) + term.white("█"))

                if (x, y) in map.box:
                    print(term.move_xy(x, y) + term.white("■"))

        print(term.move_xy(map.player[0], map.player[1]) + term.white("O"))

    print(term.move_y(map.img_dim[1]))
    return


if __name__ == "__main__":
    map_print(make_tuple_map("level2.png"))
