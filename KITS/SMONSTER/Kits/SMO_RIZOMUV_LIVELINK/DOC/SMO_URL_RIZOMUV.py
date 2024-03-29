# python
"""
Name:           SMO_URL_RIZOMUV.py

Purpose:        This script is designed to:
                Open the RIZOM-LAB Website

Author:         Franck ELISABETH
Website:        https://www.linkedin.com/in/smoluck/
Created:        16/05/2020
Copyright:      (c) Franck Elisabeth 2017-2022
"""

import lx

filePathToOpen = lx.eval("query platformservice alias ? {kit_SMO_RIZOMUV_LIVELINK:DOC/RIZOMUV.url}")
lx.eval('file.open {%s}' % filePathToOpen)
