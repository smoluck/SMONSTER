# python
"""
Name:           SMO_DeleteAllItemSelectionSet.py

Purpose:        This script is designed to:
                Delete every Item Selection set in the scene

Author:         Franck ELISABETH
Website:        https://www.linkedin.com/in/smoluck/
Created:        29/03/2019
Copyright:      (c) Franck Elisabeth 2017-2022
"""

import lx

lx.eval('select.itemType mesh')
lx.eval('!select.deleteSet SOURCE_MESH true')
lx.eval('!scene.save')
lx.eval('scene.close')