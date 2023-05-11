import os, sys
from functions import FuncallStmnt 
from Lexer import Lexer
from functions import parse_function

filepath = sys.argv[1]


if not os.path.isfile(filepath):
    print("ERROR: The file {filename} does not exist.")

else:  
    f = open(filepath, "r")
    source_code = f.read()

    lexer = Lexer(filepath, source_code)
    parsed = parse_function(lexer)
    if not parsed: exit(69)

   
    # token = lexer.next_token()
    # while(token):
    #     print(token.value)
    #     token = lexer.next_token()
    for stmnt in parsed.body:
        if isinstance(stmnt, FuncallStmnt):
            if stmnt.name.value == "printf":
                print(f"print('{','.join(stmnt.args)}')")
            else:
                print("ERROR: unkown function", stmnt.name.loc().get_data())
                exit(69)
