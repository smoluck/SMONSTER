# python
"""
# Name:         SMO_Cleanup_DelPreTransform.py
# Version:      1.0
#
# Purpose:  This script is designed to:
#           Delete all 3DSMAX related PreTransform Channels created at
#           FBX Export in the current scene. Position / Rotation / Scale
#
# Author:       Franck ELISABETH
# Website:      https://www.smoluck.com
#
# Created:      03/03/2020
# Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import modo

scene = modo.scene.current()


# # ------------- ARGUMENTS Test
# PreTransform = 1
# FreezeRot = 1
# # ------------- ARGUMENTS ------------- #
args = lx.args()
lx.out(args)

MergeTransRot = int(args[0])
lx.out('Merge Transform Rotation:', MergeTransRot)

FreezeRot = int(args[1])
lx.out('Freeze Rotation:', FreezeRot)
# # ------------- ARGUMENTS ------------- #




# mesh.select(True)
lx.eval('select.type polygon')
lx.eval('select.all')
lx.eval('cut')
lx.eval('select.type item')
if MergeTransRot == 1 :
    # Merge Rotation Matrix
    lx.eval('smo.GC.MergeTransByArg 1')
if FreezeRot == 1 :
    # Freeze Rotation Matrix
    lx.eval('transform.freeze rotation')
lx.eval('select.type polygon')
lx.eval('paste')
lx.eval('select.type item')



#------------------------------------------------#
# Delete all 3DSMAX related PreRotation Channels #
#------------------------------------------------#

# # Variables
# DelPreTraList = []
# DelPreTraList = lx.eval('query sceneservice selected ? mesh') # mesh item layers
# for mesh in DelPreTraList:



# #------------------------------------------------#
# # Delete all 3DSMAX related PreRotation Channels #
# #------------------------------------------------#

# PrePos = "*PrePosition*"
# PreRot = "*PreRotation*"
# PreSca = "*PreScale*"

# Detected = 0

# # Variables
# DelPreTraList = []
# DelPreTraList = lx.eval('query sceneservice selected ? mesh') # mesh item layers
# for mesh in DelPreTraList:
    # # mesh.select(True)
    # lx.eval('select.type polygon')
    # lx.eval('select.all')
    # lx.eval('cut')
    # lx.eval('select.type item')
    
    
    # # NOT VALID I must find a way to select only the related PreTransform item on the current selected Mesh
    # try:
        # if PreTransform == 0 :
            # lx.eval('selectPattern.pattern %s' % PrePos)
            # Detected = 1
        # if PreTransform == 1 :
            # lx.eval('selectPattern.pattern %s' % PreRot)
            # Detected = 1
        # if PreTransform == 2 :
            # lx.eval('selectPattern.pattern %s' % PreSca)
            # Detected = 1
    # except:
        # pass
    # if Detected == 1 :
        # lx.eval('selectPattern.apply set')
        # lx.eval('!delete')
    # # NOT VALID
    
    
    # lx.eval('select.type polygon')
    # lx.eval('paste')
    # lx.eval('select.type item')
    # lx.eval('select.drop item')