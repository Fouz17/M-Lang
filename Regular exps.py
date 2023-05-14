import re

# Example pattern: string should only contain alphabetic characters
variable = r'^@[a-zA-Z_]+[0-9]*[a-zA-Z_]+$'
# Example pattern: string should only contain alphabetic characters
string = r'^=\s*".*"$'
number = r'^=\s*[0-9]*\s*$'

print(re.match(string, '="5"'))

set_ = {1,2,3,4}
set_.add(14)
print(set_)


_str = ';;;;;;;;'
print(_str.replace(r';*','-'))