# Lexer/tokenizer implementation
import re

RULES = {
    "<var-decl>": ["<varname><vars>-><DT><assign>;"],
    "<varname>": [r'^@[a-zA-Z_]+[0-9]*[a-zA-Z_]+$'],
    "<vars>": [",<varname>", None],
    "<DT>": ["str", "num"],
    "<assign>": [r"^=[a-zA-Z0-9]+", None],
}

def tokenize(program):
    tokens = re.findall(
        r'@[a-zA-Z_]+[0-9]*[a-zA-Z_]+|[a-zA-Z_][a-zA-Z0-9_]*|->|".*"|;|\S', program)
    print(tokens)
    return tokens

# Parser implementation


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.token_index = -1
        self.advance()

    def advance(self):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        else:
            self.current_token = None

    def retreat(self):
        self.token_index -= 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        else:
            self.current_token = None


    def parse(self):
        if (self.current_token[0] == "@"):
            return self.declaration()

    def declaration(self):
        Type = None
        while (self.current_token):
            if re.match(RULES["<varname>"][0], self.current_token) is not None:
                self.advance()
                if self.current_token == ',':
                    self.advance()
                    continue
                elif self.current_token == '->':
                    self.advance()
                    if (self.current_token in RULES["<DT>"]):
                        Type = self.current_token
                        self.advance()
                        if self.checkVariableAssignment(Type):
                            self.advance()
                            if(self.current_token != ';'):
                                raise SyntaxError("Missing semi colon")
                            self.advance()
                        else:
                            raise SyntaxError(f"Can not assign the value to type {Type}")
                    else:
                        raise SyntaxError("Invalid data type")
                else:
                    raise SyntaxError("Invalid Identifier")
            else:
                raise SyntaxError("Variable naming voilation")
        print("VALID")

    def checkVariableAssignment(self, DT):
        if (self.current_token == ';'):
            self.retreat()
            return True
        NewToken = self.current_token
        self.advance()
        NewToken += self.current_token
        if (DT == "str"):
            return re.match(r'^=\s*".*"$',NewToken) is not None
        else:
            return re.match(r'^=\s*[0-9]*\s*$',NewToken) is not None

    def variable_type(self):
        if self.current_token in ['int', 'float', 'string']:
            variable_type = self.current_token
            self.advance()
            return variable_type
        else:
            raise SyntaxError("Invalid variable type")


# Usage example
program = '@x1_ ,@x2_,@x3_ -> str = "5sadasdas oi324in sd,c9 79 ";'
tokens = tokenize(program)
parser = Parser(tokens)
result = parser.parse()
# print(result)  # Output: ('x', 'int')
