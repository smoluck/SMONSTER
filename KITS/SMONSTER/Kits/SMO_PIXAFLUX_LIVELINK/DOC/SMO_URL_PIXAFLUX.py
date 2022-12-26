# python
"""
# Name:         SMO_URL_PIXAFLUX.py
# Version:      1.0
#
# Purpose:      This script is designed to:
#               open the PIXAFLUX Website
#
# Author:       Franck ELISABETH
# Website:      https://www.smoluck.com
#
# Created:      16/05/2020
# Copyright:    (c) Franck Elisabeth 2017-2022
"""
import lx
filePathToOpen = lx.eval("query platformservice alias ? {kit_SMO_PIXAFLUX_LIVELINK:DOC/PIXAFLUX.url}")
lx.eval('file.open {%s}' % filePathToOpen)
