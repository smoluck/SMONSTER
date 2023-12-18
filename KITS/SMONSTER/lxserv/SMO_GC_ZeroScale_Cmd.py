# python
"""
Name:         SMO_GC_ZeroScale_Cmd.py

Purpose:      This script is designed to:
              Check Axis Scale value and modify the lowest scale to ZERO.

Author:       Franck ELISABETH
Website:      https://www.linkedin.com/in/smoluck/
Created:      13/01/2020
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu

Cmd_Name ="smo.GC.ZeroScale"
# smo.GC.ZeroScale


class SMO_GC_ZeroScale_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        # self.dyna_Add("IntBuildMode", lx.symbol.sTYPE_INTEGER)
        # self.basic_SetFlags (0, lx.symbol.fCMDARG_OPTIONAL)				# here the (0) define the argument index.
        # self.dyna_Add("IntTriRadial_Mode", lx.symbol.sTYPE_INTEGER)
        # self.basic_SetFlags (1, lx.symbol.fCMDARG_OPTIONAL)				# here the (1) define the argument index.
        # self.dyna_Add("IntUser_Mode", lx.symbol.sTYPE_INTEGER)
        # self.basic_SetFlags (2, lx.symbol.fCMDARG_OPTIONAL)				# here the (1) define the argument index.
        # self.dyna_Add("IntSideCount", lx.symbol.sTYPE_INTEGER)
        # self.basic_SetFlags (3, lx.symbol.fCMDARG_OPTIONAL)				# here the (1) define the argument index.
    
    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO GC - Zero Out Lowest Scale'
    
    def cmd_Desc (self):
        return 'Check Axis Scale value and modify the lowest scale to ZERO.'
    
    def cmd_Tooltip (self):
        return 'Check Axis Scale value and modify the lowest scale to ZERO.'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO GC - Zero Out Lowest Scale'
    
    def basic_Enable (self, msg):
        return True
    
    def basic_Execute(self, msg, flags):
            ToolScaleState = lx.eval('tool.set TransformScale ?')
            #lx.out('Tool Scale state:', ToolScaleState)

            lx.eval('tool.set TransformScale on')
            lx.eval('tool.noChange')
            
            if ToolScaleState:
                ToolScaleX = lx.eval('tool.attr xfrm.transform SX ?')
                lx.out('Tool Scale, Value on X:', ToolScaleX)
                
                ToolScaleY = lx.eval('tool.attr xfrm.transform SY ?')
                lx.out('Tool Scale, Value on Y:', ToolScaleY)
                
                ToolScaleZ = lx.eval('tool.attr xfrm.transform SZ ?')
                lx.out('Tool Scale, Value on Z:', ToolScaleZ)
                
                
                
                if ToolScaleX < ToolScaleY and ToolScaleX < ToolScaleZ:
                    TSclXMin = 1
                    TSclYMin = 0
                    TSclZMin = 0
                    
                if ToolScaleY < ToolScaleX and ToolScaleY < ToolScaleZ:
                    TSclXMin = 0
                    TSclYMin = 1
                    TSclZMin = 0
                    
                if ToolScaleZ < ToolScaleX and ToolScaleZ < ToolScaleY:
                    TSclXMin = 0
                    TSclYMin = 0
                    TSclZMin = 1
                    
                if TSclXMin == 1:
                    lx.eval('tool.setAttr xfrm.transform SX 0')
                if TSclYMin == 1:
                    lx.eval('tool.setAttr xfrm.transform SY 0')
                if TSclZMin == 1:
                    lx.eval('tool.setAttr xfrm.transform SZ 0')
                
                lx.eval('tool.doApply')
                
            
            lx.out('End of SMO_RebuildCurve Script')
            lx.out('-------------------------------')
            
    
    def cmd_Query(self, index, vaQuery):
        lx.notimpl()
    
    
lx.bless(SMO_GC_ZeroScale_Cmd, Cmd_Name)
