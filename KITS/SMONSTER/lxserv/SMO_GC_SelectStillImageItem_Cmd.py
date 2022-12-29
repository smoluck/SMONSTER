# python
"""
Name:         SMO_GC_SelectStillImageItem_Cmd.py

Purpose:      This script is designed to
              Create a still images (clips) Item of the current scene.

Author:       Franck ELISABETH (with the help of Tom Dymond)
Website:      https://www.smoluck.com
Created:      12/08/2020
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.GC.SelectStillImageItem"
# execute:      smo.GC.SelectStillImageItem
# query:        smo.GC.SelectStillImageItem ?

# ------ USE CASE
# TestResult = lx.eval('smo.GC.SelectStillImageItem ?')
# lx.out('Still image item Identity name is :',TestResult)
# ---------------


class SMO_GC_SelectStillImageItem_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Still Image Item Name", lx.symbol.sTYPE_STRING)
        self.basic_SetFlags (0, lx.symbol.fCMDARG_QUERY)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO GC - Select Still Image Item'
    
    def cmd_Desc (self):
        return 'Select the still images (clips) Item of the current scene.'
    
    def cmd_Tooltip (self):
        return 'Select the still images (clips) Item of the current scene.'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO GC - Select Still Image Item'
    
    def basic_Enable (self, msg):
        return True
    
    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()
        
        # clear selection of any item in the scene.
        # lx.eval('select.clear item')
        # lx.eval('select.drop schmNode')
        # lx.eval('select.drop channel')
        # lx.eval('select.drop link')
        
        # Get the item count
        n = lx.eval1( 'query sceneservice item.N ?' )
        
        # Loop through the items in the scene, looking for output items
        for i in range(n):
            itemtype = lx.eval( 'query sceneservice item.type ? %s' % i )
            if itemtype == "videoStill":
                StillImageItemID = lx.eval( 'query sceneservice item.id ?')
                # lx.out( 'StillImage Item ID:', StillImageItemID )
                # lx.eval ('!!user.value Smo_StillImageItemName {%s}' % StillImageItemID)
        
        lx.eval('texture.new clip:{%s:videoStill001}' % StillImageItemID)


    def cmd_Query(self, index, vaQuery):
        scene = modo.scene.current()
        
        # clear selection of any item in the scene.
        # lx.eval('select.clear item')
        # lx.eval('select.drop schmNode')
        # lx.eval('select.drop channel')
        # lx.eval('select.drop link')
        
        # Get the item count
        n = lx.eval1( 'query sceneservice item.N ?' )
        
        for i in range(n):
            itemtype = lx.eval( 'query sceneservice item.type ? %s' % i )
            if itemtype == "videoStill":
                StillImageItemID = lx.eval( 'query sceneservice item.id ?')
                # lx.out( 'StillImage Item ID:', StillImageItemID )
                # lx.eval ('!!user.value Smo_StillImageItemName {%s}' % StillImageItemID)
                
                lx.out ('Result of Query:', StillImageItemID)
                va = lx.object.ValueArray(vaQuery)
                va.AddString(StillImageItemID)
                return lx.result.OK
                

lx.bless(SMO_GC_SelectStillImageItem_Cmd, Cmd_Name)
