# python
# ---------------------------------------
# Name:         SMO_GC_CreateEmptyChildMeshMatchTransform_Cmd.py.py
# Version:      1.0
#
# Purpose:      This script is designed to:
#               Create a new child Mesh Item (empty) on current selected mesh item.
#
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      20/06/2022
# Copyright:    (c) Franck Elisabeth 2017-2022
# ---------------------------------------

import lx, lxu, modo

Cmd_Name = "smo.GC.CreateEmptyChildMeshMatchTransform"
# smo.GC.CreateEmptyChildMeshMatchTransform true        Select that new child Mesh

class SMO_GC_CreateEmptyChildMatchTransform_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("SelectCopyCutResultMesh Mode", lx.symbol.sTYPE_BOOLEAN)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_OPTIONAL)

        self.SelModePoly = bool(lx.eval1("select.typeFrom typelist:polygon;vertex;edge;item ?"))

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO GC - Create Empty Child Mesh and Match Transforms'

    def cmd_Desc(self):
        return 'Create a new child Mesh Item (empty) on current selected mesh item.'

    def cmd_Tooltip(self):
        return 'Create a new child Mesh Item (empty) on current selected mesh item.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO GC - Create Empty Child Mesh and Match Transforms'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()

        SelectCopyCutResultMesh = bool()
        if self.dyna_IsSet(0):
            SelectCopyCutResultMesh = self.dyna_Bool(0)
        elif self.dyna_Bool(0) == None:
            SelectCopyCutResultMesh = False

        if self.SelModePoly == True:
            lx.eval('smo.MASTER.ForceSelectMeshItemOnly')
        mesh = scene.selectedByType('mesh')[0]


        #####################################################################
        # Store Indice of all Polygons Selected
        # on Current Mesh in order to select them back further in the script.
        # scene = modo.scene.current()
        # mesh = scene.selectedByType('mesh')[0]
        # print(mesh.Ident())
        SelPoly = []
        SelPoly = mesh.geometry.polygons.selected
        # print(SelPoly)

        ##### scene.select(mesh.Ident())
        ##### lx.eval('select.drop polygon')
        ##### mesh.geometry.polygons.select(SelPoly)
        #####################################################################



        # BugFix to preserve the state of the RefSystem (item at origin in viewport)
        # This query only works when an item is selected.
        RefSystemActive = bool()
        CurrentRefSystemItem = lx.eval('item.refSystem ?')
        # print(CurrentRefSystemItem)
        if len(CurrentRefSystemItem) != 0:
            RefSystemActive = True
        else:
            RefSystemActive = False
        # print(RefSystemActive)


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
        #lx.out('User Pref: Deselect Elements after Copying', User_Pref_CopyDeselect)
        User_Pref_PasteSelection = lx.eval('pref.value application.pasteSelection ?')
        #lx.out('User Pref: Select Pasted Elements', User_Pref_PasteSelection)
        User_Pref_PasteDeselect = lx.eval('pref.value application.pasteDeSelection ?')
        #lx.out('User Pref: Deselect Elements Before Pasting', User_Pref_PasteDeselect)
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



        Mesh_Source = scene.selectedByType('mesh')[0]
        Mesh_Source_ID = Mesh_Source.Ident()
        # lx.out('Source Mesh:', Mesh_Source_ID)

        lx.eval('layer.new')

        Mesh_Child = scene.selectedByType('mesh')[0]
        Mesh_Child_ID = Mesh_Child.Ident()
        # lx.out('Child Mesh:', Mesh_Child_ID)
        lx.eval('select.subItem {%s} add mesh 0 0' % Mesh_Source_ID)
        lx.eval('item.parent')
        lx.eval('smo.GC.DeselectAll')

        scene.select(Mesh_Child_ID)
        lx.eval('select.type item')

        if SelectCopyCutResultMesh == False:
            scene.select(Mesh_Source_ID)
        if SelectCopyCutResultMesh == True:
            scene.select(Mesh_Child_ID)



        if RefSystemActive == False:
            lx.eval('item.refSystem {}')
        if RefSystemActive == True:
            lx.eval('item.refSystem %s' % CurrentRefSystemItem)



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


lx.bless(SMO_GC_CreateEmptyChildMatchTransform_Cmd, Cmd_Name)
