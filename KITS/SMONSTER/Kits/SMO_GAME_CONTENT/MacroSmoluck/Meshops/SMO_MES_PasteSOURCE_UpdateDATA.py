# python
"""
Name:         SMO_PasteSOURCE_UpdateDATA.py

Purpose:      This script is designed to:
              Paste the SOURCE DATA (Polygon and UVs) and save the Scene

Author:       Franck ELISABETH
Website:      https://www.linkedin.com/in/smoluck/
Created:      29/03/2019
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx

lx.eval('layer.new')
lx.eval('item.name SOURCE xfrmcore')
lx.eval('item.editorColor red')
lx.eval('paste')
lx.eval('select.typeFrom item;pivot;center;edge;polygon;vertex;ptag true')
lx.eval('!scene.save')
lx.eval('scene.close')