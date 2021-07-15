import blessed
from level_state import Point, UP, DOWN, LEFT, RIGHT, LevelState
import tiles
import json

with open("objects.json", "r") as file:
    data = json.load(file)

resolution = [int(input("Resolution X: ")), int(input("Resolution Y: "))]
# print(resolution[1]+2)

tilemap = {}
for y in range(resolution[1]):
    for x in range(resolution[0]):
        tilemap[Point(x,y)] = [tiles.Floor()]
level = LevelState(tilemap)

# def get_char(object:str):
#     """
#     Gets the char from json file.
#     """
#     for i in data:
#         if i["ob"] == object:
#             return i["char"]


def level_with_border(level: LevelState) -> str:
    width, height = level.size
    lines = str(level).split("\n")
    new_lines = []
    horizontal_border = "="*(width + 2)
    new_lines.append(horizontal_border)
    new_lines.extend(f"|{line}|" for line in lines)
    new_lines.append(horizontal_border)
    return "\n".join(new_lines)


def print_level(term, level: LevelState) -> str:
    print(term.home, term.clear)
    print(level_with_border(level))
    print(term.move_y(level.size.y + 2))


move_keys = {
    "KEY_LEFT": LEFT,
    "KEY_RIGHT": RIGHT,
    "KEY_UP": UP,
    "KEY_DOWN": DOWN,
}

tile_keys = {
    "w": tiles.Wall,
    "p": tiles.Player,
    "b": tiles.Box,
    "f": tiles.Fire
}

if __name__ == "__main__":
    term = blessed.Terminal()
    level_pos = Point(0, 0)

    with term.hidden_cursor(), term.cbreak():
        while True:
            print_level(term, level)
            cursor_pos = level_pos + Point(1, 2)
            
            with term.location(*cursor_pos):
                char_under_cursor = level.stacks[level_pos].top.symbol
                print(term.green_reverse(char_under_cursor))

            current_stack = level.stacks[level_pos]
            current_contents = current_stack.contents
            contents_strs = [x.__class__.__name__ for x in current_contents]
            print(f"current contents: {contents_strs}")
            print(f"insert tile: [w]all, [p]layer, [b]ox, [f]ire") # need to keep this in sync with tile_keys
            print(f"[q]uit, [del]ete topmost tile")
            print("note: this will not stop you doing 'illegal' configurations like putting box inside a wall")
            print("[q]uit")

            cmd = term.inkey()

            if cmd == "q":
                break
            
            elif cmd in tile_keys:
                new_tile = tile_keys[cmd]()
                level.push_tile(level_pos, new_tile)
            
            elif cmd.is_sequence:
                if cmd.name in move_keys:
                    direction = move_keys[cmd.name]
                    new_pos = level_pos + direction
                    if new_pos in level.stacks:
                        level_pos = new_pos
                
                elif cmd.name == "KEY_DELETE" and len(current_contents) > 1:
                    level.remove_tile(current_stack.top)
