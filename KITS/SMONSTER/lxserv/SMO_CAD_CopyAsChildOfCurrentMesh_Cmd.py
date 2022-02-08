# python
# ---------------------------------------
# Name:         SMO_CAD_CopyAsChildOfCurrentMesh_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to:
#               Copy selected Polygons to a new mesh as a child of the current mesh item.
#
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      07/05/2021
# Copyright:    (c) Franck Elisabeth 2017-2022
# ---------------------------------------

import lx, lxu, modo

Command_Name = "smo.CAD.CopyCutAsChildOfCurrentMesh"
# 4th Argument set to "True" will select resulting mesh instead of source
# smo.CAD.CopyCutAsChildOfCurrentMesh 0 1 1 true        Copy Polygon Similar Touching -- To Visible Mesh - And Select that new Mesh

# smo.CAD.CopyCutAsChildOfCurrentMesh 0 1          Copy Polygon Selection -- To Visible Mesh
# smo.CAD.CopyCutAsChildOfCurrentMesh 0 1 1        Copy Polygon Similar Touching -- To Visible Mesh
# smo.CAD.CopyCutAsChildOfCurrentMesh 0 1 2        Copy Polygon Similar Object -- To Visible Mesh
# smo.CAD.CopyCutAsChildOfCurrentMesh 0 1 3        Copy Polygon Similar on Layer -- To Visible Mesh
# smo.CAD.CopyCutAsChildOfCurrentMesh 0 1 4        Copy Connected Polygons -- To Visible Mesh

# smo.CAD.CopyCutAsChildOfCurrentMesh 1 1          Cut Polygon Selection -- To Visible Mesh
# smo.CAD.CopyCutAsChildOfCurrentMesh 1 1 1        Cut Polygon Similar Touching -- To Visible Mesh
# smo.CAD.CopyCutAsChildOfCurrentMesh 1 1 2        Cut Polygon Similar Object -- To Visible Mesh
# smo.CAD.CopyCutAsChildOfCurrentMesh 1 1 3        Cut Polygon Similar on Layer -- To Visible Mesh
# smo.CAD.CopyCutAsChildOfCurrentMesh 1 1 4        Cut Connected Polygons -- To Visible Mesh

# smo.CAD.CopyCutAsChildOfCurrentMesh 0 0          Copy Polygon Selection -- To Invisible Mesh
# smo.CAD.CopyCutAsChildOfCurrentMesh 0 0 1        Copy Polygon Similar Touching -- To Invisible Mesh
# smo.CAD.CopyCutAsChildOfCurrentMesh 0 0 2        Copy Polygon Similar Object -- To Invisible Mesh
# smo.CAD.CopyCutAsChildOfCurrentMesh 0 0 3        Copy Polygon Similar on Layer -- To Invisible Mesh
# smo.CAD.CopyCutAsChildOfCurrentMesh 0 0 4        Copy Connected Polygons -- To Invisible Mesh

# smo.CAD.CopyCutAsChildOfCurrentMesh 1 0          Cut Polygon Selection -- To Invisible Mesh
# smo.CAD.CopyCutAsChildOfCurrentMesh 1 0 1        Cut Polygon Similar Touching -- To Invisible Mesh
# smo.CAD.CopyCutAsChildOfCurrentMesh 1 0 2        Cut Polygon Similar Object -- To Invisible Mesh
# smo.CAD.CopyCutAsChildOfCurrentMesh 1 0 3        Cut Polygon Similar on Layer -- To Invisible Mesh
# smo.CAD.CopyCutAsChildOfCurrentMesh 1 0 4        Cut Connected Polygons -- To Invisible Mesh

class SMO_CAD_CopyCutAsChildOfCurrentMesh_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Cut Mode", lx.symbol.sTYPE_BOOLEAN)
        self.dyna_Add("Visibility Mode", lx.symbol.sTYPE_BOOLEAN)
        self.dyna_Add("Coplanar Mode / Connected Mode", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags(2, lx.symbol.fCMDARG_OPTIONAL)
        self.dyna_Add("SelectCopyCutResultMesh Mode", lx.symbol.sTYPE_BOOLEAN)
        self.basic_SetFlags(3, lx.symbol.fCMDARG_OPTIONAL)

        self.SelModePoly = bool(lx.eval1("select.typeFrom typelist:polygon;vertex;edge;item ?"))

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO CAD CopyAsChildOfCurrentMesh'

    def cmd_Desc(self):
        return 'Copy selected Polygons to a new mesh as a child of the current mesh item.'

    def cmd_Tooltip(self):
        return 'Copy selected Polygons to a new mesh as a child of the current mesh item.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO CAD CopyAsChildOfCurrentMesh'

    def cmd_Flags(self):
        return lx.symbol.fCMD_UNDO

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()
        if self.dyna_IsSet(0):
            CopyOrCut = self.dyna_Bool(0)
            lx.out('Cut Mode:', CopyOrCut)
        if self.dyna_IsSet(1):
            VisibleMode = self.dyna_Bool(1)
            lx.out('Visibility Mode:', VisibleMode)
        if self.dyna_IsSet(2):
            CoplanarConnectedMode = self.dyna_Int(2)
            lx.out('Coplanar Mode / Connected Mode:', CoplanarConnectedMode)
            # 0/None    Cut Polygon Selection
            # 1         Cut Polygon Similar Touching
            # 2         Cut Polygon Similar Object
            # 3         Cut Polygon Similar on Layer
            # 4         Cut Connected Polygons

        SelectCopyCutResultMesh = bool()
        if self.dyna_IsSet(3):
            SelectCopyCutResultMesh = True
        elif self.dyna_Bool(3) == None:
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



        Mesh_Source = scene.selectedByType('mesh')[0]
        Mesh_Source_ID = Mesh_Source.Ident()
        # lx.out('Source Mesh:', Mesh_Source_ID)

        if self.dyna_IsSet(2):
            if CoplanarConnectedMode == 1:
                lx.eval('smo.GC.SelectCoPlanarPoly 0 2 0.0')
            if CoplanarConnectedMode == 2:
                lx.eval('smo.GC.SelectCoPlanarPoly 1 2 1000')
            if CoplanarConnectedMode == 3:
                lx.eval('smo.GC.SelectCoPlanarPoly 2 2 1000')
            if CoplanarConnectedMode == 4:
                lx.eval('select.connect')

        if CopyOrCut == False:
            lx.eval('copy')
        if CopyOrCut == True:
            lx.eval('cut')
        lx.eval('layer.new')

        Mesh_Child = scene.selectedByType('mesh')[0]
        Mesh_Child_ID = Mesh_Child.Ident()
        # lx.out('Child Mesh:', Mesh_Child_ID)
        lx.eval('select.subItem {%s} add mesh 0 0' % Mesh_Source_ID)
        lx.eval('item.parent')
        lx.eval('smo.GC.DeselectAll')

        scene.select(Mesh_Child_ID)
        lx.eval('paste')
        lx.eval('select.drop polygon')

        if VisibleMode == 0:
            lx.eval('select.type item')
            lx.eval('hide.sel')
            lx.eval('select.type polygon')
            #lx.eval('layer.setVisibility')

        if SelectCopyCutResultMesh == False:
            scene.select(Mesh_Source_ID)
        if SelectCopyCutResultMesh == True:
            scene.select(Mesh_Child_ID)
        lx.eval('select.drop polygon')



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

lx.bless(SMO_CAD_CopyCutAsChildOfCurrentMesh_Cmd, Command_Name)