# python
"""
Name:           SMO_URL_MARMOSET.py

Purpose:		This script is designed to:
                Open the MARMOSET Website

Author:         Franck ELISABETH
Website:        https://www.smoluck.com
Created:        16/05/2020
Copyright:      (c) Franck Elisabeth 2017-2022
"""

import lx

filePathToOpen = lx.eval("query platformservice alias ? {kit_SMO_MARMOSET_LIVELINK:DOC/MARMOSET.url}")
lx.eval('file.open {%s}' % filePathToOpen)
