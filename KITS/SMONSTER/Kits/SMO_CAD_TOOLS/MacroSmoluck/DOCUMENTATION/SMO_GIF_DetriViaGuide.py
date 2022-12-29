# python
"""
Name:         SMO_GIF_DetriViaGuide.py

Purpose:      This script is designed to:
              Open the GIF as documentation helper

Author:       Franck ELISABETH
Website:      https://www.smoluck.com
Created:      30/05/2019
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx

filePathToOpen = lx.eval("query platformservice alias ? {kit_SMO_CAD_TOOLS:MacroSmoluck/DOCUMENTATION/DetriViaGuide.gif}")

# Open gif file
lx.eval('file.open {%s}' % filePathToOpen)

# @kit_SMO_CAD_TOOLS:MacroSmoluck/DOCUMENTATION/SMO_GIF_DetriViaGuide.py