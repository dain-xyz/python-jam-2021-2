from level_state import LevelState, UP, DOWN, LEFT, RIGHT, DIRECTIONS
from pathlib import Path
import time

import blessed


level_path = Path("levels/level1.png")
level = LevelState.from_image(level_path)
    


def level_print(term, level) -> None:
    term.move_xy(0, 0)
    buffer = ""
    for (x, y), tile in level.stacks.items():
        symbol = tile.top.symbol
        buffer += term.move_xy(x, y)
        if symbol == "O":# Player
            buffer += term.black_on_yellow("O")
        elif symbol == "X":
            buffer += term.black_on_red("X")
        elif symbol == "\u25a0":
            buffer += term.blue_on_black("\u25a0")
        elif symbol == "\u2588":
            buffer += term.sienna4("▒")
        else:
            buffer += " "
        
    print(buffer)



moves = {
    "KEY_LEFT": LEFT,
    "KEY_RIGHT": RIGHT,
    "KEY_UP": UP,
    "KEY_DOWN": DOWN,
}

if __name__ == "__main__":
    term = blessed.Terminal()

    with term.hidden_cursor(), term.cbreak():
        mode = "move"

        while True:
            level_print(term, level)
            print(f"{level.size=}")
            print(f"{level.player_pos=}")
            print(f"{level.grab_pos=}")
            print(f"{level.is_grabbing=}")
            print(f"{level.grab_direction=}")
            print(f"[q]uit, [s]wap mode, [g]rab mode, [u]ngrab, arrowkeys to move")
            print(f"[debug only] = {mode=}")
            cmd = term.inkey()

            if cmd == "q":
                break
            elif cmd == "s": # switch between move and grab modes"
                mode = "grab" if mode == "move" else "move"
            elif cmd == "u":
                mode = "move"
                level.ungrab()
            elif cmd == "g":
                mode = "grab"
            elif cmd.is_sequence:
                if cmd.name in moves:
                    direction = moves[cmd.name]
                    if mode == "move":
                        level.move_player(direction)
                    else:
                        level.grab(direction)
                        mode = "move"