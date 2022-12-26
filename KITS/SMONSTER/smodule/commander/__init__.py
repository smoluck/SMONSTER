# python

__version__ = "0.20"
__author__ = "Franck Elisabeth"

import sys

python_majorver = sys.version_info.major
# print('the Highest version number 2 for 2.7 release / 3 for 3.7 release')
# print(python_majorver)

if python_majorver == 2:
    # print("do something for 2.X code")
    from SMO_Commander import *
    from SMO_Var import *
    from FCL import *
elif python_majorver >= 3:
    # print("do something for 3.X code")
    from . import FCL
