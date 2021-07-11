from level_maker import LevelState, UP, DOWN, LEFT, RIGHT, DIRECTIONS
from pathlib import Path
import time

from blessed import Terminal


level_path = Path("levels/level1.png")

level = LevelState.from_image(level_path)

term = Terminal()


def level_print(level) -> None:
    with term.hidden_cursor():
        print(term.home + term.clear)

        for (x, y), tile in level._tiles.items():
            foo = term.move_xy(x, y) + term.white(tile.top.symbol)
            print(foo)
        
        print(term.move_y(level.size.y))


moves = {
    "u": UP,
    "d": DOWN,
    "l": LEFT,
    "r": RIGHT
}
# actions = "grab", "ungrab", "move"

def playground():
    while True:
        level_print(level)
        command = input()

        if command == "q":
            break
        
        if command == "ungrab":
            level.ungrab()
        
        elif command.startswith("move"):
            _, direction = command.split()
            if direction not in moves:
                continue
            
            level.move_player(moves[direction])
        
        elif command.startswith("grab"):
            _, direction = command.split()
            if direction not in moves:
                continue
            
            level.grab(moves[direction])
        
        else:
            pass
    