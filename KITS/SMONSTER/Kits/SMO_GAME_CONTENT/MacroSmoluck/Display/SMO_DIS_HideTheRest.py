# python
"""
Name:           SMO_Display_HideTheRest.py

Purpose:		This script is designed to:
                Add every light in the scene then Hide every other Item,
                in order to preserve the shading  on the selected element.

                Select in Item Mode or in Component Mode

Author:         Franck ELISABETH
Website:        https://www.linkedin.com/in/smoluck/
Created:        10/03/2019
Copyright:      (c) Franck Elisabeth 2017-2022
"""

import lx

lx.eval('select.itemType type:light super:true mode:add')
lx.eval('hide.unsel')
