from Parser import Parser
from Tokenizer import Tokenizer

program = open("./code.m",'r').read()

# program = "loop(@x2 -> num = 50,1,-5){\n//}\n"

lexer = Tokenizer(program)
tokens = lexer.tokenize()
analyzer = Parser(tokens)
analyzer.parse()