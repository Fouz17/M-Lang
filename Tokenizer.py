import re


class Tokenizer:
    def __init__(self, string):
        self.source = string
        self.current = 0
        self.tokens = []
        self.currentChar = self.source[0]
        self.nextChar = self.source[1]

    def advance(self):
        self.current += 1
        if (self.current < len(self.source)):
            self.currentChar = self.source[self.current]
            try:
                self.nextChar = self.source[self.current + 1]
            except:
                self.nextChar = None
        else:
            self.currentChar = None

    def tokenize(self):
        while (self.currentChar is not None):


            if (self.currentChar in '{(,)}='):
                self.tokens.append(self.currentChar)
                self.advance()
                continue

            if (self.currentChar == '-' and self.nextChar == '>'):
                self.tokens.append(self.currentChar+self.nextChar)
                self.advance()
                self.advance()
                continue

            if (self.currentChar == '"'):
                stringToken = self.currentChar
                self.advance()
                while (self.currentChar != '"'):
                    stringToken += self.currentChar
                    self.advance()
                stringToken += self.currentChar
                self.tokens.append(stringToken)
                self.advance()
                continue

            if (self.currentChar == '/' and self.nextChar == '/'):
                while (self.currentChar != '\n'):
                    self.advance()
                self.advance()
                continue

            if (self.currentChar == '/' and self.nextChar == '*'):
                self.advance()
                self.advance()
                while (self.currentChar != '*' and self.nextChar != '/'):
                    self.advance()
                self.advance()
                self.advance()
                continue

            if (self.currentChar == '@' and (re.match(r"@[a-zA-Z_]+$", self.currentChar+self.nextChar))):
                varToken = self.currentChar
                self.advance()
                varToken += self.currentChar
                while (re.match(r"@[a-zA-Z_]+[0-9]*[a-zA-Z_]*$", varToken)):
                    self.advance()
                    varToken += self.currentChar
                self.tokens.append(varToken[:len(varToken)-1])
                continue
            elif(self.currentChar == '@' and not(re.match(r"@[a-zA-Z_]+$", self.currentChar+self.nextChar))):
                self.tokens.append(self.currentChar)
                self.advance()
                continue

            if(self.currentChar != ' '):
                randomString = self.currentChar
                self.advance()
                while(self.currentChar != ' '):
                    randomString += self.currentChar
                    self.advance()
                self.tokens.append(randomString)
                self.advance()
                continue


            self.advance()
        print(self.tokens)


Tokenizer = Tokenizer('@x1123k -> num = ("hello")//"HELLO"\n')
Tokenizer.tokenize()
