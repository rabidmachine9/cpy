class Token:
    def __init__(self, loc, token_type, value):
        self.loc = loc
        self.type = token_type
        self.value = value