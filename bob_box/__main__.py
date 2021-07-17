# Entry point
from blessed import Terminal
from pathlib import Path
from input_box import InputBox
from game_movement import level_print
from level_state import LevelState
from interpreter import interpret, parse, InterpreterError
from utils import Action, Point, P
import time

term = Terminal()

level_num = 1
current_level = Path(f"levels/level{level_num}.png")

if __name__ == '__main__':
    with term.fullscreen(), term.hidden_cursor(), term.cbreak():
        level = LevelState.from_image(current_level)

        input_width = term.width - level.size.x - 4
        input_height = term.height - 4
        input_loc = P(level.size.x + 2, 0)
        input_box = InputBox(term, P(input_width, input_height))
        

        while True:
            # print(term.clear)
            level = LevelState.from_image(current_level) # reload level
            new_input_size = P(
                term.width - level.size.x - 4, term.height - 4
            )

            with term.location(0, 0):
                if input_box.window_size != new_input_size:
                    # user resized the terminal, we need to refresh everything
                    print(term.clear)
                    input_box.window_size = new_input_size

                level_print(term, level)
                input_box.render(input_loc)

            key = term.inkey()
            if key.is_sequence and key.name == "KEY_F5":
                print(term.clear_eol)

                try:
                    parsed = parse(input_box.as_string)
                    program = interpret(parsed)
                    
                    for action in program:
                        if isinstance(action, Action):
                            level.update(action)
                            level_print(term, level)
                            time.sleep(0.5)

                    level_print(term, level)

                except InterpreterError as e:
                    print(e)
                
                if level.won:
                    level_num += 1
                    current_level = Path(f"levels/level{level_num}.png")
            
            else:
                input_box.handle_key(key)

                

            

