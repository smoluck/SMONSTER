# python
"""
Name:           SMO_CLEANUP_CycleItem_HELP.py

Purpose:        This script is designed to:
                Open the weblink to the help page

Author:         Franck ELISABETH
Website:        https://www.linkedin.com/in/smoluck/
Created:        02/11/2019
Copyright:      (c) Franck Elisabeth 2017-2022
"""

import lx

filePathToOpen = lx.eval("query platformservice alias ? {https://wp.me/p1xA5h-rb}")
# filePathToOpen = lx.eval("query platformservice alias ? {kit_SMO_CLEANUP:MacroSmoluck/DOCUMENTATION/UV_FixFlipped_and_Normalize_Repack.gif}")

# Open gif file
lx.eval('file.open {%s}' % filePathToOpen)

# @kit_SMO_CLEANUP:MacroSmoluck/DOCUMENTATION/SMO_GIF_UV_FixFlipped_and_Normalize_Repack.py