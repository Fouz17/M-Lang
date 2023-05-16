from Tokenizer import Tokenizer
import re


RULES = {
    "<var-decl>": ["<varname><vars>-><DT><assign>;"],
    "<varname>": [r'^@[a-zA-Z_]+[0-9]*[a-zA-Z_]*$'],
    "<vars>": [",<varname>", None],
    "<DT>": ["str", "num"],
    "<assign>": [r"^=[a-zA-Z0-9]+", None],
    "<loop-decl>": ["loop(<init>,N1,N2)"],
    "<init>": ["varname-><L-DT><L-assign>"],
    "<L-DT>": ["num"],
    "<L-assign>": [r"^=[0-9]+"],
}

# Parser implementation
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.variableStack = set({})
        self.token_index = -1
        self.advance()
        self.ScopeStack = []

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
        while (self.current_token):
            if (self.current_token == ";"):
                self.advance()
            elif (self.current_token[0] == "@"):
                self.declaration()
            elif (self.current_token == "loop"):
                self.advance()
                self.parseLoop()
            elif (self.current_token == '}' and len(self.ScopeStack) > 0):
                self.ScopeStack.pop()
                break
            else:
                raise SyntaxError(f"Invalid Identifier {self.current_token}")

    def parseLoop(self):
        Terminate = False
        while (not Terminate):
            if self.current_token == "(":
                self.advance()
                self.checkLoopInitialization()
                NewToken = self.combineLoopCondsAndINCDEC()
                if (re.match(r'^[0-9]+,[-+]*[0-9]+[)]$', NewToken)):
                    if (self.current_token == '{'):
                        self.loopStatements()
                        self.advance()
                        Terminate = True
                    else:
                        raise SyntaxError(
                            "Unexpected identifier  Expected '{' ")
                else:
                    raise SyntaxError("Unexpected identifier")
            else:
                raise SyntaxError(
                    f"Invalid Identifier Expected '(' given '{self.current_token}'")
        print("VALID LOOP")

    def loopStatements(self):
        while (self.current_token != '}'):
            self.ScopeStack.append(self.current_token)
            self.advance()
            self.parse()

    def combineLoopCondsAndINCDEC(self):
        NewToken = self.current_token
        self.advance()
        NewToken += self.current_token
        self.advance()
        NewToken += self.current_token
        self.advance()
        NewToken += self.current_token
        self.advance()
        if ('-' in NewToken or '+' in NewToken):
            NewToken += self.current_token
            self.advance()
        return NewToken

    def checkLoopInitialization(self):
        if re.match(RULES["<varname>"][0], self.current_token) is not None:
            self.checkForDuplicateVariables()
            self.variableStack.add(self.current_token)
            self.advance()
            if self.current_token == ',':
                raise SyntaxError("Invalid Identifier")
            elif self.current_token == '->':
                self.advance()
                if (self.current_token == "num"):
                    Type = "num"
                    self.advance()
                    NewToken = self.current_token
                    self.advance()
                    NewToken += self.current_token
                    if re.match(r'^=\s*[0-9]*\s*$', NewToken):
                        self.advance()
                        if (self.current_token != ','):
                            raise SyntaxError("Expected ','")
                        self.advance()
                    else:
                        raise SyntaxError(
                            f"Can not assign the value to type {Type}")
                else:
                    raise SyntaxError(
                        "Invalid data type in loop initialization expected 'num'")
            else:
                raise SyntaxError("Invalid Identifier")
        else:
            raise SyntaxError("Variable naming voilation")

    def checkVariableAssignment(self, DT):
        if (self.current_token == ';'):
            self.retreat()
            return True
        NewToken = self.current_token
        self.advance()
        NewToken += self.current_token
        if(self.current_token in '-+'):
            self.advance()
            NewToken += self.current_token
        if (DT == "str"):
            return re.match(r'^=\s*".*"$', NewToken) is not None
        else:
            return re.match(r'^=\s*[-+]*[0-9]*\s*$', NewToken) is not None

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
        print("VALID DECLARATION")

    def checkForDuplicateVariables(self):
        if (self.current_token in self.variableStack):
            raise NameError(
                f"variable {self.current_token } has already been declared.")


# Usage example
program = '@x1 -> num = 1;\nloop(@x2 -> num = 50,0,-1){@x3 -> num = -1;loop(@x4 -> num = 50,0,-1){@x5 -> num = -1;}@x6 -> num = +1;}'
lexer = Tokenizer(program)
tokens = lexer.tokenize()
parser = Parser(tokens)
result = parser.parse()
