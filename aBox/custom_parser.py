# parses the code written to convert it to something we can run
from __future__ import division

from typing import List
import math
import operator as op

Symbol = str  # A Lisp Symbol is implemented as a Python str
List = list  # A Lisp List is implemented as a Python list
Number = (int, float)  # A Lisp Number is implemented as a Python int or float

movelist = [] #this could be returned -pusi

def tokenise(chars: str) -> list:
    """Convert a string of characters into a list of tokens."""

    return chars.replace("\n", " ").replace('(', ' ( ').replace(')', ' ) ').split()


def parse(program: str):
    """Read a Scheme expression from a string."""
    return read_from_tokens(tokenise(program))


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
    else:
        try:
            return int(token)
        except ValueError:
            return Symbol(token)


def equals_to(args):
    return args[0]==args[1]

def add(args):
    return args[0]+args[1]

custom_funcs = {

}

vars = {

}

macro_strings = ["up", "down", "right", "left"] # keep all lowercase

def eval(code, functions):                 #i dont get what this returns, but it should return the movelist[] -pusi
    if isinstance(code, Symbol): # a variable
        return vars.get(code)
    
    elif not isinstance(code, List):# a constant
        return code
    
    func, *arguments = code# split the list into the function and the arguments

    for i, arg in enumerate(arguments):
            if type(arg) == str and arg.lower() not in macro_strings:
                if arg in vars and func != "set":
                    arguments[i] = vars[arg]
                else:
                    arguments[i] = parse(arg)

    if func == "begin":
        for argument in arguments:
            eval(argument, functions) 

    elif func == "if": #if statement
        test, if_true, *if_false = arguments
        if eval(test, functions):
            eval(if_true, functions)
        else:
            eval(if_false)
    
    elif func == "loop":
        amount, to_run = arguments

        for i in range(amount-1):
            eval(to_run, functions)
        return eval(to_run, functions)
    
    elif func == "set":
        var_name, var_value = arguments
        actual_value = eval(var_value, functions)
        vars[var_name] = actual_value
    
    elif func == "func":
        
        name, code = arguments
        custom_funcs[name] = code

    
    else:
        try:
            function = functions[func]
            return function(arguments)
        except KeyError:
            eval(custom_funcs[func], functions)
        
        
        
