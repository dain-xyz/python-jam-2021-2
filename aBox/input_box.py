from blessed import Terminal
from utils import Point, P, UP, DOWN, LEFT, RIGHT
from dataclasses import replace


class InputBox:
    def __init__(self, term, window_size: Point):
        self.term = term
        self.window_size = window_size

        self.lines = [""]
        self.cursor = P(0, 0)
        self.window_loc = P(0, 0)
    
    @property
    def width(self):
        return self.window_size.x
    
    @property
    def height(self):
        return self.window_size.y

    @property
    def wx(self):
        return self.window_loc.x
    
    @wx.setter
    def wx(self, value):
        value = max(value, 0)
        self.window_loc = replace(self.window_loc, x=value)

    @property
    def wy(self):
        return self.window_loc.y
    
    @wy.setter
    def wy(self, value):
        value = max(value, 0)
        self.window_loc = replace(self.window_loc, y=value)
    
    @property
    def cursor_in_window(self):
        in_x = self.wx <= self.x <= self.wx + self.width
        in_y = self.wy <= self.y <= self.wy + self.height
        return in_x and in_y
    
    @property
    def this_line(self):
        return self.lines[self.cursor.y]
    
    @this_line.setter
    def this_line(self, value):
        self.lines[self.cursor.y] = value
    
    @property
    def x(self):
        return self.cursor.x
    
    @x.setter
    def x(self, value):
        value = max(value, 0)
        diff = value - self.x
        direction = int(diff / abs(diff)) if diff else 0

        self.cursor = replace(self.cursor, x=value)
        if direction:
            while not self.cursor_in_window:
                self.wx += direction
            
    
    @property
    def y(self):
        return self.cursor.y
    
    @y.setter
    def y(self, value):
        value = max(value, 0)
        diff = value - self.y
        direction = int(diff / abs(diff)) if diff else 0

        self.cursor = replace(self.cursor, y=value)
        if direction:
            while not self.cursor_in_window:
                self.wy += direction
    
    @property
    def y_max(self):
        return len(self.lines) - 1
    
    def get_char(self, x, y):
        if y <= self.y_max:
            line = self.lines[y]
            if x < len(line):
                return line[x]
        
        return " "
    
    def get_char_in_window(self, x, y):
        return self.get_char(self.wx + x, self.wy + y)
    
    @property
    def char_under_cursor(self):
        return self.get_char(self.x, self.y)

    def handle_key(self, key):
        line_before = self.this_line[:self.x]
        line_after = self.this_line[self.x:]

        if not key.is_sequence:
            if key == "(":
                self.this_line = f"{line_before}(){line_after}"
            elif key == ")" and self.char_under_cursor == ")":
                pass
            else:
                self.this_line = f"{line_before}{key}{line_after}"
            
            self.x += 1
        
        # proceed assuming key.is_sequence
        elif key.name == "KEY_ENTER":
            self.lines.insert(self.y + 1, line_after)
            self.this_line = line_before
            self.x = 0
            self.y += 1
        
        elif key.name == "KEY_BACKSPACE":
            if self.x == 0:
                if self.y > 0:
                    upper, lower = self.y - 1, self.y
                    
                    self.x = len(self.lines[upper])
                    self.y = upper

                    self.lines[upper] += self.lines[lower]
                    self.lines.pop(lower)
            
            else:
                self.this_line = line_before[:self.x - 1] + line_after
                self.x -= 1
        
        elif key.name == "KEY_DELETE":
            if self.x < len(self.this_line):
                self.this_line = line_before + line_after[1:]
            
            elif self.y < self.y_max:
                self.this_line += self.lines[self.y + 1]
                self.lines.pop(self.y + 1)

            else:
                pass # cursor is at the end
        
        elif key.name == "KEY_LEFT":
            if self.x == 0:
                if self.y > 0:
                    self.y -= 1
                    self.x = len(self.this_line)
            
            else:
                self.x -= 1
        
        elif key.name == "KEY_RIGHT":
            if self.x == len(self.this_line):
                if self.y < self.y_max:
                    self.y += 1
                    self.x = 0
            
            else:
                self.x += 1
        
        elif key.name == "KEY_UP":
            if self.y > 0:
                self.y -= 1
                self.x = min(self.x, len(self.this_line))
            
            else:
                self.x = 0
        
        elif key.name == "KEY_DOWN":
            if self.y < self.y_max:
                self.y += 1
                self.x = min(self.x, len(self.this_line))
            
            else:
                self.x = len(self.this_line)
        
        elif key.name == "KEY_HOME":
            self.x = 0
        
        elif key.name == "KEY_END":
            self.y = len(self.this_line)
        
        elif key.name == "KEY_TAB":
            self.this_line = f"{line_before}    {line_after}"
            self.x += 4


    def render(self, location):
        for wy in range(self.height + 1):
            line = "".join(self.get_char_in_window(wx, wy) for wx in range(self.width + 1))
            term_loc = location.x, location.y + wy
            print(self.term.move_xy(*term_loc) + line)
        
        cursor_location = location + self.cursor - self.window_loc
        with self.term.location(*term_loc):
            print(self.term.move_xy(*cursor_location) + self.term.green_reverse(self.char_under_cursor))

    
    @property
    def as_string(self):
        return "\n".join(self.lines)




if __name__ == "__main__":
    term = Terminal()

    with term.fullscreen(), term.hidden_cursor(), term.cbreak():
        box = InputBox(term, P(40, 10))
        box_loc = Point(40, 0)

        while True:
            key = term.inkey()
            print(term.clear)
            with term.location(0, 0):
                box.handle_key(key)
                box.render(box_loc)
            
            print(f"{box.cursor=}")

