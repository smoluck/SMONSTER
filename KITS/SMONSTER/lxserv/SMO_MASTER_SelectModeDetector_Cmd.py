# python
"""
Name:         SMO_MASTER_SelectModeDetector_Cmd.py

Purpose:      This Command is designed to Mirror
              Detect the current Component Mode and iterate
              user values based on the detection for further use of the tool.

Author:       Franck ELISABETH
Website:      https://www.linkedin.com/in/smoluck/
Created:      17/05/2020
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.MASTER.SelectModeDetector"


# smo.MASTER.SelectModeDetector 1


class SMO_MASTER_SelectModeDetector_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Debug Mode", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_OPTIONAL)  # here the (1) define the argument index.

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO MASTER - Component Mode Detector'

    def cmd_Desc(self):
        return 'Detect the current Component Mode and iterate user values based on the detection for further use of the tool.'

    def cmd_Tooltip(self):
        return 'Detect the current Component Mode and iterate user values based on the detection for further use of the tool.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO MASTER - Component Mode Detector'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()

        args = lx.args()
        # lx.out(args)
        DEBUG_MODE = self.dyna_Int(0)

        # ------------------------------ #
        # <----( DEFINE VARIABLES )----> #
        # ------------------------------ #
        # ---------------- Define user value for all the different SafetyCheck --- START
        #####
        lx.eval("user.defNew name:SMO_MASTER_SelectModeDetector_ItemModeEnabled type:integer life:momentary")
        lx.eval("user.defNew name:SMO_MASTER_SelectModeDetector_min1ItemSelected type:integer life:momentary")
        lx.eval("user.defNew name:SMO_MASTER_SelectModeDetector_MultiItemSelected type:integer life:momentary")

        lx.eval("user.defNew name:SMO_MASTER_SelectModeDetector_PolyModeEnabled type:integer life:momentary")
        lx.eval("user.defNew name:SMO_MASTER_SelectModeDetector_min1PolySelected type:integer life:momentary")

        lx.eval("user.defNew name:SMO_MASTER_SelectModeDetector_EdgeModeEnabled type:integer life:momentary")
        lx.eval("user.defNew name:SMO_MASTER_SelectModeDetector_min1EdgeSelected type:integer life:momentary")

        lx.eval("user.defNew name:SMO_MASTER_SelectModeDetector_VertModeEnabled type:integer life:momentary")
        lx.eval("user.defNew name:SMO_MASTER_SelectModeDetector_min1VertSelected type:integer life:momentary")
        #####
        # ---------------- Define user value for all the different SafetyCheck --- END

        SMO_MASTER_SelectModeDetector_VertModeEnabled = 0
        SMO_MASTER_SelectModeDetector_min1VertSelected = 0
        SMO_MASTER_SelectModeDetector_EdgeModeEnabled = 0
        SMO_MASTER_SelectModeDetector_min1EdgeSelected = 0
        SMO_MASTER_SelectModeDetector_PolyModeEnabled = 0
        SMO_MASTER_SelectModeDetector_min1PolySelected = 0
        SMO_MASTER_SelectModeDetector_ItemModeEnabled = 0
        SMO_MASTER_SelectModeDetector_min1ItemSelected = 0
        SMO_MASTER_SelectModeDetector_MultiItemSelected = 0

        try:
            item = modo.Item()
            mesh = scene.selectedByType('mesh')[0]
            meshes = scene.selectedByType(lx.symbol.sITYPE_MESH)

            ###############################################
            ####### SAFETY CHECK 1 - Selection Mode #######
            ###############################################

            selType = ""
            # Used to query layerservice for the list of polygons, edges or vertices.
            attrType = ""

            if lx.eval1("select.typeFrom typelist:vertex;polygon;edge;item;ptag ?"):
                selType = "vertex"
                attrType = "vert"

                SMO_MASTER_SelectModeDetector_ItemModeEnabled = 0
                SMO_MASTER_SelectModeDetector_PolyModeEnabled = 0
                SMO_MASTER_SelectModeDetector_EdgeModeEnabled = 0
                SMO_MASTER_SelectModeDetector_VertModeEnabled = 1
                if DEBUG_MODE == 1:
                    lx.out('script Running: Vertex Selection Mode')


            elif lx.eval1("select.typeFrom typelist:edge;vertex;polygon;item ?"):
                selType = "edge"
                attrType = "edge"

                SMO_MASTER_SelectModeDetector_ItemModeEnabled = 0
                SMO_MASTER_SelectModeDetector_PolyModeEnabled = 0
                SMO_MASTER_SelectModeDetector_EdgeModeEnabled = 1
                SMO_MASTER_SelectModeDetector_VertModeEnabled = 0
                if DEBUG_MODE == 1:
                    lx.out('script Running: Edge Selection Mode')


            elif lx.eval1("select.typeFrom typelist:polygon;vertex;edge;item ?"):
                selType = "polygon"
                attrType = "poly"

                SMO_MASTER_SelectModeDetector_ItemModeEnabled = 0
                SMO_MASTER_SelectModeDetector_PolyModeEnabled = 1
                SMO_MASTER_SelectModeDetector_EdgeModeEnabled = 0
                SMO_MASTER_SelectModeDetector_VertModeEnabled = 0
                if DEBUG_MODE == 1:
                    lx.out('script Running: Polygon Selection Mode')


            else:
                # This only fails if none of the three supported selection
                # modes have yet been used since the program started, or
                # if "item" or "ptag" (ie: materials) is the current
                # selection mode.
                # elif lx.eval1( "select.typeFrom typelist:item;polygon;vertex;edge ?" ):
                # selType = "item"
                # attrType = "item"

                SMO_MASTER_SelectModeDetector_ItemModeEnabled = 1
                SMO_MASTER_SelectModeDetector_PolyModeEnabled = 0
                SMO_MASTER_SelectModeDetector_EdgeModeEnabled = 0
                SMO_MASTER_SelectModeDetector_VertModeEnabled = 0
                if DEBUG_MODE == 1:
                    lx.out('script Running: Item Selection Mode')

            # -------------------------------------------- #
            ####### SAFETY CHECK 2 - Component Count #######
            # -------------------------------------------- #
            CsVert = len(mesh.geometry.vertices.selected)
            if DEBUG_MODE == 1:
                lx.out('Count Selected Vertex', CsVert)
            if SMO_MASTER_SelectModeDetector_VertModeEnabled == 1:
                # at Least 1 Polygons is selected --- START
                if CsVert < 1:
                    SMO_MASTER_SelectModeDetector_min1VertSelected = 0

                elif CsVert >= 1:
                    SMO_MASTER_SelectModeDetector_min1VertSelected = 1
                # at Least 1 Polygons is selected --- END

            CsEdges = len(mesh.geometry.edges.selected)
            if DEBUG_MODE == 1:
                lx.out('Count Selected Edge', CsEdges)
            if SMO_MASTER_SelectModeDetector_EdgeModeEnabled == 1:
                # at Least 1 Polygons is selected --- START
                if CsEdges < 1:
                    SMO_MASTER_SelectModeDetector_min1EdgeSelected = 0

                elif CsEdges >= 1:
                    SMO_MASTER_SelectModeDetector_min1EdgeSelected = 1
                # at Least 1 Polygons is selected --- END

            CsPolys = len(mesh.geometry.polygons.selected)
            if DEBUG_MODE == 1:
                lx.out('Count Selected Polygon', CsPolys)

            if SMO_MASTER_SelectModeDetector_PolyModeEnabled == 1:
                # at Least 1 Polygons is selected --- START
                if CsPolys < 1:
                    SMO_MASTER_SelectModeDetector_min1PolySelected = 0

                elif CsPolys >= 1:
                    SMO_MASTER_SelectModeDetector_min1PolySelected = 1
                # at Least 1 Polygons is selected --- END

            # if SMO_MASTER_SelectModeDetector_ItemModeEnabled == 1 :
            # at Least 1 Polygons is selected --- START
            SelectedMeshItemCount = len(scene.selectedByType(lx.symbol.sTYPE_MESH))
            if DEBUG_MODE == 1:
                lx.out('Selected Item Mesh Count', SelectedMeshItemCount)

            if SelectedMeshItemCount < 1:
                SMO_MASTER_SelectModeDetector_min1ItemSelected = 0
                SMO_MASTER_SelectModeDetector_MultiItemSelected = 0

            elif SelectedMeshItemCount == 1:
                SMO_MASTER_SelectModeDetector_min1ItemSelected = 1
                SMO_MASTER_SelectModeDetector_MultiItemSelected = 0

            elif SelectedMeshItemCount > 1:
                SMO_MASTER_SelectModeDetector_min1ItemSelected = 1
                SMO_MASTER_SelectModeDetector_MultiItemSelected = 1
            # at Least 1 Polygons is selected --- END

            # --------------------  safety check 1: Polygon Selection Mode enabled --- END

            if SMO_MASTER_SelectModeDetector_VertModeEnabled == 1:
                lx.eval('user.value SMO_SelectModeDetector_Vert 1')
            if SMO_MASTER_SelectModeDetector_VertModeEnabled == 0:
                lx.eval('user.value SMO_SelectModeDetector_Vert 0')

            if SMO_MASTER_SelectModeDetector_min1VertSelected == 0 and SMO_MASTER_SelectModeDetector_VertModeEnabled == 1:
                lx.eval('user.value SMO_SelectModeDetector_NoVertSelected 1')
                lx.eval('user.value SMO_SelectModeDetector_MultiVertSelected 0')
            if SMO_MASTER_SelectModeDetector_min1VertSelected == 1 and SMO_MASTER_SelectModeDetector_VertModeEnabled == 1:
                lx.eval('user.value SMO_SelectModeDetector_NoVertSelected 0')
                lx.eval('user.value SMO_SelectModeDetector_MultiVertSelected 1')

            lx.eval('user.value SMO_SelectModeDetector_CountVertSelected %s' % CsVert)

            if SMO_MASTER_SelectModeDetector_EdgeModeEnabled == 1:
                lx.eval('user.value SMO_SelectModeDetector_Edge 1')
            if SMO_MASTER_SelectModeDetector_EdgeModeEnabled == 0:
                lx.eval('user.value SMO_SelectModeDetector_Edge 0')

            if SMO_MASTER_SelectModeDetector_min1EdgeSelected == 0 and SMO_MASTER_SelectModeDetector_EdgeModeEnabled == 1:
                lx.eval('user.value SMO_SelectModeDetector_NoEdgeSelected 1')
                lx.eval('user.value SMO_SelectModeDetector_MultiEdgeSelected 0')
            if SMO_MASTER_SelectModeDetector_min1EdgeSelected == 1 and SMO_MASTER_SelectModeDetector_EdgeModeEnabled == 1:
                lx.eval('user.value SMO_SelectModeDetector_NoEdgeSelected 0')
                lx.eval('user.value SMO_SelectModeDetector_MultiEdgeSelected 1')

            lx.eval('user.value SMO_SelectModeDetector_CountEdgeSelected %s' % CsEdges)

            if SMO_MASTER_SelectModeDetector_PolyModeEnabled == 1:
                lx.eval('user.value SMO_SelectModeDetector_Poly 1')
            if SMO_MASTER_SelectModeDetector_PolyModeEnabled == 0:
                lx.eval('user.value SMO_SelectModeDetector_Poly 0')

            if SMO_MASTER_SelectModeDetector_min1PolySelected == 0 and SMO_MASTER_SelectModeDetector_PolyModeEnabled == 1:
                lx.eval('user.value SMO_SelectModeDetector_NoPolySelected 1')
                lx.eval('user.value SMO_SelectModeDetector_MultiPolySelected 0')
            if SMO_MASTER_SelectModeDetector_min1PolySelected == 1 and SMO_MASTER_SelectModeDetector_PolyModeEnabled == 1:
                lx.eval('user.value SMO_SelectModeDetector_NoPolySelected 0')
                lx.eval('user.value SMO_SelectModeDetector_MultiPolySelected 1')

            lx.eval('user.value SMO_SelectModeDetector_CountPolySelected %s' % CsPolys)

            if SMO_MASTER_SelectModeDetector_ItemModeEnabled == 1:
                lx.eval('user.value SMO_SelectModeDetector_Item 1')
            if SMO_MASTER_SelectModeDetector_ItemModeEnabled == 0:
                lx.eval('user.value SMO_SelectModeDetector_Item 0')

            if SMO_MASTER_SelectModeDetector_min1ItemSelected == 0 and SMO_MASTER_SelectModeDetector_ItemModeEnabled == 1:
                lx.eval('user.value SMO_SelectModeDetector_NoItemSelected 1')
            if SMO_MASTER_SelectModeDetector_min1ItemSelected == 1 and SMO_MASTER_SelectModeDetector_ItemModeEnabled == 1:
                lx.eval('user.value SMO_SelectModeDetector_NoItemSelected 0')

            if SMO_MASTER_SelectModeDetector_MultiItemSelected == 0 and SMO_MASTER_SelectModeDetector_ItemModeEnabled == 1:
                lx.eval('user.value SMO_SelectModeDetector_MultiItemSelected 0')
            if SMO_MASTER_SelectModeDetector_MultiItemSelected == 1 and SMO_MASTER_SelectModeDetector_ItemModeEnabled == 1:
                lx.eval('user.value SMO_SelectModeDetector_MultiItemSelected 1')

            lx.eval('user.value SMO_SelectModeDetector_CountItemSelected %s' % SelectedMeshItemCount)



        except:
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMO_ComponentModeDetector_Cmd:}')
            lx.eval(
                'dialog.msg {You must at least select one Mesh Item layer to work on, in the Item List, to run that script}')
            lx.eval('+dialog.open')
            if DEBUG_MODE == 1:
                lx.out('script Stopped: Select at least one Mesh Item')

            lx.eval('user.value SMO_SelectModeDetector_Vert 0')
            lx.eval('user.value SMO_SelectModeDetector_NoVertSelected 1')
            lx.eval('user.value SMO_SelectModeDetector_MultiVertSelected 0')
            lx.eval('user.value SMO_SelectModeDetector_CountVertSelected 0')

            lx.eval('user.value SMO_SelectModeDetector_Edge 0')
            lx.eval('user.value SMO_SelectModeDetector_NoEdgeSelected 1')
            lx.eval('user.value SMO_SelectModeDetector_MultiEdgeSelected 0')
            lx.eval('user.value SMO_SelectModeDetector_CountEdgeSelected 0')

            lx.eval('user.value SMO_SelectModeDetector_Poly 0')
            lx.eval('user.value SMO_SelectModeDetector_NoPolySelected 1')
            lx.eval('user.value SMO_SelectModeDetector_MultiPolySelected 0')
            lx.eval('user.value SMO_SelectModeDetector_CountPolySelected 0')

            lx.eval('user.value SMO_SelectModeDetector_Item 0')
            lx.eval('user.value SMO_SelectModeDetector_NoItemSelected 1')
            lx.eval('user.value SMO_SelectModeDetector_MultiItemSelected 0')
            lx.eval('user.value SMO_SelectModeDetector_CountItemSelected 0')

            # sys.exit

        if DEBUG_MODE == 1:
            A = lx.eval1('user.value SMO_SelectModeDetector_Vert ?')
            B = lx.eval1('user.value SMO_SelectModeDetector_Edge ?')
            C = lx.eval1('user.value SMO_SelectModeDetector_Poly ?')
            D = lx.eval1('user.value SMO_SelectModeDetector_Item ?')

            A1 = lx.eval1('user.value SMO_SelectModeDetector_NoVertSelected ?')
            B1 = lx.eval1('user.value SMO_SelectModeDetector_NoEdgeSelected ?')
            C1 = lx.eval1('user.value SMO_SelectModeDetector_NoPolySelected ?')
            D1 = lx.eval1('user.value SMO_SelectModeDetector_NoItemSelected ?')

            A2 = lx.eval1('user.value SMO_SelectModeDetector_MultiVertSelected ?')
            B2 = lx.eval1('user.value SMO_SelectModeDetector_MultiEdgeSelected ?')
            C2 = lx.eval1('user.value SMO_SelectModeDetector_MultiPolySelected ?')
            D2 = lx.eval1('user.value SMO_SelectModeDetector_MultiItemSelected ?')

            A3 = lx.eval1('user.value SMO_SelectModeDetector_CountVertSelected ?')
            B3 = lx.eval1('user.value SMO_SelectModeDetector_CountEdgeSelected ?')
            C3 = lx.eval1('user.value SMO_SelectModeDetector_CountPolySelected ?')
            D3 = lx.eval1('user.value SMO_SelectModeDetector_CountItemSelected ?')

            lx.out('V---------- Selection Mode ----------V')
            lx.out('Vert Mode', A)
            lx.out('Edge Mode', B)
            lx.out('Poly Mode', C)
            lx.out('Item Mode', D)
            lx.out('V---------- Element Not Selected ----------V')
            lx.out('No Vert Selected', A1)
            lx.out('No Edge Selected', B1)
            lx.out('No Poly Selected', C1)
            lx.out('No Item Selected', D1)
            lx.out('V---------- At least one Element Selected ----------V')
            lx.out('Multi Vert Selected', A2)
            lx.out('Multi Edge Selected', B2)
            lx.out('Multi Poly Selected', C2)
            lx.out('Multi Item Selected', D2)
            lx.out('V---------- At least one Element Selected ----------V')
            lx.out('Count Vert Selected', A3)
            lx.out('Count Edge Selected', B3)
            lx.out('Count Poly Selected', C3)
            lx.out('Count Item Selected', D3)

    def cmd_Query(self, index, vaQuery):
        lx.notimpl()


lx.bless(SMO_MASTER_SelectModeDetector_Cmd, Cmd_Name)
