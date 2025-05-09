# python
"""
Name:         SMO_GIF_STRI_Ring_to_Quad_Round.py

Purpose:      This script is designed to:
              Open the GIF  as documentation helper

Author:       Franck ELISABETH
Website:      https://www.linkedin.com/in/smoluck/
Created:      30/05/2019
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx

filePathToOpen = lx.eval("query platformservice alias ? {kit_SMO_CAD_TOOLS:MacroSmoluck/DOCUMENTATION/TRI_Ring_to_Quad_Round.gif}")

# Open gif file
lx.eval('file.open {%s}' % filePathToOpen)