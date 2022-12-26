# python
"""
# Name:         SMO_GC_SelectCoPlanarPoly_Cmd.py
# Version:      1.0
#
# Purpose:      This Command is designed to
#               (Replace the old Seneca Lazy Select by the Built in Select CoPlanar poly tool.)
#               
#
# Author:       Franck ELISABETH (with the help of Tom Dymond for debug)
# Website:      https://www.smoluck.com
#
# Created:      22/04/2021
# Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.GC.SelectCoPlanarPoly"
# smo.GC.SelectCoPlanarPoly 0 20


class SMO_GC_SelectCoPlanarPoly_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Mode", lx.symbol.sTYPE_INTEGER)
        self.dyna_Add("Angle", lx.symbol.sTYPE_INTEGER)
        self.dyna_Add("Range", lx.symbol.sTYPE_FLOAT)         # Set HardCoded to 10000 in order to not filter by distance when Mode is set to 2
        self.basic_SetFlags (2, lx.symbol.fCMDARG_OPTIONAL)

        self.SelModePoly = bool(lx.eval1("select.typeFrom typelist:polygon;vertex;edge;item ?"))

        # self.dyna_Add("On-Off Toggle", lx.symbol.sTYPE_BOOLEAN)
        # self.dyna_Add("Value", lx.symbol.sTYPE_INTEGER)
        # self.dyna_Add("Value with Decimal", lx.symbol.sTYPE_FLOAT)
        # self.dyna_Add("Text", lx.symbol.sTYPE_STRING)
        # self.dyna_Add("Axis", lx.symbol.sTYPE_AXIS)
        # self.dyna_Add("Value as Distance", lx.symbol.sTYPE_DISTANCE)
        # self.dyna_Add("Fill Color", lx.symbol.sTYPE_COLOR)
        # self.dyna_Add("Angle", lx.symbol.sTYPE_ANGLE)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO GC - Select CoPlanar Poly'

    def cmd_Desc(self):
        return 'Replace the old Seneca Lazy Select by the Built in Select CoPlanar poly tool.'

    def cmd_Tooltip(self):
        return 'Replace the old Seneca Lazy Select by the Built in Select CoPlanar poly tool.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO GC - Select CoPlanar Poly'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()

        if self.SelModePoly:
            lx.eval('smo.MASTER.ForceSelectMeshItemOnly')



        mesh = scene.selectedByType('mesh')[0]
        SelItems = (lx.evalN('query sceneservice selection ? locator'))
        lx.out('Selected items is:', SelItems)

        def rad(a):                 # (360/2)/pi = 57.295779513082320876798154814105
            return a * 57.2957795130



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



        # ------------------------------ #
        # <----( DEFINE VARIABLES )----> #
        # ------------------------------ #
        #####--- Define user value for all the different SafetyCheck --- START ---#####
        #####
        lx.eval("user.defNew name:PolyCoPlanarAngle type:angle life:momentary")
        lx.eval("user.defNew name:PolyCoPlanarConnect type:integer life:momentary")
        lx.eval("user.defNew name:PolyCoPlanarRange type:distance life:momentary")
        # lx.eval("user.defNew name:ANGLE type:angle life:momentary")
        # lx.eval("user.defNew name:MODE type:integer life:momentary")
        # lx.eval("user.defNew name:RANGE type:distance life:momentary")
        #####
        #####--- Define user value for all the different SafetyCheck --- END ---#####

        #################################
        # <----( DEFINE ARGUMENTS )----> #
        #################################
        args = lx.args()
        lx.out(args)
        MODE = self.dyna_Int(0)         #  select = 0 (similarTouching)   ###   polygon(SimilarOnObject) = 1   ###   none = 2 (SimilarOnLayer)
        ANGLE = self.dyna_Int(1)  # in degree
        if not self.dyna_IsSet(2):
            RANGE = 10000.0
        else:
            RANGE = self.dyna_Float(2)  # in distance

        if self.dyna_Int(0) == 0:
            RANGE = 0.0

        # Expose the Result of the Arguments
        lx.out(MODE, ANGLE, RANGE)
        #################################
        # <----( DEFINE ARGUMENTS )----> #
        #################################

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

        # ---------------------------------- #
        # <----( Main Macro - POLYGON )----> #
        # ---------------------------------- #
        if ItemMode == 0 and VertMode == 0 and EdgeMode == 0 and PolyMode == 1 and CountItem > 0:
            if CountPoly > 0:
                lx.eval('tool.set select.polygonCoplanar on')

                ##########################################
                ## query State of Current Tool Settings ##
                ##########################################
                PolyCoPlanarAngle = lx.eval('tool.attr select.polygonCoplanar angle ?')
                PolyCoPlanarConnect = lx.eval('tool.attr select.polygonCoplanar connect ?')
                PolyCoPlanarRange = lx.eval('tool.attr select.polygonCoplanar range ?')
                # print(rad(PolyCoPlanarAngle))
                # print(PolyCoPlanarConnect)
                # print(PolyCoPlanarRange)

                # ------------------------------------- #
                ## Set defined Settings and Run the tool ##
                # ------------------------------------- #
                lx.eval('tool.attr select.polygonCoplanar angle %s' % ANGLE)
                if MODE == 0 : # Similar Touching (Filter selection)
                    lx.eval('tool.attr select.polygonCoplanar connect select')
                if MODE == 1 : # Similar On Object (filter connected polygon)
                    lx.eval('tool.attr select.polygonCoplanar connect polygon')
                if MODE == 2 : # Similar On Layer (filter none)
                    lx.eval('tool.attr select.polygonCoplanar connect none')
                lx.eval('tool.attr select.polygonCoplanar range %s' % RANGE)
                # Command Block Begin:  ToolAdjustment
                lx.eval('tool.setAttr select.polygonCoplanar angle %s' % ANGLE)
                if MODE == 0 : # Similar Touching
                    lx.eval('tool.setAttr select.polygonCoplanar connect select')
                if MODE == 1 : # Similar On Object
                    lx.eval('tool.setAttr select.polygonCoplanar connect polygon')
                if MODE == 2 : # Similar On Layer
                    lx.eval('tool.setAttr select.polygonCoplanar connect none')
                lx.eval('tool.setAttr select.polygonCoplanar range %s' % RANGE)
                # Command Block End:  ToolAdjustment
                lx.eval('tool.doApply')
                lx.eval('select.nextMode')

                ##########################################
                ## Set Back the previuous user Settings ##
                ##########################################
                # Revert previous User Settings for the Tool
                lx.eval('tool.set select.polygonCoplanar on')
                lx.eval('tool.attr select.polygonCoplanar angle %s' % rad(PolyCoPlanarAngle))
                lx.eval('tool.attr select.polygonCoplanar connect %s' % PolyCoPlanarConnect)
                # Command Block Begin:  ToolAdjustment
                lx.eval('tool.setAttr select.polygonCoplanar angle %s' % rad(PolyCoPlanarAngle))
                lx.eval('tool.setAttr select.polygonCoplanar connect %s' % PolyCoPlanarConnect)
                lx.eval('tool.setAttr select.polygonCoplanar range %s' % PolyCoPlanarRange)
                # Command Block End:  ToolAdjustment
                lx.eval('tool.set select.polygonCoplanar off')

        # Bugfix to remove a reset of Item Reference system to be set while a Workplane was set. It prevent the 3D view to be offset from current viewpoint.
        #         if RefSystemActive == False:
        #             lx.eval('item.refSystem {}')
        #         else:
        #             # print('Ref System activated')
        #             lx.eval('item.refSystem %s' % SelItems[0])
        #
        # if RefSystemActive == False:
        #     lx.eval('item.refSystem {}')
        if RefSystemActive:
            lx.eval('item.refSystem %s' % CurrentRefSystemItem)


    def cmd_Query(self, index, vaQuery):
        lx.notimpl()


lx.bless(SMO_GC_SelectCoPlanarPoly_Cmd, Cmd_Name)
