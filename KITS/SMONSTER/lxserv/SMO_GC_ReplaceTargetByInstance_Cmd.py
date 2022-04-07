#python
#----------------------------------------------------
# Name:         SMO_GC_ReplaceTargetByInstance_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to:
#               Delete all 3DSMAX related Channels created
#               at FBX Export in the current scene.
#
# Author:       Franck ELISABETH (based on William Vaughan Script)
# Website:      http://www.smoluck.com
#
# Created:      19/06/2020
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------------


import lx, lxu, modo

class SMO_GC_ReplaceTargetByInstance_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Item Type", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags (0, lx.symbol.fCMDARG_OPTIONAL)             # here the (0) define the argument index.
    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO GC Replace By Instance'
    
    def cmd_Desc (self):
        return 'Select the target then the source Mesh Item.'
    
    def cmd_Tooltip (self):
        return 'Select the target then the source Mesh Item.'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO GC Replace By Instance'
    
    def basic_Enable (self, msg):
        return True
        
    
    def basic_Execute(self, msg, flags):
        ItemType = self.dyna_Int (0)
        if ItemType == 0 :
            lx.out('Regular Clone Mode')
        elif ItemType == 1 :
            lx.out('Instance Clone Mode')
        
        
        SelectedItemsCount = len(lx.evalN("query sceneservice selection ? locator"))
        
        if SelectedItemsCount < 2:
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {Replace Target By Instance:}')
            lx.eval('dialog.msg {"You must have at least 2 items selected to run this script.}')
            lx.eval('+dialog.open')
            sys.exit()
        
        SelectedItemsCount = (SelectedItemsCount -1)
        lx.out('Selected Target Count:',SelectedItemsCount)
        
        selMeshes = lx.eval('query sceneservice selection ? mesh')
        lx.out('selMeshes',selMeshes)
        
        sourceMesh = selMeshes[-1]
        lx.out(sourceMesh)
        
        meshnum = 0
        
        #deselect items
        lx.eval('select.drop item')
        
        for r in range(SelectedItemsCount):
            lx.eval('select.item {%s} set' %selMeshes[meshnum])
            m = lx.eval('query sceneservice selection ? mesh')
            
            #Get item Position, Scale and Rotation
            mPos = lx.eval('query sceneservice item.Pos ? %s' % m)      #Queries the current item XYZ position
            mRot = lx.eval('query sceneservice item.Rot ? %s' % m)      #Queries the current item Rotation XYZ value
            mScl = lx.eval('query sceneservice item.Scale ? %s' % m)    #Queries the current item Scale XYZ value
            lx.out(mPos)
            lx.out(mRot)
            lx.out(mScl)
            
            mRotX = ((mRot[0] *180) /3.14)
            mRotY = ((mRot[1] *180) /3.14)
            mRotZ = ((mRot[2] *180) /3.14)
            
            #delete
            lx.eval('!delete')
            
            lx.eval('select.item {%s} set' %sourceMesh)
            if ItemType == 0 :
                lx.eval('item.duplicate')
            elif ItemType == 1 :
                lx.eval('item.duplicate true locator false true')
            
            #Move the new item
            lx.eval('transform.channel pos.X %s'%mPos[0])
            lx.eval('transform.channel pos.Y %s'%mPos[1])
            lx.eval('transform.channel pos.Z %s'%mPos[2])
            lx.eval('tool.doApply')
            
            #Rotate the new item
            lx.eval('transform.channel rot.X %s'%mRotX)
            lx.eval('transform.channel rot.Y %s'%mRotY)
            lx.eval('transform.channel rot.Z %s'%mRotZ)
            
            
            #Scale the new item
            lx.eval('transform.channel scl.X %s'%mScl[0])
            lx.eval('transform.channel scl.Y %s'%mScl[1])
            lx.eval('transform.channel scl.Z %s'%mScl[2])
            
            
            #deselect items
            lx.eval('select.drop item')
            
            meshnum +=1
        
    
lx.bless(SMO_GC_ReplaceTargetByInstance_Cmd, "smo.GC.ReplaceTargetByInstance")
# smo.GC.ReplaceTargetByInstance 1 # copy in instance mode