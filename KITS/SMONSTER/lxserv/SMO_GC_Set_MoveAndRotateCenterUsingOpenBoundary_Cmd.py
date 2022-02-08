#python
#---------------------------------------------
# Name:         SMO_GC_Set_MoveAndRotateCenterUsingOpenBoundary_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to:
#               Select an Opened Mesh Move and Rotate
#               the Center to Open boundary centroid and rotate it (use it in item mode)
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      20/06/2020
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------------


import lx, lxu, modo

class SMO_GC_Set_MoveAndRotateCenterUsingOpenBoundary_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO GC Set Move And Rotate Center Using Open Boundary'
    
    def cmd_Desc (self):
        return 'Select an Opened Mesh Move and Rotate the Center to Open boundary centroid and rotate it (use it in item mode)'
    
    def cmd_Tooltip (self):
        return 'Select an Opened Mesh Move and Rotate the Center to Open boundary centroid and rotate it (use it in item mode)'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO GC Set Move And Rotate Center Using Open Boundary'
    
    def cmd_Flags (self):
        return lx.symbol.fCMD_UNDO
    
    def basic_Enable (self, msg):
        return True
        
    
    def basic_Execute(self, msg, flags):
        scene = modo.Scene()
        mesh_list = scene.selectedByType(lx.symbol.sTYPE_MESH)
        
        SelectedItemsCount = len(lx.evalN('query sceneservice selection ? locator'))
        
        if SelectedItemsCount < 1:
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMO GC Set MoveAndRotateCenterUsingOpenBoundary:}')
            lx.eval('dialog.msg {"You must have at least 1 item selected to run this script.}')
            lx.eval('+dialog.open')
            sys.exit()
        
        meshnum = 0
        
        #deselect items
        lx.eval('select.drop item')
        
        # for r in range(SelectedItemsCount
        
        for mesh in mesh_list:
            mesh.select(True)
            
            
            
            lx.eval('script.run "macro.scriptservice:92663570022:macro"')
            lx.eval('poly.make auto')
            lx.eval('select.convert polygon')
            lx.eval('select.editSet temmmmmp add')
            
            
            
            ###
            ###lx.eval('smo.GC.StarTriple')
            ###
            
            lx.eval('tool.set actr.auto on')
            lx.eval('tool.set poly.bevel on')
            #Command Block Begin: ToolAdjustment
            lx.eval('tool.setAttr poly.bevel shift 0.0')
            lx.eval('tool.setAttr poly.bevel inset 0.005')
            #Command Block End: ToolAdjustment
            lx.eval('tool.doApply')
            lx.eval('tool.drop')
            lx.eval('poly.collapse')
            
            
            
            lx.eval('select.useSet temmmmmp select')
            lx.eval('select.convert vertex')
            lx.eval('select.contract')
            
            
            
            ###
            ###lx.eval('smo.GC.Setup.MoveRotateCenterToSelection 1 0')
            ###
            lx.eval('workPlane.fitSelect')
            lx.eval('select.type item')
            lx.eval('select.convert type:center')
            lx.eval('matchWorkplanePos')
            lx.eval('workPlane.reset')
            lx.eval('select.type polygon')
            
            
            
            lx.eval('select.drop polygon')
            lx.eval('select.useSet temmmmmp select')
            
            
            
            ###
            ###lx.eval('smo.GC.Setup.MoveRotateCenterToSelection 0 1')
            ###
            lx.eval('workPlane.fitSelect')
            lx.eval('select.type item')
            lx.eval('select.convert type:center')
            lx.eval('matchWorkplaneRot')
            lx.eval('workPlane.reset')
            lx.eval('select.type item')
            
            
            
            lx.eval('select.type polygon')
            lx.eval('select.useSet temmmmmp select')
            lx.eval('!delete')
            lx.eval('select.type item')
            
            #deselect items
            lx.eval('select.drop item')
            
            meshnum +=1
        
    
lx.bless(SMO_GC_Set_MoveAndRotateCenterUsingOpenBoundary_Cmd, "smo.GC.Set.MoveAndRotateCenterUsingOpenBoundary")
# smo.GC.Set.MoveAndRotateCenterUsingOpenBoundary