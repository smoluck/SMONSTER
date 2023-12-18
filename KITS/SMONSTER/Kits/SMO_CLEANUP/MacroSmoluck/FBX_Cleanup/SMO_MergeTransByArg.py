# python
"""
Name:         SMO_MergeTransByArg.py

Purpose:      This script is designed to:
              Merge the multiple Pos/Rot/Sca Transform into only one Transform Matrix.
              via String Argument to define wich Transform to update: Position / Rotation / Scale
              Select the Mesh item and launch it.

Author:       Franck ELISABETH
Website:      https://www.linkedin.com/in/smoluck/
Created:      03/03/2020
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import modo

scene = modo.Scene()
scn = scene.selected[0]
locsup = modo.LocatorSuperType(scn)
pos = locsup.position
rot = locsup.rotation
sca = locsup.scale

# ------------- ARGUMENTS Test
TransMode = 0
# Searched = "UVChannel_1"
# OutputName = "TargetUVMap"
# ------------- ARGUMENTS ------------- #
# args = lx.args()
# lx.out(args)

# PreTransform = int(args[0])
# lx.out('PreTransform search type:', PreTransform)
# ------------- ARGUMENTS ------------- #


transformsStack = [xfrm for xfrm in locsup.transforms]
transformsStack.reverse()

for n, xfrm in enumerate(transformsStack):
    print(xfrm.name)
    if xfrm == pos and TransMode == 0:
        if transformsStack[n + 1].type == 'position':
            scene.select([transformsStack[n + 1], xfrm])
            lx.eval('transform.merge rem:1')
    if xfrm == rot and TransMode == 1:
        if transformsStack[n + 1].type == 'rotation':
            scene.select([transformsStack[n + 1], xfrm])
            lx.eval('transform.merge rem:1')
    if xfrm == sca and TransMode == 2:
        if transformsStack[n + 1].type == 'scale':
            scene.select([transformsStack[n + 1], xfrm])
            lx.eval('transform.merge rem:1')
