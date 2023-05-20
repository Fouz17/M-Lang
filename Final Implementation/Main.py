from Parser import Parser
from Tokenizer import Tokenizer

# path = "./code.m"
# print(__name__)
# if(__debug__):
path = "./final implementation/code.m"
program = open(path,'r').read()

# program = "loop(@x2 -> num = 50,1,-5){\n//}\n"

lexer = Tokenizer(program)
tokens = lexer.tokenize()
analyzer = Parser(tokens)
analyzer.parse()