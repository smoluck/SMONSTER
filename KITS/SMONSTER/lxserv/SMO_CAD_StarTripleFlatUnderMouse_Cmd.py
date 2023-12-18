# python
"""
Name:         SMO_CAD_StarTripleFlatUnderMouse_Cmd

Purpose:      This script is designed to:
              Star Triple Similar Touching (Mouse over a polygon in item mode and launch)

Author:       Franck ELISABETH
Website:      https://www.linkedin.com/in/smoluck/
Created:      22/09/2020
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo
import sys

Cmd_Name = "smo.CAD.StarTripleFlat"
# smo.CAD.StarTripleFlat


class SMO_CAD_StarTripleFlatUnderMouse_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        # self.dyna_Add("Similar Selection Mode", lx.symbol.sTYPE_INTEGER)
        # self.basic_SetFlags(0, lx.symbol.fCMDARG_OPTIONAL)  # here the (0) define the argument index.
        # self.dyna_Add("Select Loop Automatic", lx.symbol.sTYPE_INTEGER)
        # self.basic_SetFlags(1, lx.symbol.fCMDARG_OPTIONAL)  # here the (0) define the argument index.

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO CAD - Star Triple Flat'

    def cmd_Desc(self):
        return 'Star Triple Similar Touching (Mouse over a polygon in item mode and launch).'

    def cmd_Tooltip(self):
        return 'Star Triple Similar Touching (Mouse over a polygon in item mode and launch).'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO CAD - Star Triple Flat'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        # IntSimilarMode = self.dyna_Int(0)
        # IntSelectLoop = self.dyna_Int(1)
        scene = modo.scene.current()

        # ------------- 5 ARGUMENTS ------------- #
        # args = lx.args()
        # lx.out(args)
        #
        # 0 = Similar Touching
        # 1 = Similar Object
        # 2 = Similar Layer
        # SimilarMode = IntSimilarMode
        # lx.out('Similar Selection Mode:', SimilarMode)
        #
        # 0 = Select Loop
        # 1 = Keep current selection
        # SelectLoop = IntSelectLoop
        # lx.out('Select Loop Automatic:', SelectLoop)
        # ------------- ARGUMENTS ------------- #



        # ------------------------------ #
        # <----( DEFINE VARIABLES )----> #
        # ------------------------------ #

        # ---------------- Define user value for all the different SafetyCheck --- START
        #####
        lx.eval("user.defNew name:SMO_SafetyCheck_PolygonModeEnabled type:integer life:momentary")

        lx.eval("user.defNew name:SMO_SafetyCheck_ItemModeEnabled type:integer life:momentary")
        lx.eval("user.defNew name:SMO_SafetyCheck_min1PolygonSelected type:integer life:momentary")
        #####
        # ---------------- Define user value for all the different SafetyCheck --- END

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

            SMO_SafetyCheck_ItemModeEnabled = 0
            SMO_SafetyCheck_PolygonModeEnabled = 0
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMO VeNom:}')
            lx.eval('dialog.msg {You must be in Item Mode and have 1 Mesh Layer selected to run that script.}')
            lx.eval('+dialog.open')
            lx.out('script Stopped: You must be in Item Mode and have 1 Mesh Layer selected to run that script.')
            sys.exit
            # sys.exit( "LXe_FAILED:Must be in polygon selection mode." )


        elif lx.eval1("select.typeFrom typelist:edge;vertex;polygon;item ?"):
            selType = "edge"
            attrType = "edge"

            SMO_SafetyCheck_ItemModeEnabled = 0
            SMO_SafetyCheck_PolygonModeEnabled = 0
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMO VeNom:}')
            lx.eval('dialog.msg {You must be in Item Mode and have 1 Mesh Layer selected to run that script.}')
            lx.eval('+dialog.open')
            lx.out('script Stopped: You must be in Item Mode and have 1 Mesh Layer selected to run that script.')
            sys.exit
            # sys.exit( "LXe_FAILED:Must be in polygon selection mode." )

        elif lx.eval1("select.typeFrom typelist:polygon;vertex;edge;item ?"):
            selType = "polygon"
            attrType = "poly"

            SMO_SafetyCheck_ItemModeEnabled = 0
            SMO_SafetyCheck_PolygonModeEnabled = 1
            lx.out('script Running: Correct Item Selection Mode')
            # sys.exit( "LXe_FAILED:Must be in polygon selection mode." )
        else:
            # This only fails if none of the three supported selection
            # modes have yet been used since the program started, or
            # if "item" or "ptag" (ie: materials) is the current
            # selection mode.
            SMO_SafetyCheck_ItemModeEnabled = 1
            SMO_SafetyCheck_PolygonModeEnabled = 0
            lx.out('script Running: Correct Item Selection Mode')
        # --------------------  safety check 1: Polygon Selection Mode enabled --- END

        #####-------------------------------------------------------------------------------#####
        ####### Track Mouse Over Selection. Is there a polygon under Mouse and select it. #######
        #####-------------------------------------------------------------------------------#####
        if SMO_SafetyCheck_ItemModeEnabled == 1:
            lx.eval('select.type polygon')

            lx.eval('query view3dservice mouse ?')
            view_under_mouse = lx.eval('query view3dservice mouse.view ?')
            lx.eval('query view3dservice view.index ? %s' % view_under_mouse)
            lx.eval('query view3dservice mouse.pos ?')
            Item_under_mouse = lx.eval('query view3dservice element.over ? ITEM ')
            Poly_under_mouse = lx.eval('query view3dservice element.over ? POLY ')
            # edge_under_mouse = lx.eval('query view3dservice element.over ? EDGE ')
            hitpos = lx.eval('query view3dservice mouse.hitpos ?')

            lx.out(view_under_mouse)
            lx.out(Item_under_mouse)
            lx.out(Poly_under_mouse)
            lx.out(hitpos)

            lx.eval('select.drop polygon')
            # lx.eval('materials.underMouse')

            success = True
            try:
                lx.eval('select.3DElementUnderMouse')
            except:
                success = False
        scene = modo.Scene()
        scene.select(Item_under_mouse)
        mesh = scene.selectedByType('mesh')[0]
        items = scene.selected
        # lx.out(items)

        selected_mesh = scene.selected[0]  # gets the current selected object (throws an error if nothing is selected)
        target_positions = selected_mesh.transforms.position.get()
        # lx.out(target_positions)
        target_rotations = selected_mesh.transforms.rotation.get()
        # lx.out(target_positions)

        # -------------------------- #
        # <---( SAFETY CHECK 2 )---> #
        # -------------------------- #
        CsPolys = len(mesh.geometry.polygons.selected)
        # at Least 1 Polygons is selected --- START
        lx.out('Count Selected Poly', CsPolys)

        if CsPolys < 1:
            SMO_SafetyCheck_min1PolygonSelected = 0
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMO VeNom:}')
            lx.eval('dialog.msg {You must mouse over a polygon to run that script}')
            lx.eval('+dialog.open')
            lx.out('script Stopped: Mouse over a polygon')
            sys.exit

        elif CsPolys >= 1:
            SMO_SafetyCheck_min1PolygonSelected = 1
            lx.out('script running: right amount of polygons in selection')
        # at Least 1 Polygons is selected --- END

        # ---------------- Define current value for the Prerequisite TotalSafetyCheck --- START
        #####
        TotalSafetyCheckTrueValue = 2
        lx.out('Desired Value', TotalSafetyCheckTrueValue)
        if SMO_SafetyCheck_ItemModeEnabled == 1:
            TotalSafetyCheck = (SMO_SafetyCheck_ItemModeEnabled + SMO_SafetyCheck_min1PolygonSelected)
            lx.out('Current Value', TotalSafetyCheck)

        #####
        # ---------------- Define current value for the Prerequisite TotalSafetyCheck --- END

        # Modo_ver = int(lx.eval ('query platformservice appversion ?'))
        # lx.out('Modo Version:',Modo_ver)

        # ------------------------ #
        # <----( Main Macro )----> #
        # ------------------------ #

        # ---------------- Compare TotalSafetyCheck value and decide or not to continue the process  --- START
        if TotalSafetyCheck == TotalSafetyCheckTrueValue:
            # Polygon Undermouse Selection Mode. You must be in Item Mode
            if SMO_SafetyCheck_ItemModeEnabled == 1:
                lx.eval('select.type polygon')
                # if SimilarMode == 0:
                #     lx.eval('smo.GC.SelectCoPlanarPoly 0 2 0')
                # if SimilarMode == 1:
                #     lx.eval('smo.GC.SelectCoPlanarPoly 1 2')
                # if SimilarMode == 2:
                #     lx.eval('smo.GC.SelectCoPlanarPoly 2 2')
                lx.eval('smo.GC.SelectCoPlanarPoly 0 2 0')
                lx.eval('smo.GC.StarTriple')
                lx.eval('select.type item')
                lx.eval('smo.GC.DeselectAll')


lx.bless(SMO_CAD_StarTripleFlatUnderMouse_Cmd, Cmd_Name)
