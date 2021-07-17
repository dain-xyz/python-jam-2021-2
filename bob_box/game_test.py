from level_state import LevelState
from utils import UP, DOWN, LEFT, RIGHT
from pathlib import Path
import time

import blessed


def level_print(term, level) -> None:
    print(term.home + term.clear)

    for (x, y), tile in level.stacks.items():
        symbol = term.move_xy(x, y) + term.white(tile.top.symbol)
        print(symbol)
    
    print(term.move_y(level.size.y))


moves = {
    "KEY_LEFT": LEFT,
    "KEY_RIGHT": RIGHT,
    "KEY_UP": UP,
    "KEY_DOWN": DOWN,
}

def test_level(level):
    term = blessed.Terminal()

    with term.hidden_cursor(), term.cbreak():
        mode = "move"

        while True:
            level_print(term, level)
            print(f"{level.size=}")
            print(f"{level.player.position=}")
            print(f"{level.player.is_dead=}")
            print(f"{level.grab_pos=}")
            print(f"{level.is_grabbing=}")
            print(f"{level.grab_direction=}")
            print(f"{level.won=}")
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


if __name__ == "__main__":
    level_path = Path("level_images/level1.png")
    level = LevelState.from_image(level_path)
    test_level(level)