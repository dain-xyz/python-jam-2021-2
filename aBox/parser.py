# a parser for our lisp like language

def tokenise(statement: str)-> list[str]:
    result = statement
    statement = statement.replace("(", " ( ").replace(")", " ) ")
    return statement.split()


def parse(program: str) -> list[str]:
    tokens = tokenise(program)
    return listify(tokens)

def listify(tokens: list[str]) -> list:
    
    current_token = tokens.pop(0) # remove the first token and store it in current_token

    if current_token == "(":
        new_list = []
        while tokens[0] != ")": # end of statement
            new_list.append(listify(tokens))
        tokens.pop(0) # end of statement reached
        return new_list
    
    elif current_token == ")": # Syntax error
        return "Syntax Error"
    
    else: # int
        try:
            return int(current_token)
        except ValueError:
            return current_token

    


if __name__ == "__main__":
    print(parse("(repeat 5 ((move up) (move left)))"))
    




