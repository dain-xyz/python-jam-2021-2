# parses the code written to convert it to something we can run
from __future__ import division

from typing import List
import math
import operator
from functools import reduce

from utils import Action

Symbol = str  # A Lisp Symbol is implemented as a Python str
List = list  # A Lisp List is implemented as a Python list
Number = (int, float)  # A Lisp Number is implemented as a Python int or float
Boolean = bool


def tokenise(chars: str) -> list:
    """Convert a string of characters into a list of tokens."""

    return chars.replace("\n", " ").replace('(', ' ( ').replace(')', ' ) ').split()


def read_from_tokens(tokens: list):
    """Read an expression from a sequence of tokens."""
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF')
    token = tokens.pop(0)
    if token == '(':
        L = []
        while tokens[0] != ')':
            L.append(read_from_tokens(tokens))
        tokens.pop(0)  # pop off ')'
        return L
    elif token == ')':
        raise SyntaxError('unexpected )')
    
    elif token == "true":
        return True
    
    elif token == "false":
        return False

    elif token == "none":
        return None

    else:
        try:
            return int(token)
        except ValueError:
            return Symbol(token)


def parse(program: str):
    """Read a Scheme expression from a string."""
    return read_from_tokens(tokenise(program))


actions = {
    "move-up": Action.move_up,
    "move-down": Action.move_down,
    "move-left": Action.move_left,
    "move-right": Action.move_right,
    "grab-up": Action.grab_up,
    "grab-down": Action.grab_down,
    "grab-left": Action.grab_left,
    "grab-right": Action.grab_right,
    "ungrab": Action.ungrab,
    "wait": Action.wait
}


basic_functions = {
    "+": lambda first, *rest: reduce(operator.add, rest, first),
    "-": lambda first, *rest: reduce(operator.sub, rest, first),
    "*": lambda first, *rest: reduce(operator.mul, rest, first),
    "/": lambda first, *rest: reduce(operator.truediv, rest, first),
    "//": lambda first, *rest: reduce(operator.floordiv, rest, first),
    "<": operator.lt,
    "<=": operator.le,
    ">": operator.gt,
    ">=": operator.ge,
    "==": operator.eq,
    "if": lambda cond, if_true, if_false: if_true if cond else if_false
}


def eval2(code):
    if isinstance(code, Symbol):
        return (yield ("lookup", code))
    
    elif not isinstance(code, List):
        return code
    
    func, *arguments = code

    if func == "begin":
        for argument in arguments:
            value = yield from eval2(argument)
        
        return value
    
    elif func == "set":
        var_name, var_value = arguments
        actual_value = yield from eval2(var_value)
        return (yield ("set", var_name, actual_value))
    

    elif func == "repeat":
        times, body = arguments
        times_value = yield from eval2(times)
        res = None

        for _ in range(times_value):
            res = yield from eval2(body)
        
        return res
    

    elif func == "while":
        cond, body = arguments
        cond_value = yield from eval2(cond)
        res = None

        while cond_value := (yield from eval2(cond)):
            res = yield from eval2(body)

        return res
    

    # define a function (cannot take arguments yet)
    elif func == "func":
        code = arguments[0]
        return (yield ("func", code))

    
    elif func in basic_functions:
        evalled_args = []
        for arg in arguments:
            evalled = yield from eval2(arg)
            evalled_args.append(evalled)

        return (yield (func, *evalled_args))


    else: # a user-defined function
        body = yield ("lookup", func)
        return (yield from eval2(body))



def interpret(parsed):
    reply = None
    variables = {}

    interpreter = eval2(parsed)

    try:
        while True:
            instruction, *args = interpreter.send(reply)

            if instruction == "set":
                name, value = args
                variables[name] = value
                reply = None
                yield
            
            elif instruction == "lookup":
                name = args[0]

                if name in actions:
                    yield actions[name]
                    reply = None
                
                else:
                    reply = variables[name]
            
            elif instruction == "func":
                reply = args[0]
                # name, code = args
                # variables[name] = code
                # reply = None
                yield

            elif instruction in basic_functions:
                func = basic_functions[instruction]
                reply = func(*args)
                yield
            
            else:
                # print(f"{instruction=}, {args=}")
                reply = instruction # ?
                yield
    
    except StopIteration as e:
        return e


if __name__ == "__main__":
    test_code = """(
        begin
        (set x 5)
        (set y 6)
        (set add (+ x y))
        (set res
            (if (< 3 4)
                (begin (set foo -1) (set bar -4))
                grab-left))
        (set inc1 1)
        (set inc2 1)
        (repeat 5 (begin (set inc1 (+ inc1 1)) (set inc2 (- inc2 1))))
        
        (set inc3 0)
        (set while-result (while (< inc3 5)
            (begin (set inc3 (+ inc3 1)))
        ))
        (set thing-before 0)
        (set my-func
            (func
                (begin
                    (set thing-before 5)
                    move-up
                )
            )
        )
        (my-func)
        5
        move-right
    )"""

    parsed = parse(test_code)
    for x in interpret(parsed):
        if isinstance(x, Action):
            print(x)

