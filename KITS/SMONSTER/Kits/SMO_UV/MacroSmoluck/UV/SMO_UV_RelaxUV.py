# python
"""
# Name:         SMO_UV_RelaxUV.py
# Version: 1.0
#
# Purpose: This script is designed to
# Relax the UV's of the current Polygon Selection
#
# Author:       Franck ELISABETH
# Website:      https://www.smoluck.com
#
# Created:      10/10/2019
# Copyright:    (c) Franck Elisabeth 2017-2022
"""

import modo
import lx

# ------------- ARGUMENTS ------------- #
args = lx.args()
lx.out(args)

# Conformal= 0
# Angle Based = 1
RelaxUV_Iter = int(args[0])
lx.out('Relax UV iteration Count: %s' % RelaxUV_Iter)
# ------------- ARGUMENTS ------------- #

##### UV SEAM Map Detection #####
# MODO version checks.
# Modo 13.0 and up have UV Seam map.
# Version below 13.0 haven't
Modo_ver = int(lx.eval ('query platformservice appversion ?'))
lx.out('Modo Version:',Modo_ver)
##### UV SEAM Map Detection #####

#Define the vmap name Search case.
lx.eval("user.defNew name:UVConstraints type:string life:momentary")
lx.eval("user.defNew name:ReplaceUVSeamFailed type:string life:momentary")
ReplaceUVSeamFailed = 0
UVConstraints = 'UV Constraints'

lx.eval('tool.set uv.relax on')
lx.eval('tool.noChange')

lx.eval('tool.attr uv.relax mode lscm')
lx.eval('tool.attr uv.relax live false')
# lx.eval('tool.attr uv.relax live true')
lx.eval('tool.attr uv.relax iter %s' % RelaxUV_Iter)
lx.eval('tool.attr uv.relax boundary smooth')

lx.eval('tool.doApply')
lx.eval('select.nextMode')
# lx.eval('!vertMap.deleteByName pick "UV Constraints"')




# Get the number of UV Seam map available on mesh
DetectedVMapPickCount = len(lx.evalN('vertMap.list pick ?'))
lx.out('Vmap Pick Count:', DetectedVMapPickCount)
# Get the name of UV Seam map available on mesh
DetectedVMapPickName = lx.eval('vertMap.list pick ?')
lx.out('Vmap Pick Name:', DetectedVMapPickName)
##### UV SEAM Map Detection #####
## UV Constraint Map Selection Check To bugfix the UV Constraint VMap creation ##
lx.out('<--- UV Constraint Map Safety Check --->')
lx.out('<---------- START ---------->')
if Modo_ver <= 1399 :
    if DetectedVMapPickCount >= 1 and DetectedVMapPickName == UVConstraints :
        lx.out('UV Constraints junk map detected')
        lx.eval('!vertMap.deleteByName pick "UV Constraints"')
        if Modo_ver >= 1300:
            try:
                lx.eval('!select.vertexMap "UV Seam" seam replace')
            except:
                ReplaceUVSeamFailed = 1
                # lx.out('UV Seam map NOT detected')
            if ReplaceUVSeamFailed == 1 :
                lx.eval('@{kit_SMO_UV:MacroSmoluck/UV/SMO_UV_Update_UVSeamCutMap.py}')
                lx.eval('select.type polygon')
    elif DetectedVMapPickCount <= 0 and DetectedVMapPickName != UVConstraints :
        lx.out('UV Constraints junk map NOT detected')