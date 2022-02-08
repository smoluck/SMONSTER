# python
import sys
python_majorver = sys.version_info.major
# print('the Highest version number 2 for 2.7 release / 3 for 3.7 release')
# print(python_majorver)

if python_majorver == 2 :
    # print("do something for 2.X code")
    from commander import *
elif python_majorver >= 3 :
    # print("do something for 3.X code")
    pass