# python
"""
Name:         SMO_MIFABOMA_RADIALSWEEP_TagsProcessFromHighPolyMeshData_Cmd.py

Purpose:      This script is designed to:
              Create tags for MiFaBoMa RadialSweepLocal from Edges.

Author:       Franck ELISABETH
Website:      https://www.smoluck.com
Created:      05/02/2020
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.MIFABOMA.RadialSweep.TagsProcessFromHighPolyMeshData"
# smo.MIFABOMA.RadialSweep.TagsProcessFromHighPolyMeshData 0


class SMO_MIFABOMA_RADIALSWEEP_TagsProcessFromHighPolyMeshData_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Task ID", lx.symbol.sTYPE_INTEGER)
        
    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact (self):
        pass

    def cmd_UserName (self):
        return 'SMO MIFABOMA - Tags Process for Radial Sweep from HighPoly Mesh Data'

    def cmd_Desc (self):
        return 'Create tags for MiFaBoMa RadialSweepLocal from Edges.'

    def cmd_Tooltip (self):
        return 'Create tags for MiFaBoMa RadialSweepLocal from Edges.'

    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName (self):
        return 'SMO MIFABOMA - Tags Process for Radial Sweep from HighPoly Mesh Data'

    def basic_Enable (self, msg):
        return True

    def basic_Execute(self, msg, flags):
    
        scene = modo.Scene()
        # ------------- 5 ARGUMENTS ------------- #
        args = lx.args()
        lx.out(args)

        # Create Tags= 0
        # Delete Tagged Data = 1
        TaskID = self.dyna_Int (0)
        lx.out('Tache:',TaskID)
        # ------------- ARGUMENTS



        ############### COPY/PASTE Check Procedure #################
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
        # -------------------------------------------- #


        
        if TaskID == 0:
            # Tag Treaten Edges and Polygon
            lx.eval('select.editSet EdgesSelSet add')
            lx.eval('select.type polygon')
            lx.eval('cut')
            lx.eval('paste')
            lx.eval('select.editSet RadSwe_ProcessedPolysSelSet add')
            lx.eval('hide.unsel')
            
            lx.eval('select.type edge')
            lx.eval('select.useSet EdgesSelSet replace')
            lx.eval('select.convert vertex')
            lx.eval('select.expand')
            lx.eval('select.convert polygon')
            
            lx.eval('select.editSet RadSwe_PolySelSet add')  
            lx.eval('select.invert')
            lx.eval('select.editSet PolySelSetToDelete add')  
            lx.eval('select.nextMode')
            lx.eval('select.nextMode')
            lx.eval('select.convert vertex')
            lx.eval('select.invert')
            lx.eval('select.editSet RadSwe_VertexSelSetToDelete add')
            lx.eval('select.nextMode')
            lx.eval('select.nextMode')
            lx.eval('select.drop polygon')
            lx.eval('select.type edge')
            
        if TaskID == 1:
            lx.eval('select.type polygon')
            lx.eval('select.drop polygon')
            lx.eval('select.useSet PolySelSetToDelete replace')
            lx.eval('delete')
            lx.eval('!select.deleteSet RadSwe_ProcessedPolysSelSet false')
            lx.eval('!select.deleteSet RadSwe_PolySelSet false')
            lx.eval('select.type vertex')
            lx.eval('delete')
            lx.eval('!select.deleteSet RadSwe_VertexSelSetToDelete false')
            lx.eval('select.type edge')
            lx.eval('!select.deleteSet EdgesSelSet false')
            lx.eval('unhide')



        # -------------- COPY/PASTE END Procedure  -------------- #
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
        # -------------------------------------------- #


lx.bless(SMO_MIFABOMA_RADIALSWEEP_TagsProcessFromHighPolyMeshData_Cmd, Cmd_Name)
