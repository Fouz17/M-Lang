# Lexer/tokenizer implementation
import re

RULES = {
    "<var-decl>": ["<varname><vars>-><DT><assign>;"],
    "<varname>": [r'^@[a-zA-Z_]+[0-9]*[a-zA-Z_]*$'],
    "<vars>": [",<varname>", None],
    "<DT>": ["str", "num"],
    "<assign>": [r"^=[a-zA-Z0-9]+", None],
}


def tokenize(program):
    tokens = re.findall(
        r'@[a-zA-Z_]+[0-9]*[a-zA-Z_]*|[a-zA-Z_][a-zA-Z0-9_]*|[0-9]+|->|".*"|;|\S', program)
    print(tokens)
    return tokens

# Parser implementation


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.variableStack = set({})
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
        if self.token_index > 0:
            self.current_token = self.tokens[self.token_index]
        else:
            self.current_token = None

    def parse(self):
        while(self.current_token):
            if(self.current_token == ";"):
                self.advance()
            elif (self.current_token[0] == "@"):
                self.declaration()
            else:
                raise SyntaxError("Invalid Identifier")
    def declaration(self):
        Type = None
        Terminate = False
        while (not Terminate):
            if re.match(RULES["<varname>"][0], self.current_token) is not None:
                self.checkForDuplicateVariables()
                self.variableStack.add(self.current_token)
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
                            if (self.current_token != ';'):
                                raise SyntaxError("Missing semi colon")
                            self.advance()
                            Terminate = True
                        else:
                            raise SyntaxError(
                                f"Can not assign the value to type {Type}")
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
            return re.match(r'^=\s*".*"$', NewToken) is not None
        else:
            return re.match(r'^=\s*[0-9]*\s*$', NewToken) is not None

    def checkForDuplicateVariables(self):
        if (self.current_token in self.variableStack):
            raise NameError(
                f"variable {self.current_token } has already been declared.")


# Usage example
program = '@x1_ ,@x2_,@x3_ -> str = "5sadasdas oi324in sd,c9 79 ";;'
tokens = tokenize(program)
parser = Parser(tokens)
result = parser.parse()
# print(result)  # Output: ('x', 'int')
