# python
"""
Name:         SMO_CB_GetDrawingPackageState_Cmd.py

Purpose:      This script is designed to
              Get the Drawing Package State of the current mesh or Locator. If not present add a Drawing Package.

Author:       Franck ELISABETH (with the help of Tom Dymond)
Website:      https://www.smoluck.com
Created:      12/12/2020
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.CB.GetDrawingPackageState"
# query:        smo.CB.GetDrawingPackageState ?

# ----------- USE CASE
# TestResult = lx.eval('smo.CB.GetDrawingPackageState ?')
# lx.out('Drawing Package state is :',TestResult)
# --------------------


class SMO_CB_GetDrawingPackageState_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Drawing Package State", lx.symbol.sTYPE_BOOLEAN)
        self.basic_SetFlags (0, lx.symbol.fCMDARG_QUERY)
    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO CB - Get Drawing Package State'
    
    def cmd_Desc (self):
        return 'Get the Drawing Package State of the current mesh or Locator. If not present add a Drawing Package.'
    
    def cmd_Tooltip (self):
        return 'Get the Drawing Package State of the current mesh or Locator. If not present add a Drawing Package.'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO CB - Get Drawing Package State'
    
    def basic_Enable (self, msg):
        return True
        
    def cmd_Query(self, index, vaQuery):
        scene = modo.scene.current()
        meshes = scene.selectedByType(lx.symbol.sITYPE_MESH)
        locators = scene.selectedByType(lx.symbol.sITYPE_LOCATOR)
        
        if len(locators) >= 1 :
            for item in locators:
                if item.PackageTest(lx.symbol.sITYPE_GLDRAW):
                    DrawPack = 1
                
                # Test to see if package 'glDraw' is added
                elif not item.PackageTest(lx.symbol.sITYPE_GLDRAW):
                    DrawPack = 0
                    # If not, lets add the package.
                    item.PackageAdd(lx.symbol.sITYPE_GLDRAW)
                
            # print DrawPack
        
        
        elif len(meshes) >= 1 :
            for item in meshes:
                if item.PackageTest(lx.symbol.sITYPE_GLDRAW):
                    DrawPack = 1
                
                # Test to see if package 'glDraw' is added
                elif not item.PackageTest(lx.symbol.sITYPE_GLDRAW):
                    DrawPack = 0
                    # If not, lets add the package.
                    item.PackageAdd(lx.symbol.sITYPE_GLDRAW)
                
            # print DrawPack
                
        # lx.out ('Result of Query:', DrawPack)
        va = lx.object.ValueArray(vaQuery)
        va.AddInt(DrawPack)
        return lx.result.OK
                
    
lx.bless(SMO_CB_GetDrawingPackageState_Cmd, Cmd_Name)
