from level_maker import LevelState, UP, DOWN, LEFT, RIGHT, DIRECTIONS
# from screen import map_print
from pathlib import Path
import time

from blessed import Terminal


level_path = Path("levels/level1.png")

level = LevelState.from_image(level_path)

term = Terminal()


def level_print(level) -> None:
    with term.hidden_cursor():
        print(term.home + term.clear)

        for (x, y), tile in level._point_to_tile.items():
            foo = term.move_xy(x, y) + term.white(tile.symbol)
            print(foo)
        
        print(term.move_y(level.size.y))


moves = {
    "u": UP,
    "d": DOWN,
    "l": LEFT,
    "r": RIGHT
}
# actions = "grab", "ungrab", "move"

while True:
    level_print(level)
    command = input()

    if command == "q":
        break
    
    if command == "ungrab":
        level.ungrab()
    
    elif command == "unsafe ungrab":
        level.unsafe_ungrab()
    
    elif command.startswith("move"):
        _, direction = command.split()
        if direction not in moves:
            print("???"); continue
        
        level.move_player(moves[direction])
    
    elif command.startswith("unsafe move"):
        _1, _2, direction = command.split()
        if direction not in moves:
            print("???"); continue
        
        level.unsafe_move_player(moves[direction])
    
    else:
        print("???")
    




# level = make_dictionary_map(level_path)

# speed = 0.1
# moves = ['r', 'r', 'r', 'r', 'r', 'r', 'u', 'u', 'u', 'u', 'u', 'u', 'u']

# up = (0, -1)
# down = (0, 1)
# left = (-1, 0)
# right = (1, 0)

# def vector_add(a, b):
#     return a[0] + b[0], a[1] + b[1]

# #there are too much functions, need to be cleaned up, I have over complicated things
# def player_move(direction):
#     level['player'] = vector_add(level["player"], direction)

# def box_move(dir, index):
#     level['box'][index] = (level['box'][index][0] + dir[0], level['box'][index][1] + dir[1])

# def player_check(dir, ob):
#     return (level['player'][0] + dir[0], level['player'][1] + dir[1]) not in level[ob]

# def box_check(dir):
#     t = False
#     for i in level['box']: 
#         if (i[0] + dir[0], i[1] + dir[1]) in level['wall']:
#             t = True
#     return t

# def box_num(dir):
#     for i in range(len(level['box'])):
#         if (level['player'][0] + dir[0], level['player'][1] + dir[1]) == level['box'][i]:
#             return i
#     return -1

# def move(dir):
#     global b
#     if not(player_check(dir, 'box')) and not(box_check(dir)):
#         box_move(dir, box_num(dir))
#         player_move(dir)
#         b = box_num(dir)
#     elif player_check(dir, 'wall') and player_check(dir, 'box'):
#         player_move(dir)

# map_print(level)

# cm = 'a'
# #for cm in moves: #cm stands for curent move
# while cm != 'e': #I have put a while loop here for debuging
#     cm = input("Type u, d, l, r to move: ") #only for debuging
#     time.sleep(speed)
#     if cm == 'u':
#         dir = up
#         move(dir)
#     elif cm == 'd':
#         dir = down
#         move(dir)
#     elif cm == 'l':
#         dir = left
#         move(dir)
#     elif cm == 'r':
#         dir = right
#         move(dir)
#     map_print(level)
#     print("curent move:", cm, "  loc:", level['player'])