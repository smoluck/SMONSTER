# python
"""
# Name:         SMO_GC_MergeTransByArg_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to:
#               Merge the multiple Pos/Rot/Sca Transform into only one Transform Matrix.
#               via String Argument to define wich Transform to update: POSition / ROTation / SCAle
#               Select the Mesh item and launch it.
#
# Author:       Franck ELISABETH (with the help of James O'Hare)
# Website:      https://www.smoluck.com
#
# Created:      03/03/2020
# Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.GC.MergeTransByArg"
# smo.GC.MergeTransByArg 1


class SMO_GC_MergeTransByArg_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Mode", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags (0, lx.symbol.fCMDARG_OPTIONAL)             # here the (0) define the argument index.
    
    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO GC - Merge Transforms by Arguments'
    
    def cmd_Desc (self):
        return 'Merge the multiple Pos/Rot/Sca Transform into only one Transform Matrix via String Argument to define wich Transform to update: POSition / ROTation / SCAle.'
    
    def cmd_Tooltip (self):
        return 'Merge the multiple Pos/Rot/Sca Transform into only one Transform Matrix via String Argument to define wich Transform to update: POSition / ROTation / SCAle.'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO GC - Merge Transforms by Arguments'
    
    def basic_Enable (self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scene = modo.Scene()
        scn = scene.selected[0]
        locsup = modo.LocatorSuperType(scn)
        pos = locsup.position
        rot = locsup.rotation
        sca = locsup.scale
        
        # # ------------- ARGUMENTS Test
        TransMode = self.dyna_Int (0)
        # Searched = "UVChannel_1"
        # OutputName = "TargetUVMap"
        # # ------------- ARGUMENTS ------------- #
        # args = lx.args()
        # lx.out(args)
        
        # PreTransform = int(args[0])
        # lx.out('PreTransform search type:', PreTransform)
        # # ------------- ARGUMENTS ------------- #
        
        
        if TransMode == 0 :
            transformsStackPos = [xfrm for xfrm in locsup.transforms]
            transformsStackPos.reverse()
            
            for n, xfrm in enumerate(transformsStackPos):
                print(xfrm.name)
                if xfrm == pos :
                    if transformsStackPos[n + 1].type == 'position':
                        scene.select([transformsStackPos[n + 1], xfrm])
                        lx.eval('transform.merge rem:1')
                        break
        
        
        elif TransMode == 1 :
            transformsStackRot = [xfrm for xfrm in locsup.transforms]
            transformsStackRot.reverse()
                
            for n, xfrm in enumerate(transformsStackRot):
                print(xfrm.name)
                if xfrm == rot :
                    if transformsStackRot[n + 1].type == 'rotation':
                        scene.select([transformsStackRot[n + 1], xfrm])
                        lx.eval('transform.merge rem:1')
                        break
        
        
        elif TransMode == 2 :
            transformsStackSca = [xfrm for xfrm in locsup.transforms]
            transformsStackSca.reverse()
                
            for n, xfrm in enumerate(transformsStackSca):
                print(xfrm.name)
                if xfrm == sca :
                    if transformsStackSca[n + 1].type == 'scale':
                        scene.select([transformsStackSca[n + 1], xfrm])
                        lx.eval('transform.merge rem:1')
                        break


lx.bless(SMO_GC_MergeTransByArg_Cmd, Cmd_Name)
