# python
# Base python principles
"""
'' and "" are equivalent
"" are more useful especially for text string that require '
Avoid mixing up '' and "" inside the same python script

more references:
https://www.pythontutorial.net/python-basics/python-backslash/
"""

print("----- about ------ Printing Data --------------------------")
"""
function print to print data
"""

print('I love Modo community')
print("I love Modo community")

print("-------------------------------------")
print("I'm Franck")

"""
print('I'm Franck')

return error
"""

print("-------------------------------------")
"""
to print in line
"""

print(
    """text text text text text text text text text text text text text text text text text text text text text text text""")



print("\n")
print("----- about ------ Backslash and Special Characters --------------------------")
'''
Special characters
slash = /
AntiSlash (BackSlash) = \

\n          # New Line
\f          # page up
\v          # tabulation (horizontal)
\t          # tabulation (horizontal)
\r          # raise
'''

print("a\nb")
"""
a
b
"""

print("\u2764")
"""
an heart icon "❤"
"""

"""
name = "Allen Hastings"
print("User's Name:", name)
"""

""" you can put a backslash before  a ' sign in order to ignore it in code """
name = "Allen Hastings"
print("User\'s Name:", name)



print("\n")
print("----- about ------ Raw Strings --------------------------")
"""
use Raw String to be sure the "/n" or "/v" are not interpreted as code. via (r"text")
"""

""" This example will raise an error
print("c:\temp\new folder")

it will print the data like this:
c:  emp
ew folder

instead use:
"""
print(r"c:\temp\new folder")



print("\n")
print("----- about ------ Numbers --------------------------")
""" integers, float

integers are numbers with no decimal
float can use decimal

both can be positive or negative
"""
print("----- Integers -----")
integer = int()
i_a = 2
i_b = -5
print(integer, i_a, i_b)

print("----- Floats -----")
FLOAT = float()
f_pos = 1548.687
f_neg = -1549.00
print(FLOAT, f_pos, f_neg)


print("\n")
print("----- about ------ Booleans --------------------------")
""" booleans have only 2 states:    True or False
Consider them as a switch button.
"""
print("----- Booleans -----")
boolean = bool()
state_on = True
state_off = False

print("your reply to that question is", state_off)
print("Scripting is awesome ?", "\n", state_on)


print("\n")
print("----- about ------ Subclass --------------------------")
""" Subclass are embedded definitions of string / numbers / boolean
there is already class built in python """


# Class scls
class scls():
    text = "this is the text"


# Class Result
class Result(scls):
    data = [scls]


print("----- SubClass state of various variable -----")
state = issubclass(Result, scls)
print("Does 'scls' is a subclass of 'Result' ?", "\n", "the answer is %s" % state)


print("\n")
print("----- about ------ Join Function --------------------------")

colors = ['red', 'green', 'blue']
rgb = '\n'.join(colors)
s = f"The RGB colors are:\n{rgb}"
print(s)
