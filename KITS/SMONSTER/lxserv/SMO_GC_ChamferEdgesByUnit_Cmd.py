# python
# ---------------------------------------
# Name:         SMO_GC_ChamferEdgesByUnit_Cmd.py
# Version:      1.0
#
# Purpose:      This Command is designed to
#               Chamfer currently selected Edges (or Selection Boundary Edges if in Polygon Mode) with a Chamfer set to 1 Side, using arguments by unit and width.
#
# Author:       Franck ELISABETH (with the help of Tom Dymond for debug)
# Website:      http://www.smoluck.com
#
# Created:      16/09/2019
# Copyright:    (c) Franck Elisabeth 2017-2022
# ---------------------------------------

import lx, lxu, modo

Cmd_Name = "smo.GC.ChamferEdgesByUnit"
# smo.GC.ChamferEdgesByUnit [1mm]       # Using Square Brackets around values validate the use of units like "km", "m" , "cm", "mm", "um".

class SMO_GC_ChamferEdgesByUnit_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Witdh Value", lx.symbol.sTYPE_DISTANCE)

        self.SelModeEdge = bool(lx.eval1("select.typeFrom typelist:edge;vertex;polygon;item ?"))
        self.SelModePoly = bool(lx.eval1("select.typeFrom typelist:polygon;vertex;edge;item ?"))

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO GC - Chamfer Edges by Unit'

    def cmd_Desc(self):
        return 'Chamfer currently selected Edges (or Selection Boundary Edges if in Polygon Mode) with a Chamfer set to 1 Side, using arguments by unit and width.'

    def cmd_Tooltip(self):
        return 'Chamfer currently selected Edges (or Selection Boundary Edges if in Polygon Mode) with a Chamfer set to 1 Side, using arguments by unit and width.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO GC - Chamfer Edges by Unit'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()
        EdgeCount = int(lx.eval('user.value SMO_UseVal_GC_ChamferEdgeCount ?'))
        #lx.out(EdgeCount)

        if self.SelModeEdge == True or self.SelModePoly == True:
            lx.eval('smo.MASTER.ForceSelectMeshItemOnly')

        #######################################################
        ## <----( Convert to Boundary if POLYGON Mode )----> ##
        #######################################################
        if self.SelModePoly == True:
            lx.eval('script.run "macro.scriptservice:92663570022:macro"')
            lx.eval('select.type edge')

        mesh = scene.selectedByType('mesh')[0]
        SelItems = (lx.evalN('query sceneservice selection ? locator'))
        lx.out('Selected items is:', SelItems)

        ################################
        # <----[ DEFINE ARGUMENTS ]---->#
        ################################
        Value = self.dyna_Float(0)              # Width size

        # Expose the Result of the Arguments
        # lx.out(Value)
        ################################
        # <----[ DEFINE ARGUMENTS ]---->#
        ################################


        lx.eval('smo.MASTER.SelectModeDetector')

        VertMode = lx.eval1('user.value SMO_SelectModeDetector_Vert ?')
        EdgeMode = lx.eval1('user.value SMO_SelectModeDetector_Edge ?')
        PolyMode = lx.eval1('user.value SMO_SelectModeDetector_Poly ?')
        ItemMode = lx.eval1('user.value SMO_SelectModeDetector_Item ?')

        NoVert = lx.eval1('user.value SMO_SelectModeDetector_NoVertSelected ?')
        NoEdge = lx.eval1('user.value SMO_SelectModeDetector_NoEdgeSelected ?')
        NoPoly = lx.eval1('user.value SMO_SelectModeDetector_NoPolySelected ?')
        NoItem = lx.eval1('user.value SMO_SelectModeDetector_NoItemSelected ?')

        MultiVert = lx.eval1('user.value SMO_SelectModeDetector_MultiVertSelected ?')
        MultiEdge = lx.eval1('user.value SMO_SelectModeDetector_MultiEdgeSelected ?')
        MultiPoly = lx.eval1('user.value SMO_SelectModeDetector_MultiPolySelected ?')
        MultiItem = lx.eval1('user.value SMO_SelectModeDetector_MultiItemSelected ?')

        CountVert = lx.eval1('user.value SMO_SelectModeDetector_CountVertSelected ?')
        CountEdge = lx.eval1('user.value SMO_SelectModeDetector_CountEdgeSelected ?')
        CountPoly = lx.eval1('user.value SMO_SelectModeDetector_CountPolySelected ?')
        CountItem = lx.eval1('user.value SMO_SelectModeDetector_CountItemSelected ?')

        lx.out('V---------- Selection Mode ----------V')
        lx.out('Vert Mode', VertMode)
        lx.out('Edge Mode', EdgeMode)
        lx.out('Poly Mode', PolyMode)
        lx.out('Item Mode', ItemMode)
        lx.out('V---------- Element Not Selected ----------V')
        lx.out('No Vert Selected', NoVert)
        lx.out('No Edge Selected', NoEdge)
        lx.out('No Poly Selected', NoPoly)
        lx.out('No Item Selected', NoItem)
        lx.out('V---------- At least one Element Selected ----------V')
        lx.out('Multi Vert Selected', MultiVert)
        lx.out('Multi Edge Selected', MultiEdge)
        lx.out('Multi Poly Selected', MultiPoly)
        lx.out('Multi Item Selected', MultiItem)
        lx.out('V---------- At least one Element Selected ----------V')
        lx.out('Vert Count Selected', CountVert)
        lx.out('Multi Count Selected', CountEdge)
        lx.out('Multi Count Selected', CountPoly)
        lx.out('Multi Count Selected', CountItem)



        ########################################
        ## <----( Main Macro - EDGE )----> ##
        ########################################
        if ItemMode == 0 and VertMode == 0 and PolyMode == 0 and CountItem > 0:
            if EdgeMode == 1 :
                # if CountEdge >= 1 :

                ###################################
                ######## Mirror Tool Setup ########
                ###################################
                lx.eval('tool.snapState false')
                lx.eval('tool.set edge.chamfer on')
                lx.eval('tool.setAttr edge.chamfer offset {%f}' % Value)
                lx.eval('tool.setAttr edge.chamfer mode inset')
                lx.eval('tool.setAttr edge.chamfer segments %s' % EdgeCount)
                lx.eval('tool.setAttr edge.chamfer shape round')
                lx.eval('tool.setAttr edge.chamfer edgeEnd profile')

                # Disable the Bevel Clamping. If the value is higher than the smallest thickness it will clamp that value. Better to disable this.
                lx.eval('tool.setAttr edge.chamfer stopAtEdge false')
                lx.eval('tool.setAttr edge.chamfer autoWeld false')
                lx.eval('tool.setAttr edge.chamfer parallel true')
                lx.eval('tool.setAttr edge.chamfer coplanar false')
                lx.eval('tool.setAttr edge.chamfer sharpCorner false')
                lx.eval('tool.setAttr edge.chamfer useMat false')
                lx.eval('tool.setAttr edge.chamfer depth 1.0')
                lx.eval('tool.setAttr edge.chamfer flatness 0.0')
                lx.eval('tool.setAttr edge.chamfer mitering 0.0')
                lx.eval('tool.setAttr edge.chamfer boundExtend true')
                lx.eval('tool.setAttr edge.chamfer reversex false')
                lx.eval('tool.setAttr edge.chamfer reversey false')
                ##############################
                lx.eval('tool.doApply')
                lx.eval('select.drop edge')
                lx.eval('select.nextMode')

                lx.out('End of SMO GC ChamferEdgesHardWay Command')

        if self.SelModePoly == True:
            lx.eval('select.type polygon')
            lx.eval('select.drop polygon')


    def cmd_Query(self, index, vaQuery):
        lx.notimpl()


lx.bless(SMO_GC_ChamferEdgesByUnit_Cmd, Cmd_Name)
