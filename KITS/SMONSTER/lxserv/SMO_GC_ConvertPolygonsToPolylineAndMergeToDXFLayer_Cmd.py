#python
#---------------------------------------
# Name:         SMO_ConvertPolygonsToPolylineAndMergeToDXFLayer_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to:
#               Convert all the current Meshes (Unique Polygons by Layer) in scene
#               to Polyline data and then merge all the lines into a single mesh for DXF export.
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      28/09/2020
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------


import lx, lxu, modo

Cmd_Name = "smo.GC.ConvertPolygonsToPolylineAndMergeToDXFLayer"
# smo.GC.ConvertPolygonsToPolylineAndMergeToDXFLayer 1 1

class SMO_GC_ConvertPolygonsToPolylineAndMergeToDXFLayer_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Freeze Transform PreProcess", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags (0, lx.symbol.fCMDARG_OPTIONAL)
        self.dyna_Add("Merge to New DXF Mesh layer Mode", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags (0, lx.symbol.fCMDARG_OPTIONAL)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact (self):
        pass

    def cmd_UserName (self):
        return 'SMO GC - Convert Polygons to Polyline and Merge to DXF Layer'

    def cmd_Desc (self):
        return 'Convert all the current Meshes (Unique Polygons by Layer) in scene to Polyline data and then merge all the lines into a single mesh for DXF export.'

    def cmd_Tooltip (self):
        return 'Convert all the current Meshes (Unique Polygons by Layer) in scene to Polyline data and then merge all the lines into a single mesh for DXF export.'

    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName (self):
        return 'SMO GC - Convert Polygons to Polyline and Merge to DXF Layer'

    def basic_Enable (self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()
        FreezeTransform = self.dyna_Int (0)
        MergeToNewDXFMeshLayer = self.dyna_Int (1)



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


        
        lx.eval('select.itemType mesh')
        if FreezeTransform == 1 :
            lx.eval('transform.freeze')
        
        meshes_list = scene.selectedByType(lx.symbol.sITYPE_MESH)
        
        # Modollama Triangulation
        #lx.eval('user.value llama_keepuvbounds false')
        #lx.eval('user.value llama_keepmatbounds false')
        
        
        for mesh in meshes_list:
            mesh.select(True)
            lx.eval('select.type edge')
            lx.eval('select.all')
            lx.eval('pmodel.edgeToCurveCMD polyline')
            lx.eval('select.type polygon')
            lx.eval('select.polygon add type line 8')
            lx.eval('select.invert')
            lx.eval('!delete')
            lx.eval('select.type item')
            
            
        if MergeToNewDXFMeshLayer == 1 :
            lx.eval('select.itemType mesh')
            lx.eval('layer.mergeMeshes false')
            lx.eval('select.itemType mesh')
            lx.eval('select.editSet Data add')
            
            lx.eval('layer.new')
            lx.eval('tool.set prim.makeVertex on 0')
            lx.eval('tool.attr prim.makeVertex cenX 0.0')
            lx.eval('tool.attr prim.makeVertex cenY 0.0')
            lx.eval('tool.attr prim.makeVertex cenZ 0.0')
            lx.eval('tool.apply')
            lx.eval('tool.set prim.makeVertex off 0')
            lx.eval('tool.clearTask snap')
            lx.eval('select.editSet Point add')
            
            
            lx.eval('select.drop item')
            lx.eval('select.useSet Data select')
            lx.eval('select.type polygon')
            lx.eval('select.all')
            lx.eval('cut')
            lx.eval('select.drop item')
            
            
            lx.eval('select.type item')
            lx.eval('select.useSet Point select')
            lx.eval('select.type polygon')
            lx.eval('paste')
            lx.eval('select.drop polygon')
            lx.eval('select.type item')
            lx.eval('select.drop item')
            lx.eval('select.useSet Data select')
            lx.eval('!delete')
            lx.eval('!select.deleteSet Point')



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
        

    def cmd_Query(self, index, vaQuery):
        lx.notimpl()


lx.bless(SMO_GC_ConvertPolygonsToPolylineAndMergeToDXFLayer_Cmd, Cmd_Name)
