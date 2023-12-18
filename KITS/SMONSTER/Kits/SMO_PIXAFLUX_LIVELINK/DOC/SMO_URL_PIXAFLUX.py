# python
"""
Name:               SMO_URL_PIXAFLUX.py

Purpose:            This Script is designed to:
                    open the PIXAFLUX Website

Author:             Franck ELISABETH
Website:            https://www.linkedin.com/in/smoluck/
Created:            16/05/2020
Copyright:          (c) Franck Elisabeth 2017-2022
"""

import lx

filePathToOpen = lx.eval("query platformservice alias ? {kit_SMO_PIXAFLUX_LIVELINK:DOC/PIXAFLUX.url}")
lx.eval('file.open {%s}' % filePathToOpen)
