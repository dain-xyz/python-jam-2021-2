# Entry point
from blessed import Terminal
from pathlib import Path
from input_box import create_box
from game_movement import level_print
from level_state import LevelState, UP, DOWN, LEFT, RIGHT, DIRECTIONS
# from custom_parser import eval, parse
from interpreter import interpret, parse
from utils import Action
import time

term = Terminal()

current_level = Path("levels/level1.png")

level_num = 1


# level = LevelState.from_image(current_level)

# functions = {
#     "move": level.move_player,
#     "==": lambda args: args[0]==args[1],
#     "+": lambda args: args[0]+args[1],
#     "grab": level.grab,
#     "ungrab": level.ungrab,
# }


display_list = [""]
cx = 0
cy = 0

mode = prev_mode = 0 # 0 is edit, 1 is run

if __name__ == '__main__':
    with term.fullscreen(), term.hidden_cursor(), term.cbreak():
        while True:
            level = LevelState.from_image(current_level)
            level_print(term, level)

            key = term.inkey()
            #print(term.home + term.clear)
            #level_print(term, level)

            display_list, cx, cy, mode = create_box(level.size.x + 10, term, key, display_list, cx, cy)

            if prev_mode != mode and mode == 1: # mode changed to run mode
                parsed = parse("".join(display_list))
                program = interpret(parsed)
                
                for action in program:
                    if isinstance(action, Action):
                        level.update(action)
                        level_print(term, level)
                        time.sleep(0.5)

                mode = 0

                if level.won:# level won
                    level_num += 1
                    current_level = Path(f"levels\level{level_num}.png")
                level_print(term, level)
            
            prev_mode = mode
                

            
