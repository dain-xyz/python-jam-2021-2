from level_maker import make_dictionary_map
from screen import map_print
import time

map = make_dictionary_map('levels\\level1.png')

speed = 0.1
moves = ['r', 'r', 'r', 'r', 'r', 'r', 'u', 'u', 'u', 'u', 'u', 'u', 'u']

up = (0, -1)
down = (0, 1)
left = (-1, 0)
right = (1, 0)

#there are too much functions, need to be cleaned up, I have over complicated things
def player_move(dir):
    map['player'] = (map['player'][0] + dir[0], map['player'][1] + dir[1])

def box_move(dir, index):
    map['box'][index] = (map['box'][index][0] + dir[0], map['box'][index][1] + dir[1])

def player_check(dir, ob):
    return (map['player'][0] + dir[0], map['player'][1] + dir[1]) not in map[ob]

def box_check(dir):
    t = False
    for i in map['box']: 
        if (i[0] + dir[0], i[1] + dir[1]) in map['wall']:
            t = True
    return t

def box_num(dir):
    for i in range(len(map['box'])):
        if (map['player'][0] + dir[0], map['player'][1] + dir[1]) == map['box'][i]:
            return i
    return -1

def move(dir):
    global b
    if not(player_check(dir, 'box')) and not(box_check(dir)):
        box_move(dir, box_num(dir))
        player_move(dir)
        b = box_num(dir)
    elif player_check(dir, 'wall') and player_check(dir, 'box'):
        player_move(dir)

map_print(map)

cm = 'a'
#for cm in moves: #cm stands for curent move
while cm != 'e': #I have put a while loop here for debuging
    cm = input("Type u, d, l, r to move: ") #only for debuging
    time.sleep(speed)
    if cm == 'u':
        dir = up
        move(dir)
    elif cm == 'd':
        dir = down
        move(dir)
    elif cm == 'l':
        dir = left
        move(dir)
    elif cm == 'r':
        dir = right
        move(dir)
    map_print(map)
    print("curent move:", cm, "  loc:", map['player'])