# python
# ---------------------------------------
# Name:         SMO_CAD_MergeCoplanarPoly_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to:
#               Merge the selected Polygons based
#               on their facing Angle to delete the
#               Edges inside those Polygons.
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      22/01/2020
# Copyright:    (c) Franck Elisabeth 2017-2022
# ---------------------------------------
import lx, lxu, modo

Command_Name = "smo.CAD.MergeCoplanarPoly"
# smo.CAD.MergeCoplanarPoly 0 2

class SMO_CAD_MergeCoplanarPoly_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Mode", lx.symbol.sTYPE_INTEGER)
        self.dyna_Add("Angle", lx.symbol.sTYPE_INTEGER)

        self.SelModePoly = bool(lx.eval1("select.typeFrom typelist:polygon;vertex;edge;item ?"))

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO CAD MergeCoplanarPoly'

    def cmd_Desc(self):
        return 'Merge the selected Polygons based on their facing Angle to delete the Edges inside those Polygons.'

    def cmd_Tooltip(self):
        return 'Merge the selected Polygons based on their facing Angle to delete the Edges inside those Polygons.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO CAD MergeCoplanarPoly'

    def cmd_Flags(self):
        return lx.symbol.fCMD_UNDO

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()

        if self.SelModePoly == True:
            lx.eval('smo.MASTER.ForceSelectMeshItemOnly')

        # ############### 1 ARGUMENTS Test ###############
        # LS_Mode = 0
        # Angle = 2
        # ############### ARGUMENTS ###############

        ############### 5 ARGUMENTS ###############
        # LS_Mode = 0 (Similar Touching Mode)
        # LS_Mode = 1 (Similar on Object Mode)
        # LS_Mode = 2 (Similar on Item Mode)
        LS_Mode = self.dyna_Int(0)
        lx.out('Lazy Select Mode:', LS_Mode)

        Angle = self.dyna_Int(1)
        lx.out('Lazy Select Facing Ratio Angle:', Angle)
        ############### ARGUMENTS ###############


        ##############################
        ####### SAFETY CHECK 1 #######
        ##############################
        lx.eval("user.defNew name:SMO_SafetyCheck_Only1MeshItemSelected type:integer life:momentary")
        #####-------------------- safety check 1 : Only One Item Selected --- START --------------------#####
        ItemCount = lx.eval('query layerservice layer.N ? fg')
        lx.out('Selected Item count:', ItemCount)

        if ItemCount != 1:
            SMO_SafetyCheck_Only1MeshItemSelected = 0
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMO Delete Edge Inside Poly Advanced:}')
            lx.eval(
                'dialog.msg {You must only select the Mesh Item layer you are working on, in Item List, to run that script}')
            lx.eval('+dialog.open')
            lx.out('Only One Item Selected result:', SMO_SafetyCheck_Only1MeshItemSelected)
            lx.out('script Stopped: Select only one Mesh Item')
            sys.exit

        else:
            SMO_SafetyCheck_Only1MeshItemSelected = 1
            lx.out('Only One Item Selected:', SMO_SafetyCheck_Only1MeshItemSelected)
            lx.out('script running: right amount of Mesh Item selected')
        #####-------------------- safety check 1 : Only One Item Selected --- END --------------------#####


        mesh = scene.selectedByType('mesh')[0]

        ##############################
        ####### SAFETY CHECK 2 #######
        ##############################
        lx.eval("user.defNew name:SMO_SafetyCheck_PolygonModeEnabled type:integer life:momentary")
        #####--------------------  safety check 2: Polygon Selection Mode enabled --- START --------------------#####
        selType = ""
        # Used to query layerservice for the list of polygons, edges or vertices.
        attrType = ""

        if lx.eval1("select.typeFrom typelist:vertex;polygon;edge;item;ptag ?"):
            selType = "vertex"
            attrType = "vert"

            SMO_SafetyCheck_PolygonModeEnabled = 0
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMO Delete Edge Inside Poly Advanced:}')
            lx.eval('dialog.msg {You must be in Polygon Mode to run that script}')
            lx.eval('+dialog.open')
            lx.out('script Stopped: You must be in Polygon Mode to run that script')
            sys.exit

        elif lx.eval1("select.typeFrom typelist:edge;vertex;polygon;item ?"):
            selType = "edge"
            attrType = "edge"

            SMO_SafetyCheck_PolygonModeEnabled = 0
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMO Delete Edge Inside Poly Advanced:}')
            lx.eval('dialog.msg {You must be in Polygon Mode to run that script}')
            lx.eval('+dialog.open')
            lx.out('script Stopped: You must be in Polygon Mode to run that script')
            sys.exit

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
            lx.eval('dialog.title {SMO Delete Edge Inside Poly Advanced:}')
            lx.eval('dialog.msg {You must be in Polygon Mode to run that script}')
            lx.eval('+dialog.open')
            lx.out('script Stopped: You must be in Polygon Mode to run that script')
            sys.exit
        #####--------------------  safety check 2: Polygon Selection Mode enabled --- END --------------------#####


        ##############################
        ####### SAFETY CHECK 3 #######
        ##############################
        lx.eval("user.defNew name:SMO_SafetyCheck_min1PolygonSelected type:integer life:momentary")
        #####--------------------  safety check 3: at Least 3 Polygons are selected --- START --------------------#####
        #####--- Get current selected polygon count --- START ---#####
        #####
        CsPolys = len(mesh.geometry.polygons.selected)
        lx.out('Count Selected Poly', CsPolys)
        #####
        #####--- Get current selected polygon count --- END ---#####


        if CsPolys == 0:
            SMO_SafetyCheck_min1PolygonSelected = 0
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMO Delete Edge Inside Poly Advanced:}')
            lx.eval('dialog.msg {You must select more than 2 polygons selected to run that script}')
            lx.eval('+dialog.open')
            lx.out('script Stopped: Add more polygons to your selection')
            sys.exit

        elif CsPolys >= 1:
            SMO_SafetyCheck_min1PolygonSelected = 1
            lx.out('script running: right amount of polygons in selection')
        #####--------------------  safety check 3: at Least 3 Polygons are selected --- END --------------------#####


        if SMO_SafetyCheck_Only1MeshItemSelected == 1 and SMO_SafetyCheck_PolygonModeEnabled == 1 and SMO_SafetyCheck_min1PolygonSelected == 1:
            # lx.eval('user.value sene_LS_facingRatio {%i}' % Angle)
            if LS_Mode == 0:
                # lx.eval('@lazySelect.pl selectTouching 2')
                lx.eval('smo.GC.SelectCoPlanarPoly 0 {%i} 0' % Angle)
                lx.eval('poly.merge')
            if LS_Mode == 1:
                # lx.eval('@lazySelect.pl selectOnObject')
                lx.eval('smo.GC.SelectCoPlanarPoly 1 2 1000')
            if LS_Mode == 2:
                # lx.eval('@lazySelect.pl selectAll')
                lx.eval('smo.GC.SelectCoPlanarPoly 2 2 1000')
            if LS_Mode == 1 or LS_Mode == 2:
                lx.eval('select.convert edge')
                lx.eval('select.contract')
                lx.eval('!!delete')
                lx.eval('select.nextMode')
            lx.eval('select.drop polygon')

    def cmd_Query(self, index, vaQuery):
        lx.notimpl()

lx.bless(SMO_CAD_MergeCoplanarPoly_Cmd, Command_Name)