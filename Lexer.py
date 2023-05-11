from Loc import Loc
from Token import Token

   
class Lexer:
    def __init__(self, file_path, source):
        self.file_path = file_path
        self.source = source
        self.cursor = 0 #keep track of the program
        self.bol = 0 #beggining of line
        self.row = 0
        #self.cur_char = self.source[self.cursor]

    def is_not_empty(self):
        #print("length is:", len(self.source), "\n" )
        #print("position is:", self.cursor,"\n")
        return self.cursor < len(self.source)

    def is_empty(self):
        return not self.is_not_empty()

    def chop_char(self):
        if self.is_not_empty():
            cur_char = self.source[self.cursor]
            self.cursor += 1
            if cur_char == "\n":
                self.bol = self.cursor
                self.row += 1

    def loc(self):
        return Loc(self.file_path, self.row,self.cursor - self.bol)

    def trim_left(self):
        while self.is_not_empty and self.source[self.cursor].isspace():
            self.chop_char()


    def drop_line(self):
        while self.is_not_empty and self.source[self.cursor] != "\n":
            #print("drop line: ", self.source[self.cursor])
            self.chop_char()

        if self.is_not_empty():
            self.chop_char()

    def next_token(self):
        if self.is_empty():
            return False

        self.trim_left()

        

        while self.is_not_empty  and self.source[self.cursor] == "#":
            self.drop_line()
            self.trim_left()

        # token = Token()
        # token.loc = self.loc
        loc = self.loc()
        first = self.source[self.cursor]

        

        loc = self.loc
        if self.source[self.cursor].isalpha():
            index = self.cursor
            while self.is_not_empty and self.source[self.cursor].isalnum():
                self.chop_char()

            value = self.source[index:self.cursor]
            return Token(loc,"TOKEN_NAME", value)

        literal_tokens = {
            "(" : "TOKEN_OPAREN",
            ")" : "TOKEN_CPAREN",
            "{" : "TOKEN_OCURLY",
            "}" : "TOKEN_CCURLY",
            "," : "TOKEN_COMMA",
            ";" : "TOKEN_SEMICOLON",
        }

        if  first in literal_tokens:
            self.chop_char()
            return Token(loc, literal_tokens[first], first)
        

        #digits
        if first.isdigit():
            start = self.cursor
            while self.is_not_empty() and self.source[self.cursor].isdigit():
                self.chop_char()

            value = int(self.source[start:self.cursor])
            return Token(loc, "TOKEN_NUMBER", value)

        #strings
        if first == '"':
            self.chop_char()
            start = self.cursor
            while self.is_not_empty() and self.source[self.cursor] != '"':
                self.chop_char()
            
            


            if self.is_not_empty():
                endOfString = self.cursor - start
                text = self.source[start:self.cursor]
                self.chop_char()
                text_token = Token(loc, "TOKEN_STRING", text)
                return text_token

            location = self.loc()
            print("ERROR: Unclosed string literal\n", location.display())
            return False