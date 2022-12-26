# python
"""
# Name:         SMO_MIFABOMA_RADIALSWEEP_RelativeToParent_Cmd.py
# Version:      1.0
#
# Purpose:      This Command is designed to :
#               Radial Sweep current Polygon Selection (or all Poly if no selection) / or Selected Edges
#               using Origin Center (World) or Item Center (Local). You need to get at least one Mesh item selected.
#
# Author:       Franck ELISABETH (with the help of Tom Dymond for debug)
# Website:      https://www.smoluck.com
#
# Created:      16/09/2019
# Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.MIFABOMA.RadialSweepRelativeToParent"
# smo.MIFABOMA.RadialSweepRelativeToParent 1 32 1 360 0 0


class SMO_MIFABOMA_RadialSweepRelativeToParent_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Axis", lx.symbol.sTYPE_INTEGER)
        self.dyna_Add("Count", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags (1, lx.symbol.fCMDARG_OPTIONAL)             # here the (1) define the argument index.
        self.dyna_Add("Caps Mode", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags (2, lx.symbol.fCMDARG_OPTIONAL)
        self.dyna_Add("Square Mode", lx.symbol.sTYPE_BOOLEAN)
        self.basic_SetFlags (3, lx.symbol.fCMDARG_OPTIONAL)

        self.SelModeEdge = bool(lx.eval1("select.typeFrom typelist:edge;vertex;polygon;item ?"))
        self.SelModePoly = bool(lx.eval1("select.typeFrom typelist:polygon;vertex;edge;item ?"))

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO MIFABOMA - Radial Sweep Relative to Parent'
    
    def cmd_Desc (self):
        return 'Radial Sweep current Polygon Selection (or all Poly if no selection) / or Selected Edges using Origin Center (World) or Item Center (Local).'
    
    def cmd_Tooltip (self):
        return 'Radial Sweep current Polygon Selection (or all Poly if no selection) / or Selected Edges using Origin Center (World) or Item Center (Local).'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO MIFABOMA - Radial Sweep Relative to Parent'
    
    def basic_Enable (self, msg):
        return True
    
    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()
        if self.SelModePoly == True or self.SelModeEdge == True:
            lx.eval('smo.MASTER.ForceSelectMeshItemOnly')

        mesh = scene.selectedByType('mesh')[0]
        SelItems = (lx.evalN('query sceneservice selection ? locator'))
        #lx.out('Selected items is:',SelItems)
        
        
        
        # ------------------------------ #
        # <----( DEFINE ARGUMENTS )----> #                # smo.MIFABOMA.RadialSweep 1 32 1 0 0
        # ------------------------------ #
        args = lx.args()
        lx.out(args)
        RADIAL_AXES = self.dyna_Int (0)                 # Axes selection:       X = 0 ### Y = 1 ### Z = 2
        ARRAY_COUNT = self.dyna_Int (1)                 # Count 4
        CAPS = self.dyna_Int (2)                        # Caps off = 0  ### Cap End = 1 ### Cap Start = 2 ### Caps Both = 3
        SQUARE = self.dyna_Bool (3)                     # Off = 0 ### On = 1
        # Expose the Result of the Arguments 
        lx.out(RADIAL_AXES,ARRAY_COUNT,CAPS,SQUARE)
        # ------------------------------ #
        # <----( DEFINE ARGUMENTS )----> #
        # ------------------------------ #
        
        
        
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
        lx.out('Vert Mode',VertMode)
        lx.out('Edge Mode',EdgeMode)
        lx.out('Poly Mode',PolyMode)
        lx.out('Item Mode',ItemMode)
        lx.out('V---------- Element Not Selected ----------V')
        lx.out('No Vert Selected',NoVert)
        lx.out('No Edge Selected',NoEdge)
        lx.out('No Poly Selected',NoPoly)
        lx.out('No Item Selected',NoItem)
        lx.out('V---------- At least one Element Selected ----------V')
        lx.out('Multi Vert Selected',MultiVert)
        lx.out('Multi Edge Selected',MultiEdge)
        lx.out('Multi Poly Selected',MultiPoly)
        lx.out('Multi Item Selected',MultiItem)
        lx.out('V---------- At least one Element Selected ----------V')
        lx.out('Vert Count Selected',CountVert)
        lx.out('Multi Count Selected',CountEdge)
        lx.out('Multi Count Selected',CountPoly)
        lx.out('Multi Count Selected',CountItem)
        
        
        
        StartANGLE = lx.eval1('user.value SMO_UseVal_MIFABOMA_RadialSweep_StartAngle_Preset ?')
        EndANGLE = lx.eval1('user.value SMO_UseVal_MIFABOMA_RadialSweep_EndAngle_Preset ?')
        lx.out('Start Angle',StartANGLE)
        lx.out('End Angle',EndANGLE)
        
        
        
        # ---------------------------------- #
        # <----( Main Macro - POLYGON )----> #
        # ---------------------------------- #
        if ItemMode == 0 and VertMode == 0 and EdgeMode == 0 and PolyMode == 1 and CountItem > 0 :
        
            # ------ PARENT  / CHILD Checkup ------ #
            # ------------------------------------- #
            if CountPoly > 0 :
                lx.eval('hide.unsel')
            lx.eval('tool.set actr.auto on 0')
            lx.eval('select.type item')
            # Tag TARGET
            lx.eval('select.editSet RadArr_ITEM_TARGET add')
            
            # Select item Hierarchy to test child presence
            lx.eval('select.itemHierarchy')
            ChildItems = len(lx.evalN('query sceneservice selection ? mesh'))
            lx.out('ChildItems',ChildItems)
            if ChildItems >= 2 :
                ChildPresent = True
                lx.out('This Target as Child elements')
                lx.eval('select.useSet RadArr_ITEM_TARGET deselect')
                lx.eval('select.editSet RadArr_ITEM_CHILD add {}')
                lx.eval('select.useSet RadArr_ITEM_TARGET select')
                lx.eval('select.useSet RadArr_ITEM_CHILD deselect')
            elif ChildItems == 1 :
                ChildPresent = False
                lx.out('This Target doesn`t have Child elements')
                lx.eval('select.useSet RadArr_ITEM_TARGET deselect')
                lx.eval('select.useSet RadArr_ITEM_TARGET replace')
                
            # Tag PARENT of TARGET
            item = modo.Scene().selected[0]
            item.parent.select()
            lx.eval('select.useSet RadArr_ITEM_TARGET deselect')
            ParentItem = len(lx.evalN('query sceneservice selection ? locator'))
            lx.out('ParentItem',ParentItem)
            # Check if Parent exist on this target mesh
            if ParentItem == 1 :
                ParentPresent = 1
                lx.out('This Target as Parent')
                lx.eval('select.editSet RadArr_ITEM_PARENT add')
                lx.eval('select.useSet RadArr_ITEM_TARGET replace')
            elif ParentItem == 0 :
                ParentPresent = 0
                lx.out('This Target doesn`t have Parent')
                lx.eval('select.useSet RadArr_ITEM_TARGET deselect')
                lx.eval('select.useSet RadArr_ITEM_TARGET replace')
                lx.eval('select.drop item')
                
            # Do actions wether Parent exist or Not
            if ParentPresent == 1 :
                lx.eval('select.drop item')
                lx.eval('select.useSet RadArr_ITEM_PARENT replace')
                SelItems = (lx.evalN('query sceneservice selection ? locator'))
                lx.out('Selected items is:',SelItems)
                lx.eval('item.refSystem %s' % SelItems)
                lx.eval('select.drop item')
                lx.eval('select.useSet RadArr_ITEM_TARGET replace')
                
            lx.eval('select.drop item')
            lx.eval('select.useSet RadArr_ITEM_TARGET replace')
            # ------------------------------------- #
            
            
            
            
            lx.eval('tool.set actr.auto on 0')
            lx.eval('select.type item')
            
            lx.eval('tool.set actr.origin on')
            lx.eval('select.type polygon')
            
            
            # ------------------------------------- #
            # ------ Radial Sweep Tool Setup ------ #
            # ------------------------------------- #
            lx.eval('tool.set "Radial Sweep" on')
            if not SQUARE:
                lx.eval('tool.setAttr gen.helix square false')
                lx.eval('tool.setAttr gen.helix sides %s' % ARRAY_COUNT)
                lx.eval('tool.setAttr gen.helix start %s' % StartANGLE)
                lx.eval('tool.setAttr gen.helix end %s' % EndANGLE)
                
            lx.eval('tool.setAttr effector.sweep flip false')
            if SQUARE:
                lx.eval('tool.setAttr gen.helix square true')
                
            if CAPS == 0 :
                lx.eval('tool.setAttr effector.sweep cap0 false')
                lx.eval('tool.setAttr effector.sweep cap1 false')
            if CAPS == 1 :
                lx.eval('tool.setAttr effector.sweep cap0 true')
                lx.eval('tool.setAttr effector.sweep cap1 false')
            if CAPS == 2 :
                lx.eval('tool.setAttr effector.sweep cap0 false')
                lx.eval('tool.setAttr effector.sweep cap1 true')
            if CAPS == 3 :
                lx.eval('tool.setAttr effector.sweep cap0 true')
                lx.eval('tool.setAttr effector.sweep cap1 true')
                
                
            lx.eval('tool.setAttr gen.helix cenX 0.0')
            lx.eval('tool.setAttr gen.helix cenY 0.0')
            lx.eval('tool.setAttr gen.helix cenZ 0.0')
            
            if RADIAL_AXES == 0:
                lx.eval('tool.setAttr gen.helix axis 0')
                lx.eval('tool.setAttr gen.helix vecX 1.0')
                lx.eval('tool.setAttr gen.helix vecY 0.0')
                lx.eval('tool.setAttr gen.helix vecZ 0.0')
            if RADIAL_AXES == 1:
                lx.eval('tool.setAttr gen.helix axis 1')
                lx.eval('tool.setAttr gen.helix vecX 0.0')
                lx.eval('tool.setAttr gen.helix vecY 1.0')
                lx.eval('tool.setAttr gen.helix vecZ 0.0')
            if RADIAL_AXES == 2:
                lx.eval('tool.setAttr gen.helix axis 2')
                lx.eval('tool.setAttr gen.helix vecX 0.0')
                lx.eval('tool.setAttr gen.helix vecY 0.0')
                lx.eval('tool.setAttr gen.helix vecZ 1.0')
            # -------------------------- #
            lx.eval('tool.doApply')
            lx.eval('select.drop polygon')
            lx.eval('select.nextMode')
            lx.eval('item.refSystem {}')
            lx.eval('tool.set actr.auto on 0')
            
            
            
            # ------ PARENT  / CHILD Checkup ------ #
            # ------------------------------------- #
            lx.eval('select.type item')
            lx.eval('!select.deleteSet RadArr_ITEM_TARGET false')
            if ParentPresent == 1 :
                lx.eval('!select.deleteSet RadArr_ITEM_PARENT false')
            if ChildPresent:
                lx.eval('!select.deleteSet RadArr_ITEM_CHILD false')
            lx.eval('select.type polygon')
            lx.eval('unhide')
            # ------------------------------------- #
            lx.eval('select.type item')
            lx.eval('unhide')
            lx.eval('select.type polygon')
        
        
        
        
        # ------------------------------- #
        # <----( Main Macro - EDGE )----> #
        # ------------------------------- #
        if ItemMode == 0 and VertMode == 0 and EdgeMode == 1 and PolyMode == 0 and CountItem > 0 :
        
            # ------ PARENT  / CHILD Checkup ------ #
            # ------------------------------------- #
            lx.eval('select.type item')
            # Tag TARGET
            lx.eval('select.editSet RadArr_ITEM_TARGET add')
            
            # Select item Hierarchy to test child presence
            lx.eval('select.itemHierarchy')
            ChildItems = len(lx.evalN('query sceneservice selection ? mesh'))
            lx.out('ChildItems',ChildItems)
            if ChildItems >= 2 :
                ChildPresent = True
                lx.out('This Target as Child elements')
                lx.eval('select.useSet RadArr_ITEM_TARGET deselect')
                lx.eval('select.editSet RadArr_ITEM_CHILD add {}')
                lx.eval('select.useSet RadArr_ITEM_TARGET select')
                lx.eval('select.useSet RadArr_ITEM_CHILD deselect')
            elif ChildItems == 1 :
                ChildPresent = False
                lx.out('This Target doesn`t have Child elements')
                lx.eval('select.useSet RadArr_ITEM_TARGET deselect')
                lx.eval('select.useSet RadArr_ITEM_TARGET replace')
                
            # Tag PARENT of TARGET
            item = modo.Scene().selected[0]
            item.parent.select()
            lx.eval('select.useSet RadArr_ITEM_TARGET deselect')
            ParentItem = len(lx.evalN('query sceneservice selection ? locator'))
            lx.out('ParentItem',ParentItem)
            # Check if Parent exist on this target mesh
            if ParentItem == 1 :
                ParentPresent = 1
                lx.out('This Target as Parent')
                lx.eval('select.editSet RadArr_ITEM_PARENT add')
                lx.eval('select.useSet RadArr_ITEM_TARGET replace')
            elif ParentItem == 0:
                ParentPresent = 0
                lx.out('This Target doesn`t have Parent')
                lx.eval('select.useSet RadArr_ITEM_TARGET deselect')
                lx.eval('select.useSet RadArr_ITEM_TARGET replace')
                lx.eval('select.drop item')
                
            # Do actions wether Parent exist or Not
            if ParentPresent == 1:
                lx.eval('select.drop item')
                lx.eval('select.useSet RadArr_ITEM_PARENT replace')
                SelItems = (lx.evalN('query sceneservice selection ? locator'))
                lx.out('Selected items is:',SelItems)
                lx.eval('item.refSystem %s' % SelItems)
                lx.eval('select.drop item')
                lx.eval('select.useSet RadArr_ITEM_TARGET replace')
            # ------------------------------------- #
            
            
            
            lx.eval('select.drop item')
            lx.eval('select.useSet RadArr_ITEM_TARGET replace')
            
            
            
            lx.eval('tool.set actr.origin on')
            lx.eval('select.type edge')
            
            
            # ------------------------------------- #
            # ------ Radial Sweep Tool Setup ------ #
            # ------------------------------------- #
            lx.eval('tool.set "Radial Sweep" on')
            if not SQUARE:
                lx.eval('tool.setAttr gen.helix square false')
                lx.eval('tool.setAttr gen.helix sides %s' % ARRAY_COUNT)
                lx.eval('tool.setAttr gen.helix start %s' % StartANGLE)
                lx.eval('tool.setAttr gen.helix end %s' % EndANGLE)
                
            if SQUARE:
                lx.eval('tool.setAttr gen.helix square true')
                
            lx.eval('tool.setAttr effector.sweep flip true')
            lx.eval('tool.setAttr effector.sweep cap0 false')
            lx.eval('tool.setAttr effector.sweep cap1 false')
                
                
            lx.eval('tool.setAttr gen.helix cenX 0.0')
            lx.eval('tool.setAttr gen.helix cenY 0.0')
            lx.eval('tool.setAttr gen.helix cenZ 0.0')
            
            if RADIAL_AXES == 0:
                lx.eval('tool.setAttr gen.helix axis 0')
                lx.eval('tool.setAttr gen.helix vecX 1.0')
                lx.eval('tool.setAttr gen.helix vecY 0.0')
                lx.eval('tool.setAttr gen.helix vecZ 0.0')
            if RADIAL_AXES == 1:
                lx.eval('tool.setAttr gen.helix axis 1')
                lx.eval('tool.setAttr gen.helix vecX 0.0')
                lx.eval('tool.setAttr gen.helix vecY 1.0')
                lx.eval('tool.setAttr gen.helix vecZ 0.0')
            if RADIAL_AXES == 2:
                lx.eval('tool.setAttr gen.helix axis 2')
                lx.eval('tool.setAttr gen.helix vecX 0.0')
                lx.eval('tool.setAttr gen.helix vecY 0.0')
                lx.eval('tool.setAttr gen.helix vecZ 1.0')
            # -------------------------- #
            lx.eval('tool.doApply')
            lx.eval('select.drop edge')
            lx.eval('select.nextMode')
            lx.eval('item.refSystem {}')
            lx.eval('tool.set actr.auto on 0')
            
            
            
            # ------ PARENT  / CHILD Checkup ------ #
            # ------------------------------------- #
            lx.eval('select.type item')
            lx.eval('unhide')
            lx.eval('!select.deleteSet RadArr_ITEM_TARGET false')
            if ParentPresent == 1 :
                lx.eval('!select.deleteSet RadArr_ITEM_PARENT false')
            if ChildPresent:
                lx.eval('!select.deleteSet RadArr_ITEM_CHILD false')
            lx.eval('select.type polygon')
            # ------------------------------------- #
            lx.eval('select.type item')
            lx.eval('unhide')
            lx.eval('select.type polygon')
        
        lx.out('End of SMO RadialSweep  Command')


    def cmd_Query(self, index, vaQuery):
        lx.notimpl()


lx.bless(SMO_MIFABOMA_RadialSweepRelativeToParent_Cmd, Cmd_Name)
