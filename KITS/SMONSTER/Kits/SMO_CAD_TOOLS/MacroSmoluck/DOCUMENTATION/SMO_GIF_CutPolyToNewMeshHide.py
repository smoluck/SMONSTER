#python
#---------------------------------------
# Name:         SMO_GIF_CutPolyToNewMeshHide.py
# Version: 1.01
#
# Purpose:      This script is designed to:
#               Open the GIF  as documentation helper
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      30/05/2019
# Modified:		30/05/2019
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------
import lx
filePathToOpen = lx.eval("query platformservice alias ? {kit_SMO_CAD_TOOLS:MacroSmoluck/DOCUMENTATION/CutPolyToNewMeshHide.gif}")

# Open gif file
lx.eval('file.open {%s}' % filePathToOpen)

# @kit_SMO_CAD_TOOLS:MacroSmoluck/DOCUMENTATION/SMO_GIF_CutPolyToNewMeshHide.py