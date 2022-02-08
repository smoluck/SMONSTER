#python
#---------------------------------------
# Name:         SMO_BAKE_EdgePadding_BSize.py
# Version:      1.0
#
# Purpose:      This script is designed to:
#               Set the Render Frame Size as well as the Edge Padding for bakes.
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      10/09/2020
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------

import modo, lx

scene = modo.Scene()
render_item = scene.item("Render")

# ############### 3 ARGUMENTS ###############
# args = lx.args()
# lx.out(args)
# # Frame Size = 256
# # Frame Size = 512
# # Frame Size = 1024
# # Frame Size = 2048
# # Frame Size = 4096
# FrameSizeX = int(args[0])
# lx.out('Render Frame Size X:',FrameSizeX)
# # Frame Size = 256
# # Frame Size = 512
# # Frame Size = 1024
# # Frame Size = 2048
# # Frame Size = 4096
# FrameSizeY = int(args[1])
# lx.out('Render Frame Size Y:',FrameSizeY)
# # Border Size = 1 px
# # Border Size = 2 px
# # Border Size = 4 px
# # Border Size = 8 px
# # Border Size = 16 px
# # Border Size = 32 px
# BakeBorderPix = int(args[2])
# lx.out('Bake Border Size in pixel:',BakeBorderPX)
# ############### ARGUMENTS ###############


FrameSizeX = lx.eval1 ('user.value SMO_UseVal_BAKE_FrameSizeX ?')
lx.out('Render Frame Size X:',FrameSizeX)
FrameSizeY = lx.eval1 ('user.value SMO_UseVal_BAKE_FrameSizeY ?')
lx.out('Render Frame Size Y:',FrameSizeY)
BakeBorderPix = lx.eval1 ('user.value SMO_UseVal_BAKE_EdgePaddingPix ?')
lx.out('Bake Border Size in pixel:',BakeBorderPix)

x_channel = render_item.channel('bakeX')
x_channel.set(FrameSizeX)
y_channel = render_item.channel('bakeY')
y_channel.set(FrameSizeY)

lx.eval('pref.value render.bakeBorder {%s}' % BakeBorderPix)
