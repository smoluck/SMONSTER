# python
"""
Name:           SMO_Cleanup_3DsMAX_FBXChannel.py

Purpose:        This script is designed to:
                Delete all 3DSMAX related Channels created
                at FBX Export in the current scene.

Author:         Franck ELISABETH
Website:        https://www.smoluck.com
Created:        19/12/2019
Copyright:      (c) Franck Elisabeth 2017-2022
"""

import lx
import modo

scene = modo.scene.current()

# ---------------------------------------#
# Delete unnecessary FBX 3DSMax Channels #
# ---------------------------------------#

lx.eval('select.itemType mesh')
# Variables
DelFBXChanMeshList = []
DelFBXChanMeshList = lx.eval('query sceneservice selection ? mesh')  # mesh item layers
for mesh in DelFBXChanMeshList:
    # mesh.select(True)
    lx.eval('smo.CLEANUP.DelChanByArg FBX_UDP3DSMAX')
    lx.eval('smo.CLEANUP.DelChanByArg FBX_MaxHandle')
lx.eval('select.drop item')
