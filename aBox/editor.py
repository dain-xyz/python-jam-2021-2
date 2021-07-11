# code editor with semantic higlighting(hopefully)

import blessed
from time import sleep
from threading import Thread, Event

terminal = blessed.Terminal()

screen = [" "]

cursor = [0, 0]# line, pos I know its stupid

tick = 0

class PeriodicThread(Thread):

    def __init__(self, interval):
        self.stop_event = Event()
        self.interval = interval
        super(PeriodicThread, self).__init__()

    def run(self):
         while not self.stop_event.is_set():
             self.main()
             # wait self.interval seconds or until the stop_event is set
             self.stop_event.wait(self.interval)        

    def terminate(self):
        self.stop_event.set()

    def main(self):
        display()

def write_char(char, line, pos):
    global screen
    cursor[1] += 1
    if len(screen[line]) == pos: #end of line
        screen[line]+=char
    else:
        current = screen[line]
        screen[line] = current[:pos]+char+current[pos:]

def backspace(line, pos):
    global screen
    if pos != 0:
        cursor[1] -= 1
        screen[line] = screen[line][:pos-1] + screen[line][pos:]
    
    elif line != 0: 
        cursor[0] -= 1
        cursor[1] = len(screen[line-1])
        deleted = screen.pop(line)
        screen[line-1] += deleted
    
    else: 
        pass

def new_line(line):
    global cursor
    screen.insert(line+1, " ")
    cursor = [cursor[0]+1, 0]


def left(line, pos):
    global cursor, screen
    if pos == 0:
        if line == 0:
            pass
        else:
            cursor[0] -= 1
            cursor[1] = len(screen[line-1])
    else:
        cursor[1] -= 1

def right(line, pos):
    global cursor, screen
    if pos == len(screen[line]):
        if line == len(screen)-1:
            pass
        else:
            cursor[0] += 1
            cursor[1] = 0
    else:
        cursor[1] += 1

def up(line, pos):
    if line == 0:
        pass
    else:
        cursor[0] -= 1
        if pos>len(screen[line-1]):# longer than prev line
            cursor[1] = len(screen[line-1])
        
def down(line, pos):
    if line == len(screen)-1:
        pass
    else:
        cursor[0] += 1
        if pos>len(screen[line+1]):# longer than next line
            cursor[1] = len(screen[line+1])


def handle_keypress(key):
    if not key.is_sequence:# is a char
        write_char(key, cursor[0], cursor[1])
    
    elif key.code == 263:# backspace
        backspace(cursor[0], cursor[1])
    
    elif key.code == 343:# Enter (new line)
        print(screen)
        new_line(cursor[0])
    
    elif key.code == 260: #left arrow
        left(cursor[0], cursor[1])
    
    elif key.code == 261: #right arrow
        right(cursor[0], cursor[1])
    
    elif key.code == 258: #down arrow
        down(cursor[0], cursor[1])
    
    elif key.code == 259:#up arrow
        up(cursor[0], cursor[1])


def display():
    global screen, terminal, tick, cursor
    buffer = ""
    tick = tick % 2
    for i, line in enumerate(screen):
        if cursor[0] != i or tick == 1:
            buffer += line
            buffer += "\n"
        else:
            x = cursor[1]
            buffer += line[:x]+"█"+line[x+1:]
            buffer += "\n"
    buffer += "\n"*(terminal.height-len(screen)-2)
    print(buffer)

    tick += 1


def main():
    updater = PeriodicThread(interval=0.5)
    updater.start()
    terminal.fullscreen()
    try:
        with terminal.cbreak():
            value = ""

            while True:
                value = terminal.inkey(timeout=0) # Keep on waiting for keypresses
                if value:
                    handle_keypress(value)
                    display()
    except (KeyboardInterrupt, SystemExit, SystemError):
        updater.terminate()



if __name__ == "__main__":
    main()
