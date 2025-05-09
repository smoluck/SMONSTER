# python
"""
Name:         SMO_MIFABOMA_BOOL_Cmd.py

Purpose:      This script is designed to
              boolean Subtract the last Polygon Selection
              (Connected Polygons) from the current Layer.

Author:       Franck ELISABETH (with the help of Tom Dymond for debug)
Website:      https://www.linkedin.com/in/smoluck/
Created:      27/02/2020
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.MIFABOMA.Boolean"
# smo.MIFABOMA.Boolean 0


class SMO_MIFABOMA_Bool_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Mode", lx.symbol.sTYPE_INTEGER)

        self.SelModePoly = bool(lx.eval1("select.typeFrom typelist:polygon;vertex;edge;item ?"))

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO MIFABOMA - Boolean'

    def cmd_Desc(self):
        return 'Mirror current Polygon Selection using Item Center.'

    def cmd_Tooltip(self):
        return 'Mirror current Polygon Selection using Item Center.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO MIFABOMA - Boolean'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        mode = self.dyna_Int(0)
        scene = modo.scene.current()
        if self.SelModePoly:
            lx.eval('smo.MASTER.ForceSelectMeshItemOnly')

        mesh = scene.selectedByType('mesh')[0]
        CsPolys = len(mesh.geometry.polygons.selected)



        # <----( Get currently Visible Items in Viewport )----> #
        lx.eval('select.itemType mesh')
        SceneMeshes = list(scene.selectedByType("mesh"))
        TCount = len(SceneMeshes)
        # print(TCount)
        lx.eval('smo.GC.DeselectAll')
        VisibleIDList = []
        VisibleNameList = []
        for item in SceneMeshes:
            itemType = modo.Item(item).type
            item = lx.object.Item(item)
            ID = item.Ident()
            if itemType == "mesh" or itemType == "meshInst":
                isVisible = lx.eval("layer.setVisibility {%s} ?" % ID)
                # print(isVisible)
                if isVisible:
                    VisibleNameList.append(item.UniqueName())
                    VisibleIDList.append(ID)
        # print(VisibleNameList)
        # print(VisibleIDList)
        scene.select(mesh)
        lx.eval('select.type polygon')



        # ------------------------------ #
        # <----( DEFINE VARIABLES )----> #
        # ------------------------------ #

        # ---------------- Define user value for all the different SafetyCheck --- START
        #####
        lx.eval("user.defNew name:SMO_SafetyCheck_PolygonModeEnabled type:integer life:momentary")
        lx.eval("user.defNew name:SMO_SafetyCheck_min1PolygonSelected type:integer life:momentary")
        #####
        # ---------------- Define user value for all the different SafetyCheck --- END

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

        # -------------------------- #
        # <---( SAFETY CHECK 1 )---> #
        # -------------------------- #

        # --------------------  safety check 1: Polygon Selection Mode enabled --- START

        selType = ""
        # Used to query layerservice for the list of polygons, edges or vertices.
        attrType = ""

        if lx.eval1("select.typeFrom typelist:vertex;polygon;edge;item;ptag ?"):
            selType = "vertex"
            attrType = "vert"

            SMO_SafetyCheck_PolygonModeEnabled = 0
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMO_BoolSubtract:}')
            lx.eval('dialog.msg {You must be in Polygon Mode to run that script}')
            lx.eval('+dialog.open')
            lx.out('script Stopped: You must be in Polygon Mode to run that script')
            sys.exit
            # sys.exit( "LXe_FAILED:Must be in polygon selection mode." )


        elif lx.eval1("select.typeFrom typelist:edge;vertex;polygon;item ?"):
            selType = "edge"
            attrType = "edge"

            SMO_SafetyCheck_PolygonModeEnabled = 0
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMO_BoolSubtract:}')
            lx.eval('dialog.msg {You must be in Polygon Mode to run that script}')
            lx.eval('+dialog.open')
            lx.out('script Stopped: You must be in Polygon Mode to run that script')
            sys.exit
            # sys.exit( "LXe_FAILED:Must be in polygon selection mode." )

        elif lx.eval1("select.typeFrom typelist:polygon;vertex;edge;item ?"):
            selType = "polygon"
            attrType = "poly"

            SMO_SafetyCheck_PolygonModeEnabled = 1
            lx.out('script Running: Correct Component Selection Mode')


        else:
            # This only fails if none of the three supported selection
            # modes have yet been used since the program started, or
            # if "item" or "ptag" (ie: materials) is the current
            # selection mode.
            SMO_SafetyCheck_PolygonModeEnabled = 0
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMO_BoolSubtract:}')
            lx.eval('dialog.msg {You must be in Polygon Mode to run that script}')
            lx.eval('+dialog.open')
            lx.out('script Stopped: You must be in Polygon Mode to run that script')
            sys.exit
            # sys.exit( "LXe_FAILED:Must be in polygon selection mode." )
        # --------------------  safety check 1: Polygon Selection Mode enabled --- END

        # -------------------------- #
        # <---( SAFETY CHECK 2 )---> #
        # -------------------------- #

        # at Least 1 Polygons is selected --- START
        lx.out('Count Selected Poly', CsPolys)

        if CsPolys < 1:
            SMO_SafetyCheck_min1PolygonSelected = 0
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMO_BoolSubtract:}')
            lx.eval('dialog.msg {You must select at least 1 polygon to run that script}')
            lx.eval('+dialog.open')
            lx.out('script Stopped: Add more polygons to your selection')
            sys.exit

        elif CsPolys >= 1:
            SMO_SafetyCheck_min1PolygonSelected = 1
            lx.out('script running: right amount of polygons in selection')
        # at Least 1 Polygons is selected --- END

        # ---------------- Define current value for the Prerequisite TotalSafetyCheck --- START
        #####
        TotalSafetyCheckTrueValue = 2
        lx.out('Desired Value', TotalSafetyCheckTrueValue)
        TotalSafetyCheck = (SMO_SafetyCheck_PolygonModeEnabled + SMO_SafetyCheck_min1PolygonSelected)
        lx.out('Current Value', TotalSafetyCheck)
        #####
        # ---------------- Define current value for the Prerequisite TotalSafetyCheck --- END

        # ------------------------ #
        # <----( Main Macro )----> #
        # ------------------------ #

        # -------------------- Compare TotalSafetyCheck value and decide or not to continue the process  --- START
        if TotalSafetyCheck == TotalSafetyCheckTrueValue:
            # replay name:"Edit Selection Set"
            lx.eval('select.editSet name:Bool_Selected_Tag mode:add')
            # replay name:"Item"
            lx.eval('select.type item')
            lx.eval('select.editSet name:Bool_SOURCE_Tag mode:add')
            lx.eval('select.type polygon')
            # replay name:"Selection All"
            lx.eval('select.all')
            # replay name:"Cut Selection"
            lx.eval('cut')
            lx.eval('layer.new')
            # replay name:"Paste Selection"
            lx.eval('paste')
            # replay name:"Item"
            lx.eval('select.type item')
            # replay name:"Edit Selection Set"
            lx.eval('select.editSet name:Bool_Parent_Tag mode:add')
            # replay name:"Select Polygons"
            lx.eval('select.polygon action:remove test:0 mode:subdiv value:0')
            # replay name:"Use Selection Set"
            lx.eval('select.useSet name:Bool_Selected_Tag mode:select')
            # replay name:"Select Connected"
            lx.eval('select.connect')
            # replay name:"Cut Selection"
            lx.eval('cut')
            lx.eval('layer.new')
            # replay name:"Paste Selection"
            lx.eval('paste')
            # replay name:"Item"
            lx.eval('select.type item')
            # replay name:"Edit Selection Set"
            lx.eval('select.editSet name:Bool_Driver_Tag mode:add')
            lx.eval('select.drop item')
            # replay name:"Use Selection Set"
            lx.eval('select.useSet name:Bool_Driver_Tag mode:select')
            # replay name:"Use Selection Set"
            lx.eval('select.useSet name:Bool_Parent_Tag mode:select')
            # replay name:"Hide Unselected"
            lx.eval('hide.unsel')
            lx.eval('select.drop item')
            # replay name:"Use Selection Set"
            lx.eval('select.useSet name:Bool_Parent_Tag mode:select')

            # -------------------------- #
            # <----( Main Command )---->
            # -------------------------- #
            if mode == 0:
                # replay name:"Boolean Action SUBTRACT"
                lx.eval('poly.boolean mode:subtract cutmesh:background')
            if mode == 1:
                # replay name:"Boolean Action SUBTRACT"
                lx.eval('poly.boolean mode:union cutmesh:background')
            if mode == 2:
                # replay name:"Boolean Action SUBTRACT"
                lx.eval('poly.boolean mode:intersect cutmesh:background')
            # -------------------------- #
            # <----( Main Command )---->
            # -------------------------- #

            lx.eval('select.type polygon')
            # replay name:"Selection All"
            lx.eval('select.all')
            # replay name:"Copy Selection"
            lx.eval('copy')
            # replay name:"Item"
            lx.eval('select.type item')
            # replay name:"Delete"
            lx.eval('!delete')
            # replay name:"Use Selection Set"
            lx.eval('select.useSet name:Bool_Driver_Tag mode:select')
            # replay name:"Delete"
            lx.eval('!delete')
            lx.eval('select.useSet name:Bool_SOURCE_Tag mode:select')
            # replay name:"Unhide"
            lx.eval('unhide')
            lx.eval('select.type polygon')
            # replay name:"Paste Selection"
            lx.eval('paste')
            # replay name:"Item"
            lx.eval('select.type item')
            lx.eval('!select.deleteSet Bool_Driver_Tag false')
            lx.eval('!select.deleteSet Bool_Parent_Tag false')
            lx.eval('!select.deleteSet Bool_SOURCE_Tag false')
            lx.eval('select.type polygon')
            lx.eval('select.polygon remove 0 subdiv 0')

            try:
                lx.eval('select.drop polygon')
                lx.eval('!select.deleteSet Bool_Selected_Tag false')
            except:
                lx.eval('select.drop polygon')

        elif TotalSafetyCheck != TotalSafetyCheckTrueValue:
            lx.out('script Stopped: your mesh does not match the requirement for that script.')
            sys.exit



        # -------------- COPY/PASTE END Procedure  -------------- #
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
        # -------------------------------------------- #



        # <----( Get Back currently Visible Items in Viewport )----> #
        lx.eval('select.type item')
        lx.eval('unhide')
        lx.eval('smo.GC.DeselectAll')
        for i in range(0, len(VisibleNameList)):
            lx.eval('select.subItem {%s} add mesh 0 0' % VisibleNameList[i])
        lx.eval('hide.unsel')
        lx.eval('smo.GC.DeselectAll')
        scene.select(mesh)
        lx.eval('select.type polygon')

        lx.out('End of SMO_Bool_Subtract Script')
        # ---------------- Compare TotalSafetyCheck value and decide or not to continue the process  --- END


    def cmd_Query(self, index, vaQuery):
        lx.notimpl()


lx.bless(SMO_MIFABOMA_Bool_Cmd, Cmd_Name)
