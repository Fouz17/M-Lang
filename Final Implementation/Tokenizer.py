import re


class Tokenizer:
    def __init__(self, string):
        self.source = string
        self.current = 0
        self.tokens = []
        self.tokenInfo = []
        self.currentChar = self.source[0]
        self.nextChar = self.source[1]
        self.line = 1
        self.col = 1

    def advance(self):
        self.current += 1
        if (self.currentChar == "\n"):
            self.col = 1
            self.line += 1
        else:  # (self.currentChar == " "):
            self.col += 1

        if (self.current < len(self.source)):
            self.currentChar = self.source[self.current]
            try:
                self.nextChar = self.source[self.current + 1]
            except:
                self.nextChar = None
        else:
            self.currentChar = None

    def retreat(self):
        self.current -= 1
        self.col -= 1
        if (self.current > 0):
            self.currentChar = self.source[self.current]
            try:
                self.nextChar = self.source[self.current + 1]
            except:
                self.nextChar = None
        else:
            self.currentChar = None

    def insertInfoObject(self):
        self.tokenInfo.append({"Line": self.line, "Col": self.col})

    def append(self, token):
        self.tokens.append(token)
        self.tokenInfo[len(self.tokenInfo)-1]["Token"] = token

    def tokenize(self):
        while (self.currentChar is not None):

            if (self.currentChar == " " or self.currentChar == "\n"):
                self.advance()
                continue

            if (self.currentChar in '{(,)}=;'):
                self.insertInfoObject()
                self.append(self.currentChar)
                self.advance()
                continue

            if (self.currentChar == '-' and self.nextChar == '>'):
                self.insertInfoObject()
                self.append(self.currentChar+self.nextChar)
                self.advance()
                self.advance()
                continue

            if (self.currentChar in '-+' and re.match(r"[0-9]$", self.nextChar)):
                self.insertInfoObject()
                numericalToken = self.currentChar
                self.advance()
                numericalToken += self.currentChar
                while (re.match(r"[-+][0-9]+$", numericalToken)):
                    self.advance()
                    numericalToken += self.currentChar
                self.append(numericalToken[:len(numericalToken)-1])
                continue
            elif (self.currentChar in "+-"):
                self.insertInfoObject()
                self.append(self.currentChar)
                self.advance()
                continue

            if (self.currentChar == '"'):
                self.insertInfoObject()
                stringToken = self.currentChar
                self.advance()
                while (self.currentChar != '"'):
                    stringToken += self.currentChar
                    self.advance()
                stringToken += self.currentChar
                self.append(stringToken)
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
                self.insertInfoObject()
                varToken = self.currentChar
                self.advance()
                varToken += self.currentChar
                while (re.match(r"@[a-zA-Z_]+[0-9]*[a-zA-Z_]*$", varToken)):
                    self.advance()
                    varToken += self.currentChar
                self.append(varToken[:len(varToken)-1])
                continue
            elif (self.currentChar == '@' and not (re.match(r"@[a-zA-Z_]+$", self.currentChar+self.nextChar))):
                self.insertInfoObject()
                self.append(self.currentChar)
                self.advance()
                continue

            if (self.currentChar == '\n'):
                self.advance()
                continue

            if (self.currentChar != ' '):
                self.insertInfoObject()
                randomString = self.currentChar
                self.advance()
                while (self.currentChar != ' '):
                    if (self.currentChar in "{(,)}=;-@"):
                        self.retreat()
                        break
                    randomString += self.currentChar
                    self.advance()
                self.append(randomString)
                self.advance()
                continue

            self.advance()

        # print(self.tokens)
        # # print(self.tokenInfo)
        # for i in range(len(self.tokenInfo)):
        #     print(self.tokenInfo[i])
        return self.tokenInfo
