# python
"""
Name:         SMO_MIFABOMA_RADIALARRAY_ViaUserPref_Cmd.py

Purpose:      This Command is designed to :
              RadialArray current Polygon Selection (or all Poly if no selection)
              using Origin Center (World) or Item Center (Local).
              You need to get at least one Mesh item selected.

Author:       Franck ELISABETH (with the help of Tom Dymond for debug)
Website:      https://www.smoluck.com
Created:      16/09/2019
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.MIFABOMA.RadialArray.ViaUserPref"
# smo.MIFABOMA.RadialArray.ViaUserPref 1 8 1 0


class SMO_MIFABOMA_RadialArray_ViaUserPref_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Axis", lx.symbol.sTYPE_INTEGER)
        self.dyna_Add("Count", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags (1, lx.symbol.fCMDARG_OPTIONAL)             # here the (1) define the argument index.
        self.dyna_Add("Action Center Mode", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags (2, lx.symbol.fCMDARG_OPTIONAL)
        self.dyna_Add("MergeMode", lx.symbol.sTYPE_BOOLEAN)
        self.basic_SetFlags (3, lx.symbol.fCMDARG_OPTIONAL)

        self.SelModeVert = bool(lx.eval1("select.typeFrom typelist:vertex;polygon;edge;item;ptag ?"))
        self.SelModeEdge = bool(lx.eval1("select.typeFrom typelist:edge;vertex;polygon;item ?"))
        self.SelModePoly = bool(lx.eval1("select.typeFrom typelist:polygon;vertex;edge;item ?"))
        self.SelModeItem = bool(lx.eval1("select.typeFrom typelist:item;pivot;center;edge;polygon;vertex;ptag ?"))
        # print(self.SelModeVert)
        # print(self.SelModeEdge)
        # print(self.SelModePoly)
        # print(self.SelModeItem)
    
    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO MIFABOMA - RadialArray'
    
    def cmd_Desc (self):
        return 'RadialArray current Polygon Selection (or all Poly if no selection) using Origin Center (World) or Item Center (Local).'
    
    def cmd_Tooltip (self):
        return 'RadialArray current Polygon Selection (or all Poly if no selection) using Origin Center (World) or Item Center (Local).'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO MIFABOMA - RadialArray'
    
    def basic_Enable (self, msg):
        return True
    
    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()

        VertMode = bool(self.SelModeVert)
        EdgeMode = bool(self.SelModeEdge)
        PolyMode = bool(self.SelModePoly)
        ItemMode = bool(self.SelModeItem)

        ##### Create a list of selected Targets items (meshes and instances)
        TargetMeshes = []
        SelectedInstances = list(scene.selectedByType("meshInst"))
        print(SelectedInstances)
        for item in SelectedInstances:
            TargetMeshes.append(item)

        SelectedMeshes = list(scene.selectedByType("mesh"))
        print(SelectedMeshes)
        for item in SelectedMeshes:
            TargetMeshes.append(item)
        print(TargetMeshes)


        if self.SelModePoly == True or self.SelModeEdge == True:
            lx.eval('smo.MASTER.ForceSelectMeshItemOnly')


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



        CloneType_Clone = lx.eval('user.value SMO_UseVal_MIFABOMA_CloneType_Clone ?')
        lx.out('Clone item regular:',CloneType_Clone)

        CloneType_Instance = lx.eval('user.value SMO_UseVal_MIFABOMA_CloneType_Instance ?')
        lx.out('Clone item by Instance state:',CloneType_Instance)

        CloneType_Replicas = lx.eval('user.value SMO_UseVal_MIFABOMA_CloneType_Replicas ?')
        lx.out('Clone item by Replicas state:',CloneType_Replicas)

        Clone_Hierarchy = lx.eval('user.value SMO_UseVal_MIFABOMA_CloneChilds ?')
        lx.out('Clone Hierarchy state:',Clone_Hierarchy)

        BackupCloneHierarchyState = Clone_Hierarchy

        if CloneType_Clone == 0 and CloneType_Instance == 0 and CloneType_Replicas == 1:
            Clone_Hierarchy = 0


        # ------------------------------ #
        # <----( DEFINE ARGUMENTS )----> #                # smo.RadialArray 1 8 1 0 1 0
        # ------------------------------ #
        args = lx.args()
        lx.out(args)
        RADIAL_AXES = self.dyna_Int (0)                 # Axes selection:       X = 0 ### Y = 1 ### Z = 2
        ARRAY_COUNT = self.dyna_Int (1)             # Count 4
        ACT_CENTER_MODE = self.dyna_Int (2)             # World = 0 ### Local = 1 ### Relative to Parent = 2
        MERGE_VERTEX = self.dyna_Bool (3)               # Off = 0 ### On = 1

        # Expose the Result of the Arguments
        lx.out(RADIAL_AXES,ARRAY_COUNT,ACT_CENTER_MODE,MERGE_VERTEX)
        # ------------------------------ #
        # <----( DEFINE ARGUMENTS )----> #
        # ------------------------------ #

        ChildPresent = bool()
        ParentPresent = bool()


        lx.eval('smo.GC.DeselectAll')


        # ---------------------------------- #
        # <----( Main Macro - POLYGON )----> #
        # ---------------------------------- #
        if ItemMode == 0 and VertMode == 0 and EdgeMode == 0 and PolyMode == 1:
            for item in SelectedMeshes:
                item.select(True)

                mesh = scene.selectedByType('mesh')[0]
                SelItems = (lx.evalN('query sceneservice selection ? locator'))
                lx.out('Selected items is:', SelItems)

                lx.eval('smo.MASTER.SelectModeDetector')

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

                # ------ PARENT  / CHILD Checkup ------ #
                # ------------------------------------- #
                lx.eval('tool.set actr.auto on 0')
                lx.eval('select.type item')

                if not RefSystemActive:
                    lx.eval('item.refSystem %s' % SelItems[0])
                else :
                    print('Ref System activated')


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
                try :
                    item.parent.select()
                    ParentPresent = 1
                except :
                    ParentPresent = 0
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
                    SelItemsParent = (lx.evalN('query sceneservice selection ? locator'))
                    lx.out('Selected items is:',SelItemsParent)
                    if CloneType_Replicas == 0 and ACT_CENTER_MODE == 2 :
                        lx.eval('item.refSystem %s' % SelItems)
                    lx.eval('select.drop item')
                    lx.eval('select.useSet RadArr_ITEM_TARGET replace')

                lx.eval('select.drop item')
                lx.eval('select.useSet RadArr_ITEM_TARGET replace')
                # ------------------------------------- #
                lx.eval('select.type polygon')

                if CountPoly > 0 :
                    lx.eval('hide.unsel')
                lx.eval('tool.set actr.auto on 0')
                lx.eval('select.type item')
                if ACT_CENTER_MODE == 0 :
                    lx.eval('item.refSystem {}')
                if ACT_CENTER_MODE == 1 :
                    lx.eval('item.refSystem %s' % SelItems)
                if ACT_CENTER_MODE == 2 :
                    lx.eval('item.refSystem %s' % SelItemsParent)
                lx.eval('tool.set actr.origin on')
                lx.eval('select.type polygon')


                # ------------------------------------- #
                # ------ Radial Array Tool Setup ------ #
                # ------------------------------------- #
                lx.eval('tool.set "*.Radial Array" on')

                if MERGE_VERTEX == 0:
                    lx.eval('tool.setAttr effector.clone merge false')
                if MERGE_VERTEX == 1:
                    lx.eval('tool.setAttr effector.clone merge true')
                    lx.eval('tool.setAttr effector.clone dist 0.0001')

                lx.eval('tool.setAttr gen.helix sides %s' % ARRAY_COUNT)
                lx.eval('tool.setAttr gen.helix cenX 0.0')
                lx.eval('tool.setAttr gen.helix cenY 0.0')
                lx.eval('tool.setAttr gen.helix cenZ 0.0')
                lx.eval('tool.setAttr gen.helix start 0.0')
                lx.eval('tool.setAttr gen.helix end 360.0')
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

                if ACT_CENTER_MODE == 1 :
                    lx.eval('item.refSystem {}')
                if ACT_CENTER_MODE == 2 :
                    lx.eval('item.refSystem {}')




                if not RefSystemActive:
                    lx.eval('item.refSystem {}')
                else:
                    print('Ref System activated')
                    lx.eval('item.refSystem %s' % SelItems[0])

                lx.eval('tool.set actr.auto on 0')
                if CountPoly > 0 :
                    lx.eval('unhide')

                # ------ PARENT  / CHILD Checkup ------ #
                # ------------------------------------- #
                lx.eval('select.type item')
                if ParentPresent == 1 :
                    lx.eval('!select.deleteSet RadArr_ITEM_PARENT false')
                if ChildPresent:
                    lx.eval('!select.deleteSet RadArr_ITEM_CHILD false')
                lx.eval('select.drop item')
                lx.eval('select.useSet RadArr_ITEM_TARGET replace')
                lx.eval('!select.deleteSet RadArr_ITEM_TARGET false')
                lx.eval('select.type polygon')
                # ------------------------------------- #


        # ------------------------------ #
        # <----( Main Macro - ITEM)----> #
        # ------------------------------ #
        if ItemMode == 1 and VertMode == 0 and EdgeMode == 0 and PolyMode == 0:
            for item in TargetMeshes:
                item.select(True)

                SelItems = (lx.evalN('query sceneservice selection ? locator'))
                lx.out('Selected items is:', SelItems)

                # ------ PARENT  / CHILD Checkup ------ #
                # ------------------------------------- #
                lx.eval('tool.set actr.auto on 0')
                lx.eval('select.type item')
                # Tag TARGET
                lx.eval('select.editSet RadArr_ITEM_TARGET add')

                # Select item Hierarchy to test child presence
                lx.eval('select.itemHierarchy')
                ChildItems = len(lx.evalN('query sceneservice selection ? all'))
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
                try :
                    item.parent.select()
                    ParentPresent = 1
                except :
                    ParentPresent = 0
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
                    SelItemsParent = (lx.evalN('query sceneservice selection ? locator'))
                    lx.out('Selected items is:',SelItemsParent)
                    if CloneType_Replicas == 0 and ACT_CENTER_MODE == 2 :
                        lx.eval('item.refSystem %s' % SelItems)
                    lx.eval('select.drop item')
                    lx.eval('select.useSet RadArr_ITEM_TARGET replace')

                lx.eval('select.drop item')
                lx.eval('select.useSet RadArr_ITEM_TARGET replace')
                # ------------------------------------- #

                lx.eval('tool.set actr.auto on 0')
                lx.eval('select.type item')
                if ACT_CENTER_MODE == 1 and CloneType_Replicas == 0 :
                    lx.eval('select.drop item')
                    lx.eval('select.useSet RadArr_ITEM_TARGET select')
                    SelItems = (lx.evalN('query sceneservice selection ? locator'))
                    lx.out('Selected items is:',SelItems)
                    lx.eval('item.refSystem %s' % SelItems)
                    lx.eval('tool.set actr.origin on')
                if ACT_CENTER_MODE == 2 and CloneType_Replicas == 0 and ParentPresent == 1 :
                    lx.eval('select.drop item')
                    lx.eval('select.useSet RadArr_ITEM_PARENT select')
                    SelItemsParent = (lx.evalN('query sceneservice selection ? locator'))
                    lx.out('Selected items is:',SelItemsParent)
                    lx.eval('item.refSystem %s' % SelItemsParent)
                    lx.eval('tool.set actr.origin on')
                    lx.eval('select.drop item')
                    lx.eval('select.useSet RadArr_ITEM_TARGET replace')
                if ACT_CENTER_MODE == 1 and CloneType_Replicas == 1 and ParentPresent == 1 :
                    lx.eval('item.parent parent:{} inPlace:1')
                if ACT_CENTER_MODE == 2 and CloneType_Replicas == 1 and ParentPresent == 1 :
                    lx.eval('item.parent parent:{} inPlace:1')
                    lx.eval('select.drop item')
                    lx.eval('select.useSet RadArr_ITEM_TARGET select')




                # ------------------------------------- #
                # ------ Radial Array Tool Setup ------ #
                # ------------------------------------- #
                if CloneType_Clone == 1 and CloneType_Instance == 0 and CloneType_Replicas == 0 :
                    lx.eval('tool.set "*.Radial Array" on')
                    lx.eval('tool.setAttr effector.item instance false')
                if CloneType_Clone == 0 and CloneType_Instance == 1 and CloneType_Replicas == 0 :
                    lx.eval('tool.set "Instance Radial Array" on')
                    lx.eval('tool.setAttr effector.item instance true')
                if CloneType_Clone == 0 and CloneType_Instance == 0 and CloneType_Replicas == 1 :
                    lx.eval('tool.set "Replica Radial Array" on')
                    lx.eval('tool.setAttr effector.replica source active')

                if Clone_Hierarchy == 1 and CloneType_Replicas == 0 :
                    lx.eval('tool.setAttr effector.item hierarchy true')

                if Clone_Hierarchy == 0 and CloneType_Replicas == 0 :
                    lx.eval('tool.setAttr effector.item hierarchy false')


                lx.eval('tool.setAttr gen.helix sides %s' % ARRAY_COUNT)
                if CloneType_Replicas == 0 :
                    lx.eval('tool.setAttr gen.helix cenX 0.0')
                    lx.eval('tool.setAttr gen.helix cenY 0.0')
                    lx.eval('tool.setAttr gen.helix cenZ 0.0')

                lx.eval('tool.setAttr gen.helix start 0.0')
                lx.eval('tool.setAttr gen.helix end 360.0')
                if RADIAL_AXES == 0 :
                    lx.eval('tool.setAttr gen.helix axis 0')
                    if CloneType_Replicas == 1 and ACT_CENTER_MODE == 1 :
                        lx.eval('tool.set actr.auto on 0')
                        lx.eval('tool.set actr.pivot on')
                    if CloneType_Replicas == 1 and ACT_CENTER_MODE == 2 :
                        lx.eval('tool.set actr.parent on')

                    lx.eval('tool.setAttr gen.helix vecX 1.0')
                    lx.eval('tool.setAttr gen.helix vecY 0.0')
                    lx.eval('tool.setAttr gen.helix vecZ 0.0')

                if RADIAL_AXES == 1 :
                    lx.eval('tool.setAttr gen.helix axis 1')
                    if CloneType_Replicas == 1 and ACT_CENTER_MODE == 1 :
                        lx.eval('tool.set actr.auto on 0')
                        lx.eval('tool.set actr.pivot on')
                    if CloneType_Replicas == 1 and ACT_CENTER_MODE == 2 :
                        lx.eval('tool.set actr.parent on')

                    lx.eval('tool.setAttr gen.helix vecX 0.0')
                    lx.eval('tool.setAttr gen.helix vecY 1.0')
                    lx.eval('tool.setAttr gen.helix vecZ 0.0')

                if RADIAL_AXES == 2 :
                    lx.eval('tool.setAttr gen.helix axis 2')
                    if CloneType_Replicas == 1 and ACT_CENTER_MODE == 1 :
                        lx.eval('tool.set actr.auto on 0')
                        lx.eval('tool.set actr.pivot on')
                    if CloneType_Replicas == 1 and ACT_CENTER_MODE == 2 :
                        lx.eval('tool.set actr.parent on')

                    lx.eval('tool.setAttr gen.helix vecX 0.0')
                    lx.eval('tool.setAttr gen.helix vecY 0.0')
                    lx.eval('tool.setAttr gen.helix vecZ 1.0')
                # -------------------------- #
                lx.eval('tool.doApply')
                lx.eval('select.nextMode')
                if ACT_CENTER_MODE == 1 and CloneType_Replicas == 0:
                    lx.eval('item.refSystem {}')
                if ACT_CENTER_MODE == 1 and CloneType_Replicas == 1 :
                    lx.eval('select.useSet RadArr_ITEM_PARENT select')
                    lx.eval('item.parent inPlace:1')
                    lx.eval('select.drop item')
                    lx.eval('select.useSet RadArr_ITEM_TARGET replace')
                if ACT_CENTER_MODE == 2 and CloneType_Replicas == 0:
                    lx.eval('item.refSystem {}')
                lx.eval('tool.set actr.auto on 0')
                lx.eval('select.drop item')

                # ------ PARENT  / CHILD Checkup ------ #
                # ------------------------------------- #
                lx.eval('select.type item')
                lx.eval('!select.deleteSet RadArr_ITEM_TARGET false')
                if ParentPresent == 1 :
                    lx.eval('!select.deleteSet RadArr_ITEM_PARENT false')
                if ChildPresent:
                    lx.eval('!select.deleteSet RadArr_ITEM_CHILD false')
                # ------------------------------------- #




                if CloneType_Clone == 0 and CloneType_Instance == 0 and CloneType_Replicas == 1:
                    lx.eval('user.value SMO_UseVal_MIFABOMA_CloneChilds %s' % BackupCloneHierarchyState)

        if not RefSystemActive:
            lx.eval('item.refSystem {}')
        if RefSystemActive:
            lx.eval('item.refSystem %s' % CurrentRefSystemItem)

        lx.out('End of SMO RadialArray  Command')


    def cmd_Query(self, index, vaQuery):
        lx.notimpl()


lx.bless(SMO_MIFABOMA_RadialArray_ViaUserPref_Cmd, Cmd_Name)
