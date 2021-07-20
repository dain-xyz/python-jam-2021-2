
# BobBox: A game about moving boxes using code

## Installation instructions

Clone the repository, cd into it, optionally create and activate a virtual environment, then issue:

```
pip install -r requirements.txt
```

Still in the repo directory, launch the game with

```
python bob_box 
```

The game has been tested to work on the following terminals: Windows Terminal, Command Prompt, Powershell, XFCE4 Terminal, Kitty.

## The language: BobScript

The language is the main part of BobBox, it's how you play after all! The goal is to write a program which instructs Bob to move all of the boxes onto the colored victory tiles. You are scored based on the size of your program -- shorter, more elegant programs are better. When you have written your program, for a level, press F5 to run it. If you are successful, you return to the level select screen. If not, you can try again until you succeed.

### Basic syntax

The language is a very simple [Lisp](https://en.wikipedia.org/wiki/Lisp_(programming_language)) dialect. Here's an example:

```
(begin
  move_up
  (set x 5)
  (repeat x
    (begin
      (if (== x 7)
        move_up
        move_right)
      (set x (+ x 1)))))
```

The equivalent in Python is:

```
move_up()
x = 5
for x in range(x):
    if x == 7:
        move_up()
    else:
        move_right()
    x = x + 1 # This is what it really does rather than x += 1
```

Note that indentation is optional in our language.

### Keywords

There are very few keywords in our language:

repeat, while, set, begin, and if

#### repeat

A loop. Has args of number of times to repeat and a block of code to execute. Example:

```
(repeat 5 move_up)
```

#### while

A while loop. Has args of condition and a block of code to execute. Example:

```
(while (== x 5) move_up)
```

#### set

Variable assignment. Has args of variable name and value. Example:

```
(set x 5)
```

Note: set can be used to initialise a variable. All variables are global.

#### begin

Starts a code-block and executes expressions one after the other. The value of the final expression is returned. Has args of statements to execute. Example:

```
(begin move_up grab_right)
```

Notes: When executing a single expression, begin is not needed, it simply says run all the following statements.

#### if

An if statement. Has args of condition and if-true. Example:

```
(if (== x 5) move_up)
```

### Actions

There are four actions that cause Bob to move, one for each direction: `move_up`, `move_down`, `move_left`, and `move_right`.

Likewise, there are four grab directions: `grab_up`, `grab_down`, `grab_left`, and `grab_right`. These cause Bob to grab hold of a box in the given direction, so that when he later moves, the box comes with him.

Finally, there are the actions `ungrab` and `wait.` The `ungrab` action puts the box on the ground so that it no longer moves when Bob does. The `wait` action causes Bob to do nothing at all for one game tik.

### Simple operators

The simple operators list has `+ - * / // < <= > >= == `\

They do what they do in Python.

Note that they are used with prefix notation: `(+ foo bar)`





