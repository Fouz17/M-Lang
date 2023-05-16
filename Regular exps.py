import re

# Example pattern: string should only contain alphabetic characters
variable = r'^@[a-zA-Z_]+[0-9]*[a-zA-Z_]+$'
# Example pattern: string should only contain alphabetic characters
string = r'^=\s*".*"$'
number = r'^=\s*[0-9]*\s*$'
loopNumberReg = r'^[0-9]+,-*[0-9]+[)]+$'

# print(re.match(loopNumberReg, '5,-5)'))

print(re.findall(r'@[a-zA-Z_]+[0-9]*[a-zA-Z_]*|[a-zA-Z_][a-zA-Z0-9_]*|[0-9]+|->|".*"|;|\S', "loop sde32"))
