# Bob Box

##What is Bob Box?
Bob Box is a box pusher game where you have to code a robot (bob) to get the boxes to the correct positions


##The language
The language is the main component of Bob Box, it's how you play after all!

### Basic syntax
The language is based on scheme, it's pretty simple. Here's an example:

```
(
    begin
    (func foo (
        begin
        (move_up)
        (set x 5)
        (repeat x (
            begin
            (if (== x 7) (
                begin
                (move_up)
                )
                (
                (move_right)
                )
            (set x (+ x 1))
            )
        ))
    ))
    (foo)
)
```
Here's what this would do in python
```python
def foo():
    move_up()
    x = 5
    for i in range(x):
        if x == 7:
            move_up()
        else:
            move_right()
        x = x + 1# This is what it actually does rather than x += 1

foo()
```

Note that indentation is optional in our language

###Keywords
There are few keywords in our language:\
repeat, while, set, begin, if and func

####repeat
A loop\
Has args of number of times to repeat and code to execute\
Example: `(repeat 5 (move_up))`

####while
A while loop\
Has args of condition and code to execute\
Example: `(while (== x 5) (move_up))`

####set
Variable setting
Args of var name and value\
Example: `(set x 5)`\
Note: set can be used to initialise a variable

####begin
Starts a code-block\
Args of statements to execute\
Example: `(begin (move_up) (grab_right))`\
Notes:When executing a single statement, begin is not required, it simply says run all the following statements

####if
An if statement\
Args of codition, if true and if false
Example: `(if (== x 5) (move_up) (move_down))`

####func
Defines a function\
Args of function name and code in function\
Example: `(func my_func (move_up))`\

###Built-in functions
There are 3 built in functions for movement, however 2 have 4 variants of them\
There are simple operators as the rest

####move
The function "move" has 4 variants; 1 for all directions. These are `move_up move_down move_left move_right`\
There are no args required for this function
It does what it says; It moves bob

####grab
The function "grab" is like move; 4 variants, 1 for each direction. The variants are `grab_up grab_down grab_left grab_right`\
There are no args required
The function "grabs" a box in the direction which allows you to move with the box. If there is no box to grab, it does nothing\
Note: grabbing a box while you already have one grabbed will cause you to ungrab the first box


####ungrab
The function "ungrab" only exists as `ungrab`\
No args are required
The function "ungrabs" any box which is grabbed

###Simple operators
The simple operators list has `+ - * / // < <= > >= == `\
They do what they do in python\
Note that they are used as such: `(+ foo bar)`

