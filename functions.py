class Func:
    def __init__(self,name, body):
        self.name = name
        self.body = body


class FuncallStmnt:
    def __init__(self, name, args):
        self.name = name
        self.args = args
    

class ReturnStmnt:
    def __init__(self,expr):
        self.expr = expr


def expect_token(lexer, *token_types):
    token = lexer.next_token()
    if not token:
        print(lexer.loc().get_data(),': ERROR: expected', "or ".join(token_types),  'but got the end of file\n')
        return False


    for ttype in token_types:
        if token.type == ttype:
            return token

    
    print(lexer.loc().get_data(),': ERROR: expected', " or ".join(token_types),  'but got', token.type)
    return False


def parse_type(lexer):
    return_type = expect_token(lexer, "TOKEN_NAME")
    if return_type.value != "int":
        print(return_type.loc().get_data(),": ERROR: unexpected type ", return_type.value)    
        return False

    return "TYPE_INT"



def parse_arglist(lexer):
    if not expect_token(lexer, "TOKEN_OPAREN"): 
        return False
    arglist = []

    expr = expect_token(lexer, "TOKEN_STRING", "TOKEN_NUMBER", "TOKEN_CPAREN")
    if not expr: 
        return False
    if expr.type == 'TOKEN_CPAREN':
        return arglist

    arglist.append(expr.value)

    while True:
        expr = expect_token(lexer, "TOKEN_CPAREN", "TOKEN_COMMA")
        if not expr: 
            return False
        if expr.type == "TOKEN_CPAREN": 
            break

        expr = expect_token(lexer, "TOKEN_STRING", "TOKEN_NUMBER")
        if not expr: 
            return False

        arglist.append(expr.value)

    
    return arglist


def parse_block(lexer):
    if not expect_token(lexer, "TOKEN_OCURLY"): 
        return False
    #if not expect_token(lexer, "TOKEN_CCURLY"): return False

    block = []

    while True:
        name = expect_token(lexer, "TOKEN_NAME", "TOKEN_CCURLY")
        if not name:
            return False
        if name.type == "TOKEN_CCURLY":
            break

        if name.value == "return":
            expr = expect_token(lexer, "TOKEN_NUMBER", "TOKEN_STRING")
            if not expr: 
                return False
            block.append(ReturnStmnt(expr.value))
        else:
            arglist = parse_arglist(lexer)
            # if not arglist:
            #     line_number,filename = current_line_number()
            #     print(f"Line {line_number} in file {filename}", "arglist not found")
            #     pprint(block)
            #     return False
            
            block.append(FuncallStmnt(name, arglist))

        if not expect_token(lexer, "TOKEN_SEMICOLON"): 
            return False

    return block 

def parse_function(lexer):
    return_type = parse_type(lexer)
    if not return_type:
        return False
    assert return_type == "TYPE_INT"

    name = expect_token(lexer, "TOKEN_NAME")
    if not name:
        return False

    if not expect_token(lexer, "TOKEN_OPAREN"): 
        return False
    if not expect_token(lexer, "TOKEN_CPAREN"): 
        return False

    func_body = parse_block(lexer)

    return Func(name, func_body)