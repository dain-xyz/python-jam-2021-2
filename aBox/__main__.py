# Entry point
from blessed import Terminal
from pathlib import Path
from input_box import create_box
from game_movement import level_print
from level_maker import LevelState, UP, DOWN, LEFT, RIGHT, DIRECTIONS

term = Terminal()

current_level = Path("levels/level1.png")
level = LevelState.from_image(current_level)

functions = {
    "move": level.move_player,
    "==": lambda args: args[0]==args[1],
    "+": lambda args: args[0]+args[1],
    "grab": level.grab,
    "ungrab": level.ungrab,
}


display_list = [""]
cx = 0
cy = 0


if __name__ == '__main__':
    with term.fullscreen(), term.hidden_cursor(), term.cbreak():
        while True:
            
            key = term.inkey()

            print(term.home + term.clear)
            level_print(term, level)
            display_list, cx, cy = create_box(level.size[0]+10, term, key, display_list, cx, cy, functions)
            

