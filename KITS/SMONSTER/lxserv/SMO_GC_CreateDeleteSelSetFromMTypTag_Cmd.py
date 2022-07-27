#python
#---------------------------------------
# Name:         SMO_GC_CreateDeleteSelSetFromMTypTag_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to:
#               Read current defined Tags for Livelink Exports.
#               Then Create OR Delete the Selection Set related to that tag for LowPoly / Cage / HighPoly.
#
#
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      30/11/2020
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------

import lx, lxu, modo

Cmd_Name = "smo.GC.CreateDeleteSelSetFromMTypTag"
# smo.GC.CreateDeleteSelSetFromMTypTag 1 ------ > Detect if MTyp Tags exist. Then Create the Selection Set related to that tag for LowPoly / Cage / HighPoly.
# smo.GC.CreateDeleteSelSetFromMTypTag 0 ------ > Delete the Selection Set related to that tag for LowPoly / Cage / HighPoly.

class SMO_GC_CreateDeleteSelSetFromMTypTag_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Action Method from Tags", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags (0, lx.symbol.fCMDARG_OPTIONAL)             # here the (0) define the argument index.
        # self.dyna_Add("Initial Projection", lx.symbol.sTYPE_INTEGER)
        # self.basic_SetFlags (1, lx.symbol.fCMDARG_OPTIONAL)
        
    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO GC - Create or Delete SelSet from Bake Mesh Type Tag'
    
    def cmd_Desc (self):
        return 'Read current defined Tags for Livelink Exports, then Create OR Delete the Selection Set related to that tag for LowPoly / Cage / HighPoly.'
    
    def cmd_Tooltip (self):
        return 'Read current defined Tags for Livelink Exports, then Create OR Delete the Selection Set related to that tag for LowPoly / Cage / HighPoly.'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO GC - Create or Delete SelSet from Bake Mesh Type Tag'
    
    def basic_Enable (self, msg):
        return True
    
    def basic_Execute(self, msg, flags):
        # if not self.dyna_IsSet(0):
            # return False
        scene = modo.Scene()
        
        ActionMethodOnTag = self.dyna_Int (0)
        
        ################################
        #<----[ DEFINE VARIABLES ]---->#
        ################################
        lx.eval("user.defNew name:itemUniqueName type:string life:momentary")
        lx.eval("user.defNew name:MtypeTagValue type:string life:momentary")
        lx.eval("user.defNew name:TagDetected type:boolean life:momentary")
        lx.eval("user.defNew name:TagDetectedCount type:integer life:momentary")
        ################################
        
        TagDetectedCount = 0
        
        
        if ActionMethodOnTag == 1 :
            
            lx.eval('select.itemType mesh')
            # Variables
            DetectTagMeshList = list(scene.selectedByType("mesh")) # mesh item layers
            itemUniqueName = (lx.eval('query sceneservice selection ? mesh'))
            # lx.out('In Selected items, List of their Unique Name is:',itemUniqueName)
            for mesh in DetectTagMeshList:
                mesh.select(True)
                itemName = (lx.eval('query sceneservice selection ? locator'))
                # lx.out('In Selected items, List of their Unique Name is:',itemName)
                
                
                try:
                    # MtypeTagValue = lx.eval('smo.GC.ReadTag item:%s tagName:MTyp tagValue:?' % itemUniqueName)
                    MtypeTagValue = lx.eval('smo.GC.ReadTag %s MTyp ?' % itemName)
                    # lx.out('tags:',MtypeTagValue)
                    TagDetected = True
                except :
                    TagDetected = False
                
                if TagDetected == True :
                    if MtypeTagValue == "LowPoly" :
                        lx.eval('select.editSet MTyp_LowPoly add')
                        
                    if MtypeTagValue == "Cage" :
                        lx.eval('select.editSet MTyp_Cage add')
                        
                    if MtypeTagValue == "HighPoly" :
                        lx.eval('select.editSet MTyp_HighPoly add')
        
        
        
        
        
        if ActionMethodOnTag == 0 :
            
            lx.eval('select.itemType mesh')
            # Variables
            DetectTagMeshList = list(scene.selectedByType("mesh")) # mesh item layers
            itemUniqueName = (lx.eval('query sceneservice selection ? mesh'))
            # lx.out('In Selected items, List of their Unique Name is:',itemUniqueName)
            for mesh in DetectTagMeshList:
                mesh.select(True)
                itemName = (lx.eval('query sceneservice selection ? locator'))
                # lx.out('In Selected items, List of their Unique Name is:',itemName)
                
                
                try:
                    # MtypeTagValue = lx.eval('smo.GC.ReadTag item:%s tagName:MTyp tagValue:?' % itemUniqueName)
                    MtypeTagValue = lx.eval('smo.GC.ReadTag %s MTyp ?' % itemName)
                    # lx.out('tags:',MtypeTagValue)
                    TagDetectedCount = TagDetectedCount + 1
                    # lx.out('tags:',MtypeTagValue)
                    # if MtypeTagValue == "LowPoly"
                        # TagDetected_LowPoly = True
                    # if MtypeTagValue == "Cage"
                        # TagDetected_Cage = True
                    # if MtypeTagValue == "HighPoly"
                        # TagDetected_Cage = True
                except :
                    TagDetected = TagDetectedCount
                    
            # lx.out('In Selected items, List of their Unique Name is:',TagDetectedCount)
            
            # lx.out('DetectedSelSet:',TagDetectedCount)
            if TagDetectedCount > 1 :
                try :
                    lx.eval('!select.deleteSet MTyp_LowPoly')
                except :
                    pass
                
                try :
                    lx.eval('!select.deleteSet MTyp_Cage')
                except :
                    pass
                
                try :
                    lx.eval('!select.deleteSet MTyp_HighPoly')
                except :
                    pass
                
        lx.eval('select.drop item')
            
    
    def cmd_Query(self, index, vaQuery):
        lx.notimpl()


lx.bless(SMO_GC_CreateDeleteSelSetFromMTypTag_Cmd, Cmd_Name)
