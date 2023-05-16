from Parser import Parser
from Tokenizer import Tokenizer

program = open("./code.m",'r').read()

# program = "@x1 -> num = +1;/*loop(@x2 -> num = 50,0,++1){    @x3 -> num = -1;loop(@x4 -> num = 50,0,1){@x5 -> num = -1;}  @x6 -> num = +1;}*/"

lexer = Tokenizer(program)
tokens = lexer.tokenize()
analyzer = Parser(tokens)
analyzer.parse()