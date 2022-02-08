#python
#---------------------------------------
# Name:         SMO_CLEANUP_ConvertHardEdge_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to:
#               Update Materials Smoothing Angle to 179 Degree according to SMO Modo Workflow,
#               and set ON the Weight by Polygon Area, Process a MeshCleanup pass and a Polygon Align.
#               smo.CLEANUP.ConvertHardEdge 0 1 or 1 1
#
# Author:       Franck ELISABETH (with the help of James O'Hare)
# Website:      http://www.smoluck.com
#
# Created:      17/02/2020
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------

import lx, lxu, modo

class SMO_Cleanup_ConvertHardEdge_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Soften All Edge", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags (0, lx.symbol.fCMDARG_OPTIONAL)				# here the (0) define the argument index.
        self.dyna_Add("Align All Polygons", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags (1, lx.symbol.fCMDARG_OPTIONAL)				# here the (1) define the argument index.
    
    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO Cleanup ConvertHardEdge'
    
    def cmd_Desc (self):
        return 'Update Materials Smoothing Angle to 179 Degree and set ON the Weight by Polygon Area according to SMO Modo Workflow, set ON the Weight by Polygon Area, Process a MeshCleanup pass and a Polygon Align'
    
    def cmd_Tooltip (self):
        return 'Update Materials Smoothing Angle to 179 Degree and set ON the Weight by Polygon Area according to SMO Modo Workflow, set ON the Weight by Polygon Area, Process a MeshCleanup pass and a Polygon Align'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO Cleanup ConvertHardEdge'
    
    def cmd_Flags (self):
        return lx.symbol.fCMD_UNDO
    
    def basic_Enable (self, msg):
        return True
        
    
    def basic_Execute(self, msg, flags):
        scn = modo.Scene()
        IntSoften = self.dyna_Int (0)
        IntAlign = self.dyna_Int (1)
        
        
        # ############### 5 ARGUMENTS ###############
        args = lx.args()
        lx.out(args)
        
        # 0 = Simple Ngon
        # 1 = Radial Triple
        Soften = IntSoften
        lx.out('Soften all Edges:', Soften)
        
        # 0 TriRadial by Polygon Bevel
        # 1 TriRadial by EdgeExtend
        Align = IntAlign
        lx.out('Align all polygons', Align)
        # ############### ARGUMENTS ###############
        
        
        lx.eval('select.drop item')
        lx.eval('select.itemType mesh')
        for mesh in scn.items('mesh'):
            mesh.select(True)
            lx.eval('hardedge.convert true true')
            if Soften == 1 :
                lx.eval('select.type edge')
                lx.eval('hardedge.set soft')
            if Align == 1 :
                lx.eval('select.type polygon')
                lx.eval('!poly.align')
            lx.eval('select.type item')
            lx.eval('!mesh.cleanup true mergeVertex:false')
            
        lx.eval('select.drop item')
        
    
lx.bless(SMO_Cleanup_ConvertHardEdge_Cmd, "smo.CLEANUP.ConvertHardEdge")
