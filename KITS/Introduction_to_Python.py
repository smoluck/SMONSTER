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
print("""text text text text text text text text text text text text text text text text text""")

print("-------------------------------------")
"""to get the list of all module tht are related to a value type
for instance on strings"""
text = "bla bla"
type(text)
dir(str)            # a list of specific modules attached to that value type will be listed.
text.capitalize()   # for instance will return "Bla bla". CFirst letter of  the chain will be high Case.


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


f_a = 1     # 1 here is an integer type of value
f_b = "3"   # 3 here is a String type of value

type(f_a)   # will return an "int" for "Integer"
type(f_b)   # will return a "str" for "String"

"""f_a + f_b will return an error, so we need to convert the value type."""
f_a + int(f_b)


print("\n")
print("----- about ------ Math Functions --------------------------")
import math

print('Multiplications')
math_a = 8*2
print(math_a)

print('Power of 2')
math_b = 8**2
print(math_b)


print("\n")
print("----- about ------ Comparison Functions --------------------------")

compare_a_to_b = (math_a == math_b)
print(compare_a_to_b)       # this will be a Boolean result: true OR false

print('Power of 2')
math_b = 8**2
print(math_b)


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


print("\n")
print("----- SubClass state of various variable -----")
state = issubclass(Result, scls)
print("Does 'scls' is a subclass of 'Result' ?", "\n", "the answer is %s" % state)


print("\n")
print("----- about ------ Join Function --------------------------")

colors = ['red', 'green', 'blue']
rgb = '\n'.join(colors)
s = f"The RGB colors are:\n{rgb}"
print(s)

print(colors.index('blue'))   # can output the index number linked to the value "blue"


print("\n")
print("----- about ------ List modules --------------------------")
colors = ['red', 'green', 'blue']
colors.append("yellow")         # append let us Add a value to a list.
colors.clear()                  # clear will clear all the values in it.
colors.copy()
colors.remove()
colors.count()
colors.insert(1, 'test')        # insert will add a value in the list at a specific index. Here at the index 1


print("\n")
print("----- about ------ Dict modules --------------------------")
# dict have no index but keys to define what you can call.
# instead of list[x] where x is the index
# dict["key"] will return the value at that key. You can output multiple values from it

d = {}
d = {'name': 'Kent', 'givenname': 'Clark'}
print(d)
d['job'] = 'Super Hero'     # 'job' is not part of the dict already, so it will add that new key and the value of it.
print(d)
print(d.keys())             # will return all the keys in it.
print(d.values())           # will return all the values in it.

# you can also only print the Values
for x in d:
    print(d[x])

# you can also only print the Keys
for x in d:
    print(x)

# you can also print the key and the values that way in the same line
for x in d:
    print(x, ':', d[x])

# you can also print the key and the values that way in the same line but now with a tabulation on both side of the separator ":"
for x in d:
    print(x, '\t:\t', d.values())

# if you want a clean list out of those keys, you will still have to get them through this to have a clean list format.
list(d.keys())

