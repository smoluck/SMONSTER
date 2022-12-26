# python
"""
# Name:         SMO_CLEANUP_DelPreTransform_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to:
#               Delete all 3DSMAX related PreTransform Channels created at
#               FBX Export in the current scene. Position / Rotation / Scale
#
# Author:       Franck ELISABETH
# Website:      https://www.smoluck.com
#
# Created:      03/03/2020
# Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.CLEANUP.DelPreTransform"


class SMO_Cleanup_DelPreTransform_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Merge Transform Rotation", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags (0, lx.symbol.fCMDARG_OPTIONAL)				# here the (0) define the argument index.
        self.dyna_Add("Freeze Rotation", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags (1, lx.symbol.fCMDARG_OPTIONAL)				# here the (1) define the argument index.

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO CLEANUP - Delete PreTransforms'
    
    def cmd_Desc (self):
        return 'Delete all PreTransform Rotation Channels.'
    
    def cmd_Tooltip (self):
        return 'Delete all PreTransform Rotation Channels.'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO CLEANUP - Delete PreTransforms'
    
    def basic_Enable (self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()
        IntMergeTransRot = self.dyna_Int (0)
        IntFreezeRot = self.dyna_Int (1)
        
        # # ------------- ARGUMENTS Test
        # PreTransform = 1
        # FreezeRot = 1
        # # ------------- ARGUMENTS ------------- #
        args = lx.args()
        lx.out(args)



        ###############COPY/PASTE Check Procedure#################
        ## create variables
        lx.eval("user.defNew name:User_Pref_CopyDeselectChangedState type:boolean life:momentary")
        lx.eval("user.defNew name:User_Pref_PasteSelectionChangedState type:boolean life:momentary")
        lx.eval("user.defNew name:User_Pref_PasteDeselectChangedState type:boolean life:momentary")

        lx.eval("user.defNew name:User_Pref_CopyDeselect type:boolean life:momentary")
        lx.eval("user.defNew name:User_Pref_PasteSelection type:boolean life:momentary")
        lx.eval("user.defNew name:User_Pref_PasteDeselect type:boolean life:momentary")
        ###################

        # Look at current Copy / Paste user Preferences:
        User_Pref_CopyDeselect = lx.eval('pref.value application.copyDeSelection ?')
        lx.out('User Pref: Deselect Elements after Copying', User_Pref_CopyDeselect)
        User_Pref_PasteSelection = lx.eval('pref.value application.pasteSelection ?')
        lx.out('User Pref: Select Pasted Elements', User_Pref_PasteSelection)
        User_Pref_PasteDeselect = lx.eval('pref.value application.pasteDeSelection ?')
        lx.out('User Pref: Deselect Elements Before Pasting', User_Pref_PasteDeselect)
        # Is Copy Deselect False ?
        if User_Pref_CopyDeselect == 0:
            lx.eval('pref.value application.copyDeSelection true')
            User_Pref_CopyDeselectChangedState = 1

        # Is Paste Selection False ?
        if User_Pref_PasteSelection == 0:
            lx.eval('pref.value application.pasteSelection true')
            User_Pref_PasteSelectionChangedState = 1

        # Is Paste Deselect False ?
        if User_Pref_PasteDeselect == 0:
            lx.eval('pref.value application.pasteDeSelection true')
            User_Pref_PasteDeselectChangedState = 1

        # Is Copy Deselect True ?
        if User_Pref_CopyDeselect == 1:
            User_Pref_CopyDeselectChangedState = 0

        # Is Paste Selection True ?
        if User_Pref_PasteSelection == 1:
            User_Pref_PasteSelectionChangedState = 0

        # Is Paste Deselect True ?
        if User_Pref_PasteDeselect == 1:
            User_Pref_PasteDeselectChangedState = 0
        ################################################


        
        MergeTransRot = IntMergeTransRot
        lx.out('Merge Transform Rotation:', MergeTransRot)
        
        FreezeRot = IntFreezeRot
        lx.out('Freeze Rotation:', FreezeRot)
        # # ------------- ARGUMENTS ------------- #
        
        lx.eval('select.drop item')
        lx.eval('select.itemType mesh')
        mesh_list = scene.selectedByType(lx.symbol.sTYPE_MESH)
        for mesh in mesh_list:
            mesh.select(True)
            lx.eval('select.type polygon')
            lx.eval('select.all')
            lx.eval('cut')
            lx.eval('select.type item')
            if MergeTransRot == 1 :
                # Merge Rotation Matrix
                lx.eval('smo.GC.MergeTransByArg 1')
            if FreezeRot == 1 :
                # Freeze Rotation Matrix
                lx.eval('transform.freeze rotation')
            lx.eval('select.type polygon')
            lx.eval('paste')
            lx.eval('select.type item')
        lx.eval('select.drop item')

        ###############COPY/PASTE END Procedure#################
        # Restore user Preferences:
        if User_Pref_CopyDeselectChangedState == 1 :
            lx.eval('pref.value application.copyDeSelection false')
            lx.out('"Deselect Elements after Copying" have been Restored')
        if User_Pref_PasteSelectionChangedState == 1 :
            lx.eval('pref.value application.pasteSelection false')
            lx.out('"Select Pasted Elements" have been Restored')
        if User_Pref_PasteDeselectChangedState == 1 :
            lx.eval('pref.value application.pasteDeSelection false')
            lx.out('"Deselect Elements Before Pasting" have been Restored')
        ########################################################
        
    
lx.bless(SMO_Cleanup_DelPreTransform_Cmd, Cmd_Name)


#------------------------------------------------#
# Delete all 3DSMAX related PreRotation Channels #
#------------------------------------------------#

# # Variables
# DelPreTraList = []
# DelPreTraList = lx.eval('query sceneservice selected ? mesh') # mesh item layers
# for mesh in DelPreTraList:



# #------------------------------------------------#
# # Delete all 3DSMAX related PreRotation Channels #
# #------------------------------------------------#

# PrePos = "*PrePosition*"
# PreRot = "*PreRotation*"
# PreSca = "*PreScale*"

# Detected = 0

# # Variables
# DelPreTraList = []
# DelPreTraList = lx.eval('query sceneservice selected ? mesh') # mesh item layers
# for mesh in DelPreTraList:
    # # mesh.select(True)
    # lx.eval('select.type polygon')
    # lx.eval('select.all')
    # lx.eval('cut')
    # lx.eval('select.type item')
    
    
    # # NOT VALID I must find a way to select only the related PreTransform item on the current selected Mesh
    # try:
        # if PreTransform == 0 :
            # lx.eval('selectPattern.pattern %s' % PrePos)
            # Detected = 1
        # if PreTransform == 1 :
            # lx.eval('selectPattern.pattern %s' % PreRot)
            # Detected = 1
        # if PreTransform == 2 :
            # lx.eval('selectPattern.pattern %s' % PreSca)
            # Detected = 1
    # except:
        # pass
    # if Detected == 1 :
        # lx.eval('selectPattern.apply set')
        # lx.eval('!delete')
    # # NOT VALID
    
    
    # lx.eval('select.type polygon')
    # lx.eval('paste')
    # lx.eval('select.type item')
    # lx.eval('select.drop item')