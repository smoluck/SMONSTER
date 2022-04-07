#python
#---------------------------------------
# Name:         SMO_CAD_AllMesh_PolylineToNGon_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to
#               Convert A;; Meshes in scene from Polyline to Polygon NGon. 
#
# Author:       Franck ELISABETH (with the help of Tom Dymond for debug)
# Website:      http://www.smoluck.com
#
# Created:      07/09/2020
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------

import lx, lxu, modo

class SMO_CAD_AllMesh_PolylineToNGon_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
    
    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO CAD All Mesh Polyline To NGon'
    
    def cmd_Desc (self):
        return 'Convert the current Polyline Selection to an NGon.'
    
    def cmd_Tooltip (self):
        return 'Convert the current Polyline Selection to an NGon.'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO CAD All Mesh Polyline To NGon'
    
    def basic_Enable (self, msg):
        return True
    
    
    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()



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



        # lx.out('Start of Polyline To Poly')
        lx.eval('select.itemType mesh')
        meshes_list = scene.selectedByType(lx.symbol.sITYPE_MESH)
        for mesh in meshes_list:
            mesh.select(True)
            lx.eval('select.type edge')
            lx.eval('select.all')
            lx.eval('!poly.make auto')
            lx.eval('select.type polygon')
            lx.eval('select.polygon remove type line 8')
            lx.eval('cut')
            lx.eval('paste')
            lx.eval('select.drop polygon')
            lx.eval('select.type edge')
            lx.eval('select.drop edge')
            lx.eval('select.type polygon')
            # lx.out('End of Polyline To Poly')

            ###############COPY/PASTE END Procedure#################
            # Restore user Preferences:
            if User_Pref_CopyDeselectChangedState == 1:
                lx.eval('pref.value application.copyDeSelection false')
                lx.out('"Deselect Elements after Copying" have been Restored')
            if User_Pref_PasteSelectionChangedState == 1:
                lx.eval('pref.value application.pasteSelection false')
                lx.out('"Select Pasted Elements" have been Restored')
            if User_Pref_PasteDeselectChangedState == 1:
                lx.eval('pref.value application.pasteDeSelection false')
                lx.out('"Deselect Elements Before Pasting" have been Restored')
            ########################################################
            
    def cmd_Query(self, index, vaQuery):
        lx.notimpl()

lx.bless(SMO_CAD_AllMesh_PolylineToNGon_Cmd, "smo.CAD.AllMesh.PolylineToNGon")