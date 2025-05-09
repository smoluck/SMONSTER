# python
"""
Name:         SMO_DeleteAllSelSetItemPolyEdgeVert.py

Purpose:      This script is designed to:
              Delete any Selection Set in all mode
              (Item / Polygon / Edges / Vertex).
              You need to be in Item Mode to launch it.

Author:       Franck ELISABETH
Website:      https://www.linkedin.com/in/smoluck/
Created:      25/03/2019
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx

# replay name:"Delete Selection Set"
lx.eval('!select.deleteSet name:ItemSSET all:true')
lx.eval('select.type polygon')
# replay name:"Delete Selection Set"
lx.eval('!select.deleteSet name:PolygonSSET all:true')
lx.eval('select.type edge')
# replay name:"Delete Selection Set"
lx.eval('!select.deleteSet name:EdgeSSET all:true')
lx.eval('select.type vertex')
# replay name:"Delete Selection Set"
lx.eval('!select.deleteSet name:VertexSSET all:true')
# replay name:"Item"
lx.eval('select.type item')
