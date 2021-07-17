# Entry point
from blessed import Terminal
from pathlib import Path
from input_box import InputBox
from game_movement import level_print
from level_state import LevelState
from interpreter import interpret, parse, InterpreterError, program_size
from utils import Action, Point, P
from level_data import(
    level_1,
    level_2,
    level_3,
    level_4,
    level_5,
    level_6,
    level_7,
    level_8,
    level_9,
    level_10
)
import time


levels = {
    1: level_1,
    2: level_2,
    3: level_3,
    4: level_4,
    5: level_5,
    6: level_6,
    7: level_7,
    8: level_8,
    9: level_9,
    10: level_10
}

level_min_width = 20


def write_stat(term, pos, message):
    with term.location(0, 0):
        print(term.move_xy(*pos) + message.ljust(level_min_width))

def write_error(term, pos, message):
    with term.location(0, 0):
        print(term.move_xy(*pos) + message + term.clear_eol)


def run_level(term, current_level):
    level = LevelState(current_level)
    
    input_loc = P(max(level.size.x + 2, level_min_width), 0) 
    input_width = term.width - input_loc.x - 4
    input_height = term.height - 4

    input_box = InputBox(term, P(input_width, input_height))

    attempts = 0
    deaths = 0
    prog_size = 0
    moves = 0

    attempts_pos = P(0, level.size.y + 1) 
    deaths_pos = P(0, level.size.y + 2) 
    size_pos = P(0, level.size.y + 3) 
    moves_pos = P(0, level.size.y + 4)
    error_pos = P(0, term.height - 3)

    write_stat(term, attempts_pos, f"Attempts: {attempts}")
    write_stat(term, deaths_pos, f"Deaths: {deaths}")
    write_stat(term, size_pos, f"Program size: {prog_size}")
    write_stat(term, moves_pos, f"Moves: {moves}")
    
    while True:
        level = LevelState(current_level) # reload level
        new_input_size = P(
            term.width - input_loc.x - 4, term.height - 4
        )

        moves = 0

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
            attempts += 1
            write_stat(term, attempts_pos, f"Attempts: {attempts}")

            try:
                parsed = parse(input_box.as_string)
                program = interpret(parsed)
                
                for action in program:
                    if isinstance(action, Action):
                        level.update(action)
                        level_print(term, level)
                        moves += 1

                        write_stat(term, moves_pos, f"Moves: {moves}")

                        time.sleep(0.5)
                    
                    if level.player.is_dead:
                        deaths += 1
                        write_stat(term, deaths_pos, f"Deaths: {deaths}")
                        break
                    
                time.sleep(2)
                level_print(term, level)

            except InterpreterError as e:
                write_error(term, error_pos, str(e))
            
            if level.won:
                return {
                    "won": True,
                    "attempts": attempts,
                    "deaths": deaths,
                    "program_size": prog_size,
                    "moves": moves
                }
        
        else:
            input_box.handle_key(key)
            try:
                prog_size = program_size(input_box.as_string)
            except InterpreterError:
                prog_size = "N/A"
            
            message = f"Program size: {prog_size}"
            message = term.red(message) if prog_size == "N/A" else message

            write_stat(term, size_pos, message)


if __name__ == '__main__':
    term = Terminal()
    level_num = 1

    with term.fullscreen(), term.hidden_cursor(), term.cbreak():
        while True:
            print(term.clear)
            current_level = levels[level_num]
            results = run_level(term, current_level)
            level_num += 1
            # break
    
    # print(results)


        